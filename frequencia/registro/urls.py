from django.urls import path

from frequencia.registro import views

app_name = 'registro'
urlpatterns = [
	#Máquinas
	path('maquinas/', views.maquinas, name='maquinas'),
	path('maquina/novo/', views.maquina_create, name='maquina_create'),
	path('maquina/editar/<int:pk>/', views.maquina_edit, name='maquina_edit'),
	path('maquina/remover/<int:pk>/', views.maquina_remove, name='maquina_remove'),

	#Registro
	path('', views.registro, name='registro'),
	path('registros_dia/', views.registros_dia, {'Bolsista': None}, name='registros_dia'),
]
