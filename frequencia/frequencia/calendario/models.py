from django.db import models

from frequencia.core.basemodel import basemodel

class FeriadoCalendarioAcademico(basemodel):

	nome = models.CharField('Nome', max_length=100)
	data = models.DateField('Data')

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Feriado'  
		verbose_name_plural = 'Feriados'