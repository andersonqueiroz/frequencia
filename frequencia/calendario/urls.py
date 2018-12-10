from django.urls import path

from frequencia.calendario import views

app_name = 'calendario'
urlpatterns = [
	#Feriados
	path('', views.feriados, name='feriados'),
	path('<int:ano>', views.feriados, name='feriados'),
	path('feriado/novo/', views.feriado_create, name='feriado_create'),
	path('feriado/remover/<int:pk>', views.feriado_remove, name='feriado_remove'),
]