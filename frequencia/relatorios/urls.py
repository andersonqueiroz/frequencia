from django.urls import path

from frequencia.relatorios import views

app_name = 'relatorios'
urlpatterns = [
	#Tipos de justificativa
	path('', views.busca_relatorio, name='busca_relatorio'),
	path('mensal/', views.relatorio_mensal, name='relatorio_mensal'),
	path('mensal/<int:pk>/', views.relatorio_mensal, name='relatorio_mensal'),
	path('geral/', views.listagem_geral, name='listagem_geral'),
	path('setor/', views.busca_setor, name='busca_setor'),
	path('setor/<int:pk>/', views.relatorio_setor, name='relatorio_setor'),
]
