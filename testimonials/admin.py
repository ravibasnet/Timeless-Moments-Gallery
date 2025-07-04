from django.contrib import admin
from django.utils.html import format_html
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_photo_thumbnail', 'client_name', 'service_type_display', 
                   'star_rating_display', 'is_featured', 'created_at')
    list_filter = ('service_type', 'rating', 'is_featured', 'created_at')
    search_fields = ('client_name', 'content', 'client_role')
    list_editable = ('is_featured',)
    readonly_fields = ('created_at', 'updated_at', 'star_rating_display')
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_role', 'client_photo')
        }),
        ('Testimonial Content', {
            'fields': ('content', 'rating', 'service_type')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'created_at', 'updated_at')
        }),
    )
    
    def client_photo_thumbnail(self, obj):
        if obj.client_photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.client_photo.url
            )
        return "No Photo"
    client_photo_thumbnail.short_description = 'Photo'
    
    def service_type_display(self, obj):
        return obj.get_service_type_display()
    service_type_display.short_description = 'Service'
    
    def star_rating_display(self, obj):
        return obj.star_rating
    star_rating_display.short_description = 'Rating'
    
    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/remixicon@3.0.0/fonts/remixicon.css',)
        }
