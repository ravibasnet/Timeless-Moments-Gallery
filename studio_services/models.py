from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class ServiceFeature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the service")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(help_text="Detailed description of the service")
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Base price for this service"
    )
    duration_minutes = models.PositiveIntegerField(
        help_text="Typical duration of the service in minutes"
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    features = models.ManyToManyField(ServiceFeature, blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this service is currently offered"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Service Type"
        verbose_name_plural = "Service Types"

    def __str__(self):
        return f"{self.name} (${self.base_price})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('studio_services:service_detail', args=[str(self.slug)])

class Equipment(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the equipment")
    description = models.TextField(help_text="Description of the equipment")
    model_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="Model number of the equipment"
    )
    purchase_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the equipment was purchased"
    )
    last_serviced = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the equipment was last serviced"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether the equipment is currently available for use"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the equipment"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self):
        return self.name

    def needs_service(self):
        """Check if equipment needs servicing based on last service date"""
        if not self.last_serviced:
            return True
        from datetime import date, timedelta
        six_months_ago = date.today() - timedelta(days=180)
        return self.last_serviced <= six_months_ago
