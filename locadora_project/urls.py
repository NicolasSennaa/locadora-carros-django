"""
URL configuration for locadora_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from carros.views import home_dispatch_view, ClienteRegisterView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_dispatch_view, name='home'), 
    path('auth/', include('django.contrib.auth.urls')), 
    path('auth/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('auth/register/', ClienteRegisterView.as_view(), name='register'),
    path('carros/', include('carros.urls', namespace='carros')),
]