from django.conf.urls import url, include

from frequencia.calendario import views

urlpatterns = [
	#Feriados
	url(r'^$', views.feriados, name='feriados'),
	url(r'^(?P<ano>\d+)/$', views.feriados, name='feriados'),
	url(r'^feriado/novo/$', views.feriado_create, name='feriado_create'),
	url(r'^feriado/remover/(?P<pk>\d+)/$', views.feriado_remove, name='feriado_remove'),
]