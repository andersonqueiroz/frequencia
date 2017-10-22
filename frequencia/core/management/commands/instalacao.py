"""
Documentação em https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):
	help = 'Realiza procedimentos iniciais do sistema'

	def handle(self, *args, **options):
		grupos = ['Bolsista', 'Chefe de setor', 'Coordenador', 'Gestor de unidade']

		try:
			for i in range(0, 4):	
				grupo, criado = Group.objects.get_or_create(name=grupos[i])
				if criado:
					self.stdout.write('Criado grupo %s' % grupo)
			self.stdout.write(self.style.SUCCESS('Grupos de usuários criados com sucesso!'))
		except:
			self.stdout.write(self.style.ERROR('Um erro ocorreu na criação dos grupos de usuários!'))