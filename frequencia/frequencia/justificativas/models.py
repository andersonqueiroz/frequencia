from django.db import models

from frequencia.core.basemodel import basemodel
from frequencia.vinculos.models import Vinculo

class TipoJustificativaFalta(basemodel):

	nome = models.CharField('Tipo', max_length=100)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Tipo de justificativa'  
		verbose_name_plural = 'Tipos de justificativa'


class JustificativaFalta(basemodel):

	JUSTIFICATIVA_STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Indeferida'),
		(2, 'Deferida'),
	)

	tipo = models.ForeignKey(TipoJustificativaFalta, verbose_name='Tipo de justificativa', related_name='justificativas')
	vinculo = models.ForeignKey(Vinculo, verbose_name='Vínculo', related_name='justificativas')

	status = models.IntegerField('Status da justificativa', choices=JUSTIFICATIVA_STATUS_CHOICES, default=0)
	descricao = models.TextField('Descrição')
	inicio = models.DateField('Data de início')
	termino = models.DateField('Data de término')

	def __str__(self):
		return '{0} - {1}'.format(self.vinculo.user.name, self.descricao)

	class Meta:
		verbose_name = 'Justificativa de falta'  
		verbose_name_plural = 'Justificativas de falta'

