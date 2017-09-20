"""frequencia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('frequencia.core.urls', namespace='core')),
    url(r'^registro/', include('frequencia.registro.urls', namespace='registro')),
    url(r'^vinculos/', include('frequencia.vinculos.urls', namespace='vinculos')),
    url(r'^calendario/', include('frequencia.calendario.urls', namespace='calendario')),
	url(r'^justificativas/', include('frequencia.justificativas.urls', namespace='justificativas')),
	url(r'^relatorios/', include('frequencia.relatorios.urls', namespace='relatorios')),

    url(r'^admin/', admin.site.urls),
    url(r'^conta/', include('frequencia.accounts.urls', namespace='accounts')),
]
