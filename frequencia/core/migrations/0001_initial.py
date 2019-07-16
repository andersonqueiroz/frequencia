from django.db import migrations

from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    grupos = ['Bolsista', 'Chefe de setor', 'Coordenador', 'Gestor de unidade']

    for grupo in grupos:
        novo_grupo, _ = Group.objects.get_or_create(name=grupo)

class Migration(migrations.Migration):
    
    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_code=migrations.RunPython.noop),
    ]
