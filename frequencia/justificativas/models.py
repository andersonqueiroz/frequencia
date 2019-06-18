from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.conf import settings

from frequencia.core.basemodel import basemodel
from frequencia.core.mail import send_mail_template
from frequencia.vinculos.models import Vinculo
from frequencia.calendario.calendar import FeriadosRioGrandeDoNorte

from .validators import validate_file_extension

class TipoJustificativaFalta(basemodel):

	nome = models.CharField('Tipo', max_length=100)
	comprovante_obrigatorio = models.BooleanField('Comprovante obrigatório', blank=True, default=False)

	def __str__(self):
		return self.nome

	class Meta:
		verbose_name = 'Tipo de justificativa'
		verbose_name_plural = 'Tipos de justificativa'


class JustificativaFaltaManager(models.Manager):
	def buscar(self, query):
		if not query:
			return self
		return self.filter(Q(vinculo__user__name__icontains=query) | 
						   Q(descricao__icontains=query))

class JustificativaFalta(basemodel):

	objects = JustificativaFaltaManager()

	JUSTIFICATIVA_STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Indeferida'),
		(2, 'Deferida'),
	)

	tipo = models.ForeignKey(TipoJustificativaFalta, verbose_name='Tipo de justificativa', related_name='justificativas', on_delete=models.PROTECT)
	vinculo = models.ForeignKey(Vinculo, verbose_name='Vínculo', related_name='justificativas', on_delete=models.CASCADE)
	usuario_analise = models.ForeignKey(Vinculo, verbose_name='Analisado por', related_name='justificativas_homologadas', on_delete=models.PROTECT, blank=True, null=True)

	status = models.IntegerField('Status da justificativa', choices=JUSTIFICATIVA_STATUS_CHOICES, default=0)
	descricao = models.TextField('Descrição')
	inicio = models.DateField('Data de início')
	termino = models.DateField('Data de término')
	comprovante = models.FileField('Comprovante', blank=True, upload_to='anexos_justificativas/', validators=[validate_file_extension])

	parecer = models.TextField('Parecer da chefia', blank=True)
	horas_abonadas = models.DurationField('Tempo abonado', blank=True, null=True)

	@property
	def horas_sugeridas(self):
		calendario = FeriadosRioGrandeDoNorte()
		numero_dias_uteis = calendario.count_working_days(self.inicio, self.termino)
		horas_sugeridas = self.vinculo.carga_horaria_diaria * numero_dias_uteis

		if not horas_sugeridas:
			return timedelta()

		horas_sugeridas = timedelta(hours=horas_sugeridas)
		from frequencia.relatorios.calculos import get_total_horas_registradas_contabilizadas
		registros = self.vinculo.registros.filter(created_at__date__gte=self.inicio, 
												  created_at__date__lte=self.termino)
		horas_registradas, horas_contabilizadas = get_total_horas_registradas_contabilizadas(registros)

		horas_sugeridas = horas_sugeridas - horas_registradas
		return horas_sugeridas if horas_sugeridas.days >= 0 else timedelta()

	def __str__(self):
		return '{0} - {1}'.format(self.vinculo.user, self.descricao)

	class Meta:
		verbose_name = 'Justificativa de falta'
		verbose_name_plural = 'Justificativas de falta'


def post_save_justificativa(instance, created, **kwargs):
	if created:
		subject = 'Nova justificativa de falta cadastrada'
		context = { 'justificativa' : instance	, 'base_url': settings.BASE_URL_SERVER }
		template_name = 'justificativas/justificativa_mail.html'
		
		chefes = instance.vinculo.setor.vinculos.filter(group__name='Chefe de setor', ativo=True, user__is_active=True)		
		for chefe in chefes:
			recipient_list = [chefe.user.email]
			try:				
				send_mail_template(subject=subject, template_name=template_name, context=context, recipient_list=recipient_list)
			except:
				pass

models.signals.post_save.connect(
	post_save_justificativa, 
	sender=JustificativaFalta,
	dispatch_uid='post_save_justificativa'
)