from django.urls import path

from frequencia.justificativas import views

app_name = 'justificativas'
urlpatterns = [
	#Tipos de justificativa
	path('tipos/', views.tipo_justificativa, name='tipo_justificativa'),
	path('tipo/novo/', views.tipo_justificativa_create, name='tipo_justificativa_create'),
	path('tipo/editar/<int:pk>/', views.tipo_justificativa_edit, name='tipo_justificativa_edit'),
	path('tipo/remover/<int:pk>/', views.tipo_justificativa_remove, name='tipo_justificativa_remove'),

	#Justificativa de falta
	path('', views.justificativas, name='justificativas'),	
	path('novo/', views.justificativa_create, name='justificativa_create'),
	path('detalhes/<int:pk>/', views.justificativa_edit, name='justificativa_edit'),
	path('reabrir/<int:pk>/', views.justificativa_reabrir, name='justificativa_reabrir'),
	path('excluir/<int:pk>/', views.justificativa_excluir, name='justificativa_excluir'),
]