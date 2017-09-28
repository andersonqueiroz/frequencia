import rules

from django.db.models import Q

from .models import Coordenadoria, Setor

@rules.predicate
def is_vinculo_chefe(user, vinculo):
	
	coordenadorias_user = Coordenadoria.objects.filter(vinculos__user=user)
	setores_user = Setor.objects.filter(Q(vinculos__user=user) | Q(coordenadoria__in=coordenadorias_user))

	return user.has_perm('accounts.is_coordenador_chefe') and vinculo.setor in setores_user

@rules.predicate
def is_vinculo_owner(user, vinculo):
	return vinculo.user == user

#Rules
rules.add_perm('vinculo.can_manage', is_vinculo_chefe)