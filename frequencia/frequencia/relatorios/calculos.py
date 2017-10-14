import datetime, calendar
from datetime import timedelta

from django.db.models import Q

from frequencia.registro.models import Frequencia
from frequencia.justificativas.models import JustificativaFalta
from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte

def get_primeiro_dia_trabalho(vinculo):
	return Frequencia.objects.filter(bolsista=vinculo).first()

def get_registros_bolsista(vinculo, data_inicio, data_fim):
	return Frequencia.objects.filter(bolsista=vinculo, created_at__date__gte=data_inicio, created_at__date__lte=data_fim)

def get_ausencias_bolsista(vinculo, data_inicio, data_fim):
	justificativas = JustificativaFalta.objects.filter(vinculo=vinculo, status=2)
	return justificativas.filter(Q(inicio__month=data_inicio.month,
											 inicio__year=data_inicio.year)	|
										   Q(termino__month=data_fim.month,
										   	 termino__year=data_fim.year))

def get_horas_abonadas_periodo(ausencias, calendario, data_inicio, data_fim):
	horas_abonadas = timedelta()
	for ausencia in ausencias:
		total_dias_ausencia = calendario.count_working_days(ausencia.inicio, ausencia.termino)
		total_dias_ausencia_periodo = calendario.count_working_days(ausencia.inicio if ausencia.inicio >= data_inicio else data_inicio,
																ausencia.termino if ausencia.termino <= data_fim else data_fim)
		horas_abonadas += ausencia.horas_abonadas / total_dias_ausencia * total_dias_ausencia_periodo		
	return horas_abonadas

def get_total_horas_trabalhadas(registros):
	horas_trabalhadas = timedelta()

	dias = registros.extra({'data': "date(created_at)"}).values('data').distinct()

	for dia in dias:
		entradas = registros.filter(tipo=0, created_at__date=dia['data'])
		saidas = registros.filter(tipo=1, created_at__date=dia['data'])

		for i, saida in enumerate(saidas):
			horas_trabalhadas += saida.created_at - entradas[i].created_at

	return horas_trabalhadas

"""
Retorna o cálculo:
Total de horas a trabalhar - horas trabalhadas - horas abonadas
"""
def get_balanco_mes(vinculo, mes, ano):
	calendario = FeriadosRioGrandeDoNorte()
	num_dias_mes = calendar.monthrange(ano, mes)[1]

	data_inicio = datetime.date(ano, mes, 1) 
	data_fim = datetime.date(ano, mes, num_dias_mes)

	num_dias_uteis_mes = calendario.count_working_days(data_inicio, data_fim)
	horas_trabalhar = num_dias_uteis_mes * (vinculo.carga_horaria_diaria or 0)
	horas_trabalhar = timedelta(hours=horas_trabalhar)

	frequencias = get_registros_bolsista(vinculo, data_inicio, data_fim)
	ausencias = get_ausencias_bolsista(vinculo, data_inicio, data_fim)

	horas_trabalhadas = get_total_horas_trabalhadas(frequencias)
	horas_abonadas_periodo = get_horas_abonadas_periodo(ausencias, calendario, data_inicio, data_fim)

	saldo_mes = horas_trabalhar - horas_trabalhadas - horas_abonadas_periodo
	return saldo_mes

def get_balanco_mes_anterior(vinculo, mes_atual, ano_atual):
	saldo_mes_anterior = timedelta()

	#Retornará zero se for o primeiro mês de trabalho do bolsista
	try:
		primeiro_dia_trabalho = get_primeiro_dia_trabalho(vinculo).created_at
		if primeiro_dia_trabalho.month is not mes_atual and primeiro_dia_trabalho.year is not ano_atual:
			mes_ano_anterior = datetime.date(ano_atual, mes_atual, 1) - timedelta(days=1)
			saldo_mes_anterior = get_balanco_mes(vinculo, mes_ano_anterior.month, mes_ano_anterior.year)
	except:
		return saldo_mes_anterior
	finally:
		return saldo_mes_anterior
	

def get_relatorio_mes(vinculo, mes, ano):

	registros = []
	horas_trabalhadas_periodo = timedelta()

	calendario = FeriadosRioGrandeDoNorte()
	feriados = calendario.holidays(ano)

	numero_dias = calendar.monthrange(ano, mes)[1]
	data_inicio = datetime.date(ano, mes, 1)
	data_fim = datetime.date(ano, mes, numero_dias)

	frequencias = get_registros_bolsista(vinculo, data_inicio, data_fim)
	ausencias = get_ausencias_bolsista(vinculo, data_inicio, data_fim)

	if not frequencias and not ausencias:
		return None

	for dia in range(1, numero_dias + 1):
		dia = datetime.date(ano, mes, dia)
		relatorio_dia = {'dia' : dia}

		feriado = [feriado for feriado in feriados if feriado[0] == dia]
	
		relatorio_dia['feriado'] = feriado[0] if feriado else False

		ausencia = ausencias.filter(inicio__lte=dia, termino__gte=dia)
		relatorio_dia['ausencia'] = ausencia if ausencia.exists() else False

		registros_dia = frequencias.filter(created_at__date=dia)
		relatorio_dia['registros'] = registros_dia
		horas_trabalhadas = get_total_horas_trabalhadas(registros_dia)
		relatorio_dia['horas_trabalhadas'] = horas_trabalhadas
		horas_trabalhadas_periodo += horas_trabalhadas		

		relatorio_dia['is_util'] = not relatorio_dia['feriado'] \
								   and not relatorio_dia['ausencia'] \
								   and super(FeriadosRioGrandeDoNorte, calendario).is_working_day(dia)

		registros.append(relatorio_dia)

	dias_uteis = calendario.count_working_days(data_inicio, data_fim)	
	
	return  {'registros': registros,
			 'dias_uteis': dias_uteis,
			 'total_horas_trabalhar': timedelta(hours=vinculo.carga_horaria_diaria) * dias_uteis,
			 'horas_trabalhadas_periodo': horas_trabalhadas_periodo,
			 'horas_abonadas_periodo': get_horas_abonadas_periodo(ausencias, calendario, data_inicio, data_fim),
			 'saldo_mes_anterior': get_balanco_mes_anterior(vinculo, mes, ano),
		    }

def get_relatorio_mensal_setor(setor, mes, ano):

	bolsistas = setor.vinculos.filter(group__name='Bolsista', 
									  ativo=True, 
									  user__is_active=True, 
									  created_at__month__lte=mes, 
									  created_at__year__lte=ano)

	relatorio = []	
	for bolsista in bolsistas:

		balanco_mes = get_balanco_mes(bolsista, mes, ano)
		balanco_mes_anterior = get_balanco_mes_anterior(bolsista, mes, ano)
		relatorio.append({
			'bolsista': bolsista,
			'balanco_mes_atual': balanco_mes,
			'balanco_mes_anterior': balanco_mes_anterior,
			'balanco_geral': balanco_mes + balanco_mes_anterior,		
		})

	return relatorio