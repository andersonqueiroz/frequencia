from django.db import models
from django.utils import timezone

from frequencia.core.basemodel import basemodel
from frequencia.accounts.models import User

class Coordenadoria(basemodel):
	coordenadores = models.ManyToManyField(User, blank=True)
	
	nome = models.CharField('Nome', max_length=50)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Coordenadoria'  
		verbose_name_plural = 'Coordenadorias'

class Setor(basemodel):

	chefes = models.ManyToManyField(User, blank=True)
	coordenadoria = models.ForeignKey(Coordenadoria, verbose_name='Coordenadoria', related_name='setores')

	nome = models.CharField('Nome', max_length=50)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Setor'  
		verbose_name_plural = 'Setores'

class Bolsista(basemodel):

	TURNO_CHOICES = (
		(0, 'Matutino'),
		(1, 'Verpertino'),
		(2, 'Noturno')
	)

	user = models.ForeignKey(User, verbose_name='Usuário', related_name='bolsistas')
	setor = models.ForeignKey(Setor, verbose_name='Setor', related_name='bolsistas')

	carga_horaria_diaria = models.IntegerField()
	turno = models.IntegerField('Turno', choices=TURNO_CHOICES, default=0)
	vinculo_ativado = models.BooleanField(default=True)

	def __str__(self):
		return self.user.name

	class Meta:
		verbose_name = 'Bolsista'  
		verbose_name_plural = 'Bolsistas'

	@property
	def registros_dia(self):
		return self.registros.filter(created_at__date=timezone.now().date())
		