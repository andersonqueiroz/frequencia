from datetime import timedelta

from django.db import models
from django.db.models import Q

from frequencia.core.basemodel import basemodel
from frequencia.vinculos.models import Vinculo
from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte

class TipoJustificativaFalta(basemodel):

	nome = models.CharField('Tipo', max_length=100)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Tipo de justificativa'
		verbose_name_plural = 'Tipos de justificativa'


class JustificativaFaltaManager(models.Manager):
	def buscar(self, query):
		if not query:
			return self
		return self.filter(Q(vinculo__user__name__contains=query) | 
						   Q(descricao__contains=query))

class JustificativaFalta(basemodel):

	objects = JustificativaFaltaManager()

	JUSTIFICATIVA_STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Indeferida'),
		(2, 'Deferida'),
	)

	tipo = models.ForeignKey(TipoJustificativaFalta, verbose_name='Tipo de justificativa', related_name='justificativas')
	vinculo = models.ForeignKey(Vinculo, verbose_name='Vínculo', related_name='justificativas')
	usuario_analise = models.ForeignKey(Vinculo, verbose_name='Analisado por', related_name='justificativas_homologadas', blank=True, null=True)

	status = models.IntegerField('Status da justificativa', choices=JUSTIFICATIVA_STATUS_CHOICES, default=0)
	descricao = models.TextField('Descrição')
	inicio = models.DateField('Data de início')
	termino = models.DateField('Data de término')

	parecer = models.TextField('Parecer da chefia', blank=True)
	horas_abonadas = models.DurationField('Tempo abonado', blank=True, null=True)

	@property
	def horas_sugeridas(self):
		calendario = FeriadosRioGrandeDoNorte()
		numero_dias_uteis = calendario.count_working_days(self.inicio, self.termino)
		horas_sugeridas = self.vinculo.carga_horaria_diaria * numero_dias_uteis
		return timedelta(hours=horas_sugeridas)


	def __str__(self):
		return '{0} - {1}'.format(self.vinculo.user.name, self.descricao)

	class Meta:
		verbose_name = 'Justificativa de falta'
		verbose_name_plural = 'Justificativas de falta'
