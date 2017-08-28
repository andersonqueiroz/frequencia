from datetime import timedelta

from workalendar.america import Brazil
from workalendar.core import ChristianMixin

from .models import FeriadoCalendarioAcademico

class FeriadosRioGrandeDoNorte(Brazil):
	
	include_servidor_publico = True
	include_christmas = False
	
	FIXED_HOLIDAYS = (
		(1, 1, "Confraternização universal"),
		(1, 6, "Santos Reis"),
		(4, 21, "Tiradentes"),
        (5, 1, "Dia do trabalhador"),
        (9, 7, "Independência do Brasil"),
        (10, 3, "Mártires de Cunhau e Uruaçu"),
        (10, 12, "Nossa Senhora Aparecida"),
        (11, 2, "Finados"),
        (11, 15, "Proclamação da República"),
        (11, 21, "Nossa Senhora da Apresentação"),
        (12, 25, "Natal"),
        (12, 31, "Ano Novo"),
	)

	def holidays(self, year=None):
		holidays = super(FeriadosRioGrandeDoNorte, self).holidays(year)

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

		for holiday in FeriadoCalendarioAcademico.objects.filter(data__year=year).values_list('data', 'nome'):
			holidays.append(holiday)

		return sorted(holidays, key=lambda x: x[0])
		

	def is_working_day(self, day, extra_working_days=None, extra_holidays=None):
		not_holiday = super(FeriadosRioGrandeDoNorte, self).is_working_day(day, extra_working_days=None, extra_holidays=None)
		return not_holiday and not FeriadoCalendarioAcademico.objects.filter(data=day).exists()

		