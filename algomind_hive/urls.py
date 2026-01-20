"""
URL configuration for algomind_hive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-main/', views.dashboard, name='dashboard-main'),
    path('hive-observation/', views.hive_management, name='hive-observation'),
    path('hive-management/', views.hive_management, name='hive-management'),
    path('climate-data/', views.climate_data, name='climate-data'),
    path('ai-predictions/', views.ai_predictions, name='ai-predictions'),
    path('predictions-recommendations/', views.ai_predictions, name='predictions-recommendations'),
    path('climate-environment/', views.climate_data, name='climate-environment'),
    path('market-price/', views.ai_predictions, name='market-price'),
    path('admin/', admin.site.urls),
    path('api/climate/', include('climate.urls')),
    path('api/hives/', include('hives.urls')),
    path('api/ai/', include('ai_engine.urls')),
]
