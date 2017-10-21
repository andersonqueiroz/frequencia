import rules

from frequencia.vinculos.rules import is_vinculo_chefe, is_vinculo_owner
from frequencia.accounts.rules import is_gestor

#Rules
rules.add_perm('relatorio.can_view', is_gestor | is_vinculo_chefe | is_vinculo_owner)