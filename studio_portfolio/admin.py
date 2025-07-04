from django.contrib import admin
from .models import Portfolio, PortfolioImage

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioImageInline]
    list_display = ('title', 'event_date')
    prepopulated_fields = {'slug': ('title',)}
