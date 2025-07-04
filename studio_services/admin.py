from django.contrib import admin
from .models import ServiceType, ServiceFeature, Equipment

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'duration_minutes', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('features',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_number', 'is_available', 'last_serviced')
    list_filter = ('is_available', 'purchase_date', 'last_serviced')
    search_fields = ('name', 'description', 'model_number')
    readonly_fields = ('created_at',)