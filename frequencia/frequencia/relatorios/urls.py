from django.conf.urls import url, include

from frequencia.relatorios import views

urlpatterns = [
	#Tipos de justificativa
	url(r'^$', views.busca_relatorio, name='busca_relatorio'),
	url(r'^mensal/$', views.relatorio_mensal, name='relatorio_mensal'),
	url(r'^mensal/(?P<pk>\d+)/$', views.relatorio_mensal, name='relatorio_mensal'),
	url(r'^geral/$', views.listagem_geral, name='listagem_geral'),
	url(r'^setor/(?P<pk>\d+)/$', views.relatorio_setor, name='relatorio_setor'),
]
