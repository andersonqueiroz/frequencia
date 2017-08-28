from django.conf.urls import url, include

from frequencia.calendario import views

urlpatterns = [
	#Feriados
	url(r'^feriados/$', views.feriados, name='feriados'),
	url(r'^feriados/(?P<ano>\d+)/$', views.feriados, name='feriados'),
	#url(r'^feriado/novo/$', views.feriado_create, name='feriado_create'),
	#url(r'^feriado/editar/(?P<pk>\d+)/$', views.feriado_edit, name='feriado_edit'),
]