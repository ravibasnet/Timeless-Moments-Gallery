from django.urls import path
from . import views

app_name = 'studio_portfolio'

urlpatterns = [
    path('', views.portfolio_list, name='portfolio_list'),
    path('all/', views.view_all_portfolios, name='view_all'),
    path('<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    
    # Add these new category URLs
    path('category/wedding/', views.portfolio_category, {'category': 'wedding'}, name='wedding'),
    path('category/portrait/', views.portfolio_category, {'category': 'portrait'}, name='portrait'),
    path('category/family/', views.portfolio_category, {'category': 'family'}, name='family'),
]
