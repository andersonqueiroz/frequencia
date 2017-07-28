from django.conf.urls import url, include

from frequencia.registro import views

urlpatterns = [
	url(r'^$', views.registro, name='registro'),
	url(r'^registrar/$', views.registrar_frequencia, name='registrar_frequencia'),
]