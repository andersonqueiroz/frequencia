import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings
from django.utils import timezone

from frequencia.core.basemodel import basemodel

class User(basemodel, AbstractBaseUser, PermissionsMixin):

	username = models.CharField(
		'Login', max_length=30, unique=True,
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
			'O nome de usuário so pode conter letras, digitos ou os seguintes caracteres: @/./+/-/_', 'invalid')]
	)
	email = models.EmailField('E-mail', unique=True)
	name = models.CharField('Nome', max_length=100, blank=True)
	cpf = models.CharField('CPF', max_length=15)
	is_active = models.BooleanField('Está ativo', blank=True, default=True)
	is_staff = models.BooleanField('Acesso ao admin do projeto', blank=True, default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.name or self.username

	def get_short_name(self):
		return self.username

	def get_full_name(self):
		return str(self)

	class Meta:
		verbose_name='Usuário'
		verbose_name_plural='Usuários'

	@property
	def ultima_frequencia_dia(self):
		ultimo = self.frequencias.filter(created_at__date=timezone.now().date()).last()
		return ultimo