from django.urls import path
from . import views

app_name = 'studio_services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
]