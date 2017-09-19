from django.conf.urls import url, include

from frequencia.relatorios import views

urlpatterns = [
	#Tipos de justificativa
	url(r'^mensal/$', views.relatorio_mensal, name='relatorio_mensal'),
]
