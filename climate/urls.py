from django.urls import path
from . import views

urlpatterns = [
    path('climate-data/', views.climate_data_list, name='climate-data-list'),
    path('climate-predictions/', views.climate_prediction_list, name='climate-predictions-list'),
    path('create-climate-data/', views.create_climate_data, name='create-climate-data'),
    path('create-climate-prediction/', views.create_climate_prediction, name='create-climate-prediction'),
]