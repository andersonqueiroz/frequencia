from django.db import models

from frequencia.core.basemodel import basemodel
from frequencia.accounts.models import User
from frequencia.vinculos.models import Vinculo

class Maquina(basemodel):
	
	nome = models.CharField('Nome', max_length=30)
	descricao = models.CharField('Descricao', max_length=100, blank=True)
	ip = models.GenericIPAddressField('Endereço IP', unpack_ipv4=True, unique=True)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Máquina'  
		verbose_name_plural = 'Máquinas'

class Frequencia(basemodel):

	TIPO_CHOICES = (
		(0, 'Entrada'),
		(1, 'Saída')
	)

	bolsista = models.ForeignKey(Vinculo, verbose_name='Bolsista', related_name='registros')
	maquina = models.ForeignKey(Maquina, verbose_name='Máquina', related_name='registros')

	observacao = models.TextField('Observação', blank=True)
	tipo = models.IntegerField('Tipo', choices=TIPO_CHOICES, default=0)

	def __str__(self):
		return "{0}/{1} em {2}".format(self.bolsista, self.get_tipo_display(), self.created_at)

	class Meta:
		verbose_name = 'Frequência'  
		verbose_name_plural = 'Frequências'	