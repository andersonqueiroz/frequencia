from django.conf.urls import url, include

from frequencia.registro import views

urlpatterns = [
	#Máquinas
	url(r'^maquinas/$', views.maquinas, name='maquinas'),
	url(r'^maquina/novo/$', views.maquina_create, name='maquina_create'),
	url(r'^maquina/editar/(?P<pk>\d+)/$', views.maquina_edit, name='maquina_edit'),
	url(r'^maquina/remover/(?P<pk>\d+)/$', views.maquina_remove, name='maquina_remove'),

	#Registro
	url(r'^$', views.registro, name='registro'),
	url(r'^registros_dia/$', views.registros_dia, {'Bolsista': None}, name='registros_dia'),
]
