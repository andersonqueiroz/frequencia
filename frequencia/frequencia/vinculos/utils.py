from django.db.models import Q

from frequencia.vinculos.models import Vinculo, Coordenadoria, Setor

def get_bolsistas(user):
	bolsistas = Vinculo.objects.filter(group__name='Bolsista', ativo=True, user__is_active=True).order_by('setor')

	if user.has_perm('accounts.is_gestor'):
		return bolsistas.all()

	elif user.has_perm('accounts.is_coordenador_chefe'):
		vinculos = user.vinculos.filter(ativo=True)
		vinculos = vinculos.filter(Q(group__name='Coordenador') | Q(group__name='Chefe de setor'))

		coordenadorias = Coordenadoria.objects.filter(vinculos__in=vinculos)
		setores = Setor.objects.filter(Q(coordenadoria__in=coordenadorias) | Q(vinculos__in=vinculos))

		bolsistas = bolsistas.filter(setor__in=setores)
	else:
		bolsistas = None

	return bolsistas