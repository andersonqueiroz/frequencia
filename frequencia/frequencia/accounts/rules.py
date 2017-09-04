import rules

from frequencia.vinculos.models import Vinculo

@rules.predicate
def is_gestor(user):		
	return user.vinculos.filter(ativo=True, group__name='Gestor de unidade').exists()

@rules.predicate
def is_coordenador(user):		
	return user.vinculos.filter(ativo=True, group__name='Coordenador').exists()

@rules.predicate
def is_chefe(user):		
	return user.vinculos.filter(ativo=True, group__name='Chefe de setor').exists()

@rules.predicate
def is_bolsista(user):		
	return user.vinculos.filter(ativo=True, group__name='Bolsista').exists()

rules.add_perm('accounts.is_gestor', is_gestor)
rules.add_perm('accounts.is_coordenador', is_coordenador)
rules.add_perm('accounts.is_chefe', is_chefe)
rules.add_perm('accounts.is_bolsista', is_bolsista)

rules.add_perm('accounts.is_coordenador_chefe', is_chefe | is_coordenador)