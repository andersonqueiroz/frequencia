from django.conf.urls import url, include

from frequencia.justificativas import views

urlpatterns = [
	#Tipos de justificativa
	url(r'^tipos/$', views.tipo_justificativa, name='tipo_justificativa'),
	url(r'^tipo/novo/$', views.tipo_justificativa_create, name='tipo_justificativa_create'),
	url(r'^tipo/editar/(?P<pk>\d+)/$', views.tipo_justificativa_edit, name='tipo_justificativa_edit'),
	url(r'^tipo/remover/(?P<pk>\d+)/$', views.tipo_justificativa_remove, name='tipo_justificativa_remove'),

	#Justificativa de falta
	url(r'^$', views.justificativas, name='justificativas'),	
	url(r'^novo/$', views.justificativa_create, name='justificativa_create'),
	url(r'^detalhes/(?P<pk>\d+)/$', views.justificativa_edit, name='justificativa_edit'),
]