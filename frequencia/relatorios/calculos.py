import datetime, calendar
from datetime import timedelta

from django.db.models import Q, F
from django.conf import settings

from frequencia.registro.models import Frequencia
from frequencia.justificativas.models import JustificativaFalta
from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte

def get_primeiro_dia_bolsa(vinculo):
	primeira_frequencia = Frequencia.objects.filter(bolsista=vinculo).order_by('created_at').first()
	primeira_justificativa = JustificativaFalta.objects.filter(vinculo=vinculo).order_by('created_at').first()
	return primeira_frequencia.created_at if primeira_frequencia.created_at.date() <= primeira_justificativa.inicio else primeira_justificativa.inicio

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
		if total_dias_ausencia and total_dias_ausencia_periodo:
			horas_abonadas += ausencia.horas_abonadas / total_dias_ausencia * total_dias_ausencia_periodo

	return horas_abonadas

def get_total_horas_registradas_contabilizadas(registros):
	ch_maxima_dia = timedelta(hours=settings.CH_MAXIMA_DIARIA)
	data_inicial_limitacao_ch = datetime.datetime.strptime(settings.DATA_INICIAL_LIMITACAO_CH_MAXIMA, '%Y-%m-%d').date()

	horas_registradas = timedelta()
	horas_contabilizadas = timedelta()

	dias = registros.annotate(
		data=F('created_at__date')
	).values('data').distinct()

	for dia in dias:
		entradas = registros.filter(tipo=0, created_at__date=dia['data'])
		saidas = registros.filter(tipo=1, created_at__date=dia['data'])

		_horas_registradas_dia = timedelta()
		for i, saida in enumerate(saidas):
			_horas_registradas_dia += saida.created_at - entradas[i].created_at
		
		horas_registradas += _horas_registradas_dia
		if dia["data"] > data_inicial_limitacao_ch:
			horas_contabilizadas += _horas_registradas_dia if _horas_registradas_dia <= ch_maxima_dia else ch_maxima_dia
		else:
			horas_contabilizadas += _horas_registradas_dia
			
	return horas_registradas, horas_contabilizadas

"""
Retorna o cálculo:
Total de horas a trabalhar - horas contabilizadas - horas abonadas
"""
def get_balanco_mes(vinculo, mes, ano, detalhado=False):
	calendario = FeriadosRioGrandeDoNorte()
	num_dias_mes = calendar.monthrange(ano, mes)[1]

	data_inicio = datetime.date(ano, mes, 1) 
	data_fim = datetime.date(ano, mes, num_dias_mes)

	num_dias_uteis_mes = calendario.count_working_days(data_inicio, data_fim)
	horas_trabalhar = num_dias_uteis_mes * (vinculo.carga_horaria_diaria or 0)
	horas_trabalhar = timedelta(hours=horas_trabalhar)

	frequencias = get_registros_bolsista(vinculo, data_inicio, data_fim)
	ausencias = get_ausencias_bolsista(vinculo, data_inicio, data_fim)

	horas_registradas, horas_contabilizadas = get_total_horas_registradas_contabilizadas(frequencias)
	horas_abonadas_periodo = get_horas_abonadas_periodo(ausencias, calendario, data_inicio, data_fim)

	saldo_mes = horas_trabalhar - horas_contabilizadas - horas_abonadas_periodo

	if detalhado:		
		return {
			'saldo_mes': saldo_mes,
			'horas_trabalhar': horas_trabalhar,
			'horas_registradas': horas_registradas,
			'horas_contabilizadas': horas_contabilizadas,
			'horas_abonadas_periodo': horas_abonadas_periodo,
		}

	return saldo_mes

def get_balanco_mes_anterior(vinculo, mes_atual, ano_atual):
	saldo_mes_anterior = timedelta()

	try:
		primeiro_dia_bolsa = get_primeiro_dia_bolsa(vinculo)
		primeiro_dia_calculo = datetime.date(primeiro_dia_bolsa.year, primeiro_dia_bolsa.month, 1)

		if primeiro_dia_calculo != datetime.date(ano_atual, mes_atual, 1):
			mes_ano_anterior = datetime.date(ano_atual, mes_atual, 1) - timedelta(days=1)
			saldo_mes_anterior = get_balanco_mes(vinculo, mes_ano_anterior.month, mes_ano_anterior.year)
	except Exception as e:
		print(e)
	finally:
		if saldo_mes_anterior.days < 0:
			saldo_mes_anterior = timedelta()

	return saldo_mes_anterior
	

def get_relatorio_mes(vinculo, mes, ano):

	registros = []
	horas_registradas_periodo = timedelta()
	horas_contabilizadas_periodo = timedelta()

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
		relatorio_dia['registros'] = registros_dia.order_by('pk')
		horas_registradas, horas_contabilizadas = get_total_horas_registradas_contabilizadas(registros_dia)
		relatorio_dia['horas_registradas'] = horas_registradas		
		relatorio_dia['horas_contabilizadas'] = horas_contabilizadas
		horas_registradas_periodo += horas_registradas		
		horas_contabilizadas_periodo += horas_contabilizadas

		relatorio_dia['is_util'] = not relatorio_dia['feriado'] \
								   and not relatorio_dia['ausencia'] \
								   and super(FeriadosRioGrandeDoNorte, calendario).is_working_day(dia)

		registros.append(relatorio_dia)

	dias_uteis = calendario.count_working_days(data_inicio, data_fim)		
	
	return  {'registros': registros,
			 'dias_uteis': dias_uteis,
			 'total_horas_trabalhar': timedelta(hours=vinculo.carga_horaria_diaria) * dias_uteis,
			 'horas_registradas_periodo': horas_registradas_periodo,
			 'horas_contabilizadas_periodo': horas_contabilizadas_periodo,
			 'horas_abonadas_periodo': get_horas_abonadas_periodo(ausencias, calendario, data_inicio, data_fim),
			 'saldo_mes_anterior': get_balanco_mes_anterior(vinculo, mes, ano),
		    }

def get_relatorio_mensal_setor(setor, mes, ano):
	dia = datetime.datetime.now().day

	bolsistas = setor.vinculos.filter(group__name='Bolsista', 
									  ativo=True, 
									  user__is_active=True, 
									  created_at__lte=datetime.date(ano, mes, dia))

	relatorio = []	
	for bolsista in bolsistas:

		balanco_mes = get_balanco_mes(bolsista, mes, ano, detalhado=True)
		balanco_mes_anterior = get_balanco_mes_anterior(bolsista, mes, ano)
		relatorio.append({
			'bolsista': bolsista,
			'balanco_mes_atual': balanco_mes,
			'balanco_mes_anterior': balanco_mes_anterior,
			'balanco_geral': balanco_mes['saldo_mes'] + balanco_mes_anterior,	
		})

	return relatorio
