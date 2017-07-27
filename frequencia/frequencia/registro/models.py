from django.db import models

from frequencia.core.basemodel import basemodel
from frequencia.accounts.models import User

class Maquina(basemodel):
	
	nome = models.CharField('Nome', max_length=30)
	descricao = models.CharField('Nome', max_length=100, blank=True)
	ip = models.GenericIPAddressField('Endereço IP', unpack_ipv4=True)

	def __str__(self):
		return nome

	class Meta:
		verbose_name = 'Máquina'  
		verbose_name_plural = 'Máquinas'

class Frequencia(basemodel):

	TIPO_CHOICES = (
		(0, 'Entrada'),
		(1, 'Saída')
	)

	user = models.ForeignKey(User, verbose_name='Usuário', related_name='frequencias')
	maquina = models.ForeignKey(Maquina, verbose_name='Máquina', related_name='frequencias')

	observacao = models.TextField('Observação')
	tipo = models.IntegerField('Tipo', choices=TIPO_CHOICES, default=0)

	#def __str__(self):
	#	return None

	class Meta:
		verbose_name = 'Frequência'  
		verbose_name_plural = 'Frequências'


