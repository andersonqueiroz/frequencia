import datetime, calendar

from datetime import timedelta

from frequencia.registro.models import Frequencia
from frequencia.justificativas.models import JustificativaFalta
from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte

def get_registros_bolsista(user, data_inicio, data_fim):
	return Frequencia.objects.filter(bolsista__user=user, created_at__date__gte=data_inicio, created_at__date__lte=data_fim)

def get_ausencias_bolsista(user, data_inicio, data_fim):
	return JustificativaFalta.objects.filter(vinculo__user=user, inicio__gte=data_inicio, termino__lte=data_fim)

def get_total_horas_trabalhadas(registros):
	horas_trabalhadas = timedelta()

	entradas = registros.filter(tipo=0)
	saidas = registros.filter(tipo=1)

	for i, saida in enumerate(saidas):
		horas_trabalhadas += saida.created_at - entradas[i].created_at
	return horas_trabalhadas

def get_relatorio_mes(user, mes, ano):
	relatorio = []
	calendario = FeriadosRioGrandeDoNorte()
	feriados = calendario.holidays(ano)

	_, numero_dias = calendar.monthrange(ano, mes)

	frequencias = get_registros_bolsista(user, datetime.date(ano, mes, 1), datetime.date(ano, mes, numero_dias))
	ausencias = get_ausencias_bolsista(user, datetime.date(ano, mes, 1), datetime.date(ano, mes, numero_dias))

	for dia in range(1, numero_dias + 1):
		dia = datetime.date(ano, mes, dia)
		relatorio_dia = {'dia' : dia}

		feriado = [feriado for feriado in feriados if feriado[0] == dia]
		relatorio_dia['feriado'] = feriado[0] if feriado else False

		ausencia = [ausencia for ausencia in ausencias if ausencia.inicio <= dia and ausencia.termino >= dia]
		relatorio_dia['ausencia'] = ausencia[0] if ausencia else False

		registros_dia = frequencias.filter(created_at__date=dia)
		relatorio_dia['registros'] = registros_dia
		relatorio_dia['horas_trabalhadas'] = get_total_horas_trabalhadas(registros_dia)

		relatorio.append(relatorio_dia)

	return relatorio