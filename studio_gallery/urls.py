from django.urls import path
from . import views

app_name = 'studio_gallery'

urlpatterns = [
    path('', views.gallery_home, name='gallery_home'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
]
