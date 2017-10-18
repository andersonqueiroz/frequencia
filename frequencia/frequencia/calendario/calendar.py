import calendar, datetime
from datetime import timedelta

from workalendar.america import Brazil
from workalendar.core import ChristianMixin

from .models import FeriadoCalendarioAcademico

class FeriadosRioGrandeDoNorte(Brazil):

	include_servidor_publico = True
	include_corpus_christi = True
	include_christmas = False
	include_sao_joao = True

	FIXED_HOLIDAYS = (
		(1, 1, "Confraternização universal"),
		(1, 6, "Santos Reis"),
		(4, 21, "Tiradentes"),
        (5, 1, "Dia do trabalhador"),
        (9, 7, "Independência do Brasil"),
        (10, 3, "Mártires de Cunhau e Uruaçu"),
        (10, 12, "Padroeira do Brasil"),
        (11, 2, "Finados"),
        (11, 15, "Proclamação da República"),
        (11, 21, "Padroeira de Natal"),
        (12, 25, "Natal"),
        (12, 31, "Ano Novo"),
	)

	def get_calendar_holidays(self, year, with_id=False):
		holidays = super(FeriadosRioGrandeDoNorte, self).get_calendar_holidays(year)

		carnaval_terca = self.get_carnaval(year)
		carnaval_segunda = carnaval_terca - timedelta(days=1)
		cinzas = carnaval_terca + timedelta(days=1)

		holidays.append((carnaval_segunda, "Carnaval"))
		holidays.append((carnaval_terca, "Carnaval"))
		holidays.append((cinzas, "Cinzas"))

		holidays.append((self.get_holy_thursday(year), "Quinta-feira Santa"))
		holidays.append((self.get_good_friday(year), "Sexta-feira da Paixão"))
		holidays.append((self.get_easter_saturday(year), "Sábado de Aleluia"))
		holidays.append((self.get_easter_sunday(year), "Páscoa"))

		if with_id:
			db_holidays = FeriadoCalendarioAcademico.objects.filter(data__year=year).values_list('data', 'nome', 'id')
		else:
			db_holidays = FeriadoCalendarioAcademico.objects.filter(data__year=year).values_list('data', 'nome')

		for holiday in db_holidays:
			holidays.append(holiday)

		return sorted(holidays, key=lambda x: x[0])

	def is_working_day(self, day, extra_working_days=None, extra_holidays=None):
		not_holiday = super(FeriadosRioGrandeDoNorte, self).is_working_day(day, extra_working_days, extra_holidays)
		return not_holiday and not FeriadoCalendarioAcademico.objects.filter(data=day).exists()

	def count_working_days(self, start_date, end_date):
		workday_count = 0
		feriados = FeriadoCalendarioAcademico.objects.filter(data__lte=start_date, data__gte=end_date)

		day_count = (end_date - start_date).days + 1
		for day in (start_date + timedelta(n) for n in range(day_count)):
			workday_count += 1 if super(FeriadosRioGrandeDoNorte, self).is_working_day(day) and not feriados.filter(data=day).exists() else 0
		return workday_count

	def count_working_days_month(self, month, year):
		days_count = calendar.monthrange(year, month)[1]
		start_date = datetime.date(year, month, 1)
		end_date = datetime.date(year, month, days_count)

		return self.count_working_days(start_date, end_date)
