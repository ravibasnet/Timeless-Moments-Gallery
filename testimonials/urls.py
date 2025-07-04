from django.urls import path
from . import views

app_name = 'testimonials'

urlpatterns = [
    path('', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('service/<str:service_type>/', views.service_testimonials, name='service_testimonials'),
    path('<int:pk>/', views.TestimonialDetailView.as_view(), name='testimonial_detail'),
]
