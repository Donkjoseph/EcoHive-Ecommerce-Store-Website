"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from django.contrib import admin
from ecohive import views
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.index, name='index'),
    path('register.html', views.register, name='register'),
    path('sellerreg.html', views.sellerreg, name='sellerreg'),
    path('login.html', views.login, name='login'),
    path('index.html', views.index, name='index'),
    path('dashlegal.html', views.dashlegal, name='dashlegal'),
    path('dashseller.html', views.dashseller, name='dashseller'),
    path('logout/', views.loggout, name='loggout'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_username/', views.check_username, name='check_username'),
    path("accounts/", include("allauth.urls")),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]
