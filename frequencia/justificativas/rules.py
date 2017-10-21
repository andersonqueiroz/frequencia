import rules

from django.db.models import Q

from frequencia.vinculos.models import Coordenadoria, Setor
from frequencia.accounts.rules import is_gestor

#Predicates
@rules.predicate
def is_tipo_justificativa_manager(user):
	return user.has_perm('accounts.is_gestor')

@rules.predicate
def justificativa_creater(user):
	return user.has_perm('accounts.is_bolsista')

@rules.predicate
def is_justificativa_author(user, justificativa):
	return justificativa.vinculo in user.vinculos.all()

@rules.predicate
def is_justificativa_chefe(user, justificativa):
	
	coordenadorias_user = Coordenadoria.objects.filter(vinculos__user=user)
	user_setores = Setor.objects.filter(Q(vinculos__user=user) | Q(coordenadoria__in=coordenadorias_user))

	return user.has_perm('accounts.is_coordenador_chefe') and justificativa.vinculo.setor in user_setores

#Custom predicates
justificativa_viewer = is_justificativa_author | is_justificativa_chefe | is_gestor

#Rules
rules.add_perm('tipo_justificativa.can_manage', is_tipo_justificativa_manager)

rules.add_perm('justificativa.can_create', justificativa_creater)
rules.add_perm('justificativa.can_view', justificativa_viewer)
rules.add_perm('justificativa.can_analyse', is_justificativa_chefe)