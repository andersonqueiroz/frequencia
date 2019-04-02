# Generated by Django 2.1.7 on 2019-04-02 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('justificativas', '0003_tipojustificativafalta_comprovante_obrigatorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='justificativafalta',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='justificativas', to='justificativas.TipoJustificativaFalta', verbose_name='Tipo de justificativa'),
        ),
        migrations.AlterField(
            model_name='justificativafalta',
            name='usuario_analise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='justificativas_homologadas', to='vinculos.Vinculo', verbose_name='Analisado por'),
        ),
        migrations.AlterField(
            model_name='tipojustificativafalta',
            name='comprovante_obrigatorio',
            field=models.BooleanField(blank=True, default=False, verbose_name='Comprovante obrigatório'),
        ),
    ]