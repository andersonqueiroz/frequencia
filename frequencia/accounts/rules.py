import rules

from frequencia.vinculos.models import Vinculo

@rules.predicate
def is_gestor(user):	
	try:	
		return user.vinculos.filter(ativo=True, group__name='Gestor de unidade').exists()
	except:
		return None

@rules.predicate
def is_coordenador(user):	
	try:	
		return user.vinculos.filter(ativo=True, group__name='Coordenador').exists()
	except:
		return None

@rules.predicate
def is_chefe(user):	
	try:	
		return user.vinculos.filter(ativo=True, group__name='Chefe de setor').exists()
	except:
		return None

@rules.predicate
def is_bolsista(user):	
	try:	
		return user.vinculos.filter(ativo=True, group__name='Bolsista').exists()
	except:
		return None
				
is_servidor = is_chefe | is_coordenador | is_gestor

rules.add_perm('accounts.is_gestor', is_gestor)
rules.add_perm('accounts.is_coordenador', is_coordenador)
rules.add_perm('accounts.is_chefe', is_chefe)
rules.add_perm('accounts.is_bolsista', is_bolsista)

rules.add_perm('accounts.is_coordenador_chefe', is_chefe | is_coordenador)
rules.add_perm('accounts.is_gestor_coordenador', is_gestor | is_coordenador)
rules.add_perm('accounts.is_servidor', is_servidor)