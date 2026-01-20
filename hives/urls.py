from django.urls import path
from . import views

urlpatterns = [
    path('hives/', views.hive_list, name='hive-list'),
    path('hive-activities/', views.hive_activity_list, name='hive-activities-list'),
    path('colony-health-predictions/', views.colony_health_predictions, name='colony-health-predictions-list'),
    path('create-hive/', views.create_hive, name='create-hive'),
    path('create-hive-activity/', views.create_hive_activity, name='create-hive-activity'),
]