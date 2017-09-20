import datetime, calendar
from datetime import timedelta

from django.db.models import Q

from frequencia.registro.models import Frequencia
from frequencia.justificativas.models import JustificativaFalta
from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte

def get_registros_bolsista(user, data_inicio, data_fim):
	return Frequencia.objects.filter(bolsista__user=user, created_at__date__gte=data_inicio, created_at__date__lte=data_fim)

def get_ausencias_bolsista(user, data_inicio, data_fim):
	justificativas = JustificativaFalta.objects.filter(vinculo__user=user, status=2)
	return justificativas.filter(Q(inicio__month=data_inicio.month, 
											 inicio__year=data_inicio.year)	|
										   Q(termino__month=data_fim.month,
										   	 termino__year=data_fim.year))

def get_total_horas_trabalhadas(registros):
	horas_trabalhadas = timedelta()

	entradas = registros.filter(tipo=0)
	saidas = registros.filter(tipo=1)

	for i, saida in enumerate(saidas):
		horas_trabalhadas += saida.created_at - entradas[i].created_at
	return horas_trabalhadas

def get_relatorio_mes(user, mes, ano):	

	registros = []
	horas_trabalhadas_mes = timedelta()

	calendario = FeriadosRioGrandeDoNorte()
	feriados = calendario.holidays(ano)

	numero_dias = calendar.monthrange(ano, mes)[1]
	data_inicio = datetime.date(ano, mes, 1)
	data_fim = datetime.date(ano, mes, numero_dias)

	frequencias = get_registros_bolsista(user, data_inicio, data_fim)
	ausencias = get_ausencias_bolsista(user, data_inicio, data_fim)

	for dia in range(1, numero_dias):
		dia = datetime.date(ano, mes, dia)
		relatorio_dia = {'dia' : dia}

		feriado = [feriado for feriado in feriados if feriado[0] == dia]
		relatorio_dia['feriado'] = feriado[0] if feriado else False

		ausencia = ausencias.filter(inicio__lte=dia, termino__gte=dia)
		relatorio_dia['ausencia'] = ausencia.exists()

		registros_dia = frequencias.filter(created_at__date=dia)
		relatorio_dia['registros'] = registros_dia
		horas_trabalhadas = get_total_horas_trabalhadas(registros_dia)
		relatorio_dia['horas_trabalhadas'] = horas_trabalhadas
		horas_trabalhadas_mes += horas_trabalhadas

		registros.append(relatorio_dia)

	#Calculando horas abonadas no mês
	horas_abonadas_mes = timedelta()
	for ausencia in ausencias:
		total_dias_ausencia = calendario.count_working_days(ausencia.inicio, ausencia.termino)
		total_dias_ausencia_mes = calendario.count_working_days(ausencia.inicio, ausencia.termino if ausencia.termino <= data_fim else data_fim)		
		horas_abonadas_mes +=  (ausencia.horas_abonadas / total_dias_ausencia) * total_dias_ausencia	
		

	relatorio = {'registros': registros,
				 'dias_uteis': calendario.count_working_days(data_inicio, data_fim),
				 'horas_trabalhadas_mes': horas_trabalhadas_mes,
				 'horas_abonadas_mes': horas_abonadas_mes,
				}

	return relatorio
