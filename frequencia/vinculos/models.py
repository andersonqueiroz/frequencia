from datetime import datetime

from django.db import models
from django.contrib.auth.models import Group

from django import template

from frequencia.core.basemodel import basemodel
from frequencia.accounts.models import User


class Coordenadoria(basemodel):
	
	nome = models.CharField('Nome', max_length=50)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Coordenadoria'  
		verbose_name_plural = 'Coordenadorias'

class Setor(basemodel):
	
	coordenadoria = models.ForeignKey(Coordenadoria, verbose_name='Coordenadoria', related_name='setores', on_delete=models.PROTECT)

	nome = models.CharField('Nome', max_length=50)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Setor'  
		verbose_name_plural = 'Setores'

class Vinculo(basemodel):

	TURNO_CHOICES = (
		(None, ''),
		(0, 'Matutino'),
		(1, 'Vespertino'),
		(2, 'Noturno')
	)

	group = models.ForeignKey(Group, verbose_name='Papel', related_name='vinculos', on_delete=models.PROTECT)
	user = models.ForeignKey(User, verbose_name='Usuário', related_name='vinculos', on_delete=models.PROTECT)
	setor = models.ForeignKey(Setor, verbose_name='Setor', related_name='vinculos', null=True, blank=True, on_delete=models.PROTECT)
	coordenadoria = models.ForeignKey(Coordenadoria, verbose_name='Coordenadoria', related_name='vinculos', on_delete=models.PROTECT, null=True, blank=True)

	carga_horaria_diaria = models.IntegerField(null=True, verbose_name='Carga horária diária', blank=True)
	turno = models.IntegerField('Turno', choices=TURNO_CHOICES, blank=True, null=True)
	ativo = models.BooleanField(verbose_name='Vínculo ativo', default=True)
	inicio_vigencia = models.DateField(verbose_name='Data de início da bolsa', blank=True, null=True)
	termino_vigencia = models.DateField(verbose_name='Data de término da bolsa', blank=True, null=True)

	def __str__(self):
		return '{0} - {1}'.format((self.user.name or self.user.username), (self.setor or self.coordenadoria))

	class Meta:
		verbose_name = 'Vínculo'  
		verbose_name_plural = 'Vínculos'

	def registros_dia(self, dia=None):
		dia = dia or datetime.now().date()
		return self.registros.filter(created_at__date=dia)

	def bolsa_expirada(self):
		return self.termino_vigencia < datetime.now().date()