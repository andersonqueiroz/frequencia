# Generated by Django 3.2.14 on 2022-08-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feriadocalendarioacademico',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]