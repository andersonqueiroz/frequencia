import rules

from frequencia.vinculos.utils import get_setores

@rules.predicate
def is_vinculo_chefe(user, vinculo):
	try:	
		setores_user = get_setores(user)
		return user.has_perm('accounts.is_coordenador_chefe') and vinculo.setor in setores_user
	except:
		return None

@rules.predicate
def is_vinculo_owner(user, vinculo):
	try:
		return vinculo.user == user
	except:
		return None

@rules.predicate
def is_setor_chefe(user, setor):
	try:	
		setores_user = get_setores(user)
		return user.has_perm('accounts.is_servidor') and setor in setores_user
	except:
		return None

#Rules
rules.add_perm('vinculo.can_manage', is_vinculo_chefe)