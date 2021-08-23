from django.db import models

class basemodel(models.Model):

	id = models.AutoField(primary_key=True)
	created_at = models.DateTimeField('Registrado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	class Meta:
		abstract = True