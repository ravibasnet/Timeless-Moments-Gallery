from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class BookingSession(models.Model):
    """Model for photography/videography booking sessions"""
    SESSION_TYPES = [
        ('wedding', 'Wedding Photography'),
        ('portrait', 'Portrait Session'),
        ('family', 'Family Photography'),
        ('maternity', 'Maternity Session'),
        ('newborn', 'Newborn Photography'),
        ('event', 'Event Coverage'),
        ('commercial', 'Commercial Shoot'),
        ('other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    class Meta:
        db_table = 'studio_orders_bookingsession'
        verbose_name = 'Booking Session'
        verbose_name_plural = 'Booking Sessions'

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    dates = models.JSONField(default=list)  # Stores multiple dates as list
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Duration in hours (8 = Full Day)"
    )
    location = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255, default='')
    client_email = models.EmailField(default='')
    client_phone = models.CharField(max_length=20, default='')
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gallery_images = models.JSONField(default=list, blank=True, help_text="List of image URLs for the session gallery")
    testimonial = models.TextField(blank=True, help_text="Client feedback/testimonial")
    testimonial_approved = models.BooleanField(default=False, help_text="Mark if testimonial is approved for display")

    def __str__(self):
        return f"{self.get_session_type_display()} for {self.client_name}"

class AvailableSlot(models.Model):
    """Model for available booking slots"""
    date = models.DateField()
    max_sessions = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['date']
        unique_together = ('date',)

    def __str__(self):
        return f"Slot on {self.date}"
