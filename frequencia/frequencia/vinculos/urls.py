from django.conf.urls import url, include

from frequencia.vinculos import views

urlpatterns = [
	url(r'^setores-coordenadorias/$', views.setores_coordenadorias, name='setores_coordenadorias'),

	#Setores
	url(r'^setor/novo/$', views.setor_create, name='setor_create'),
	url(r'^setor/editar/(?P<pk>\d+)/$', views.setor_edit, name='setor_edit'),

	#Coordenadorias
	url(r'^coordenadoria/novo/$', views.coordenadoria_create, name='coordenadoria_create'),
	url(r'^coordenadoria/editar/(?P<pk>\d+)/$', views.coordenadoria_edit, name='coordenadoria_edit'),
]