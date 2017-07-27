from django.db import models

class basemodel(models.Model):

	created_at = models.DateTimeField('Registrado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	class Meta:
		abstract = True