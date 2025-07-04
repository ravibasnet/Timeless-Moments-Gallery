"""
URL configuration for timeless_moments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.template.response import TemplateResponse
from django.shortcuts import render

# Custom error handlers
def custom_page_not_found(request, exception, template_name='studio_admin/404.html'):
    response = render(request, template_name, {})
    response.status_code = 404
    return response

def custom_server_error(request, template_name='studio_admin/500.html'):
    response = render(request, template_name, {})
    response.status_code = 500
    return response

# Set error handlers
handler404 = 'timeless_moments.urls.custom_page_not_found'
handler500 = 'timeless_moments.urls.custom_server_error'

# Admin site settings
admin.site.site_header = 'Timeless Moments Administration'
admin.site.site_title = 'Timeless Moments Admin'
admin.site.index_title = 'Dashboard'
admin.site.site_url = '/'

# Root URL configuration
urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # Include studio_main URLs (which includes the home view)
    path('', include('studio_main.urls')),
    
    # Authentication URLs (for password reset)
    path('admin/password_reset/', include('django.contrib.auth.urls')),
    
    # Redirect old admin URLs to the new admin
    path('django-admin/', RedirectView.as_view(url='/admin/', permanent=True)),
    path('accounts/login/', RedirectView.as_view(pattern_name='admin:login')),
    path('accounts/logout/', RedirectView.as_view(pattern_name='admin:logout')),
    path('accounts/password_change/', RedirectView.as_view(pattern_name='admin:password_change')),
    path('accounts/password_change/done/', RedirectView.as_view(pattern_name='admin:password_change_done')),
    
    # App URLs
    path('services/', include('studio_services.urls')),
    path('portfolio/', include('studio_portfolio.urls')),
    path('gallery/', include('studio_gallery.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('booking/', include('studio_booking.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass