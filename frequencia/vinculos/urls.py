from django.urls import path

from frequencia.vinculos import views

app_name = 'vinculos'
urlpatterns = [
	path('setores-coordenadorias/', views.setores_coordenadorias, name='setores_coordenadorias'),

	#Setores
	path('setor/novo/', views.setor_create, name='setor_create'),
	path('setor/editar/<int:pk>/', views.setor_edit, name='setor_edit'),

	#Coordenadorias
	path('coordenadoria/novo/', views.coordenadoria_create, name='coordenadoria_create'),
	path('coordenadoria/editar/<int:pk>/', views.coordenadoria_edit, name='coordenadoria_edit'),
]