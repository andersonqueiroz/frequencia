from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path

from frequencia.accounts import views

app_name = 'accounts'
urlpatterns = [
	path('entrar/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('sair/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_URL), name='logout'),
	
	path('usuarios/', views.accounts, name='accounts'),
	path('usuario/novo/', views.accounts_create, name='accounts_create'),
	path('usuario/editar/<int:pk>/', views.accounts_edit, name='accounts_edit'),
	path('usuario/editar_senha/', views.edit_password, name='edit_password'),
	path('usuario/redefinir_senha/<int:pk>/', views.reset_password, name='reset_password'),
]