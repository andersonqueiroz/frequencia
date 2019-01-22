from django.urls import path

from frequencia.core import views

app_name = 'core'
urlpatterns = [
	path('', views.index, name='index'),
	path('home/', views.home, name='home'),
	path('nova-mensagem/', views.nova_mensagem, name='nova_mensagem'),
]