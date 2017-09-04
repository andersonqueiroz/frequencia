"""
Documentação em https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
"""

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Realiza procedimentos iniciais do sistema'

    def handle(self, *args, **options):        

        self.stdout.write(self.style.SUCCESS('Procedimentos iniciais realizados com sucesso!'))