# Generated by Django 3.2.14 on 2022-08-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinculos', '0003_auto_20190402_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordenadoria',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='setor',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vinculo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vinculo',
            name='turno',
            field=models.IntegerField(blank=True, choices=[(None, ''), (0, 'Matutino'), (1, 'Vespertino'), (2, 'Noturno')], null=True, verbose_name='Turno'),
        ),
    ]
