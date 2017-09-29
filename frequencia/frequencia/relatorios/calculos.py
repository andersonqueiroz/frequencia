import datetime, calendar
from datetime import timedelta

from django.db.models import Q

from frequencia.registro.models import Frequencia
from frequencia.justificativas.models import JustificativaFalta
from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte

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

	entradas = registros.filter(tipo=0)
	saidas = registros.filter(tipo=1)

	for i, saida in enumerate(saidas):
		horas_trabalhadas += saida.created_at - entradas[i].created_at
	return horas_trabalhadas

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

	#Calculando horas abonadas no mês
	horas_abonadas_periodo = get_horas_abonadas_periodo(ausencias, calendario, data_inicio, data_fim)

	dias_uteis = calendario.count_working_days(data_inicio, data_fim)

	return  {'registros': registros,
			 'dias_uteis': dias_uteis,
			 'total_horas_trabalhar': timedelta(hours=4) * dias_uteis,
			 'horas_trabalhadas_periodo': horas_trabalhadas_periodo,
			 'horas_abonadas_periodo': horas_abonadas_periodo,
		    }