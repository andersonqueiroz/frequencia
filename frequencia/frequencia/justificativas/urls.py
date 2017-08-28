from django.conf.urls import url, include

from frequencia.justificativas import views

urlpatterns = [
	#Tipos de justificativa
	url(r'^tipos/$', views.tipo_justificativa, name='tipo_justificativa'),
	url(r'^tipo/novo/$', views.tipo_justificativa_create, name='tipo_justificativa_create'),
	url(r'^tipo/editar/(?P<pk>\d+)/$', views.tipo_justificativa_edit, name='tipo_justificativa_edit'),
	url(r'^tipo/remover/(?P<pk>\d+)/$', views.tipo_justificativa_remove, name='tipo_justificativa_remove'),
]