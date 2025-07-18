from django.contrib import admin
from .models import Category, Photo

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'upload_date')
    list_filter = ('category', 'upload_date')
    search_fields = ('title', 'description')
