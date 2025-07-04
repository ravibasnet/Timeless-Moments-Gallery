from django.urls import path
from . import views as views

app_name = 'studio_booking'  

urlpatterns = [
    path('', views.booking_spa, name='booking_spa'),
    path('api/book/', views.api_book_session, name='api_book_session'),
    path('api/slots/', views.get_available_slots, name='get_available_slots'),
    path('api/bookings/', views.get_bookings, name='get_bookings'),
    path('api/gallery/<int:booking_id>/upload/', views.upload_gallery_image, name='upload_gallery_image'),
    path('api/bookings/<int:booking_id>/gallery/', views.get_booking_gallery, name='get_booking_gallery'),
]
