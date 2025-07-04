from django.urls import path
from . import views

app_name = 'studio_main'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
] 