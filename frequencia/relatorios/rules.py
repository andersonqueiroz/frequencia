import rules

from frequencia.vinculos.rules import is_vinculo_chefe, is_vinculo_owner, is_setor_chefe
from frequencia.accounts.rules import is_gestor

#Rules
rules.add_perm('relatorio.can_view', is_gestor | is_vinculo_chefe | is_vinculo_owner)
rules.add_perm('relatorio.can_view_setor', is_setor_chefe)