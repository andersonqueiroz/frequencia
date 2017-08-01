from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from django.conf import settings

from frequencia.accounts import views

urlpatterns = [
	url(r'^entrar/$', views.login, name='login'),
	url(r'^sair/$', logout, {'next_page': settings.LOGIN_URL}, name='logout'),
	
	url(r'^usuarios/$', views.accounts, name='accounts'),
	url(r'^usuario/novo/$', views.accounts_create, name='accounts_create'),
	url(r'^usuario/editar/(?P<pk>\d+)/$', views.accounts_edit, name='accounts_edit'),
	url(r'^usuario/editar_senha/$', views.edit_password, name='edit_password'),
]