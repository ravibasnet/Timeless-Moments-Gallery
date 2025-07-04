from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


def client_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/testimonials/clients/<id>/<filename>
    return f'testimonials/clients/{instance.id}/{filename}'

class Testimonial(models.Model):
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    
    SERVICE_CHOICES = [
        ('wedding', 'Wedding Photography'),
        ('portrait', 'Portrait Session'),
        ('family', 'Family Session'),
        ('event', 'Event Coverage'),
        ('commercial', 'Commercial'),
        ('other', 'Other'),
    ]
    
    client_name = models.CharField(_("Client's Name"), max_length=100)
    client_role = models.CharField(_("Client's Role/Title"), max_length=100, blank=True, 
                                 help_text="E.g., Bride, CEO, Happy Customer")
    client_photo = models.ImageField(_("Client's Photo"), upload_to=client_photo_path, 
                                   blank=True, null=True)
    content = models.TextField(_("Testimonial Content"), 
                             help_text="What the client said about your service")
    rating = models.PositiveSmallIntegerField(_("Rating"), 
                                             choices=RATING_CHOICES,
                                             validators=[
                                                 MinValueValidator(1), 
                                                 MaxValueValidator(5)
                                             ])
    service_type = models.CharField(_("Service Type"), 
                                   max_length=20, 
                                   choices=SERVICE_CHOICES,
                                   default='other')
    is_featured = models.BooleanField(_("Featured on Homepage"), default=False,
                                    help_text="Show this testimonial on the homepage")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
    
    def __str__(self):
        return f"{self.client_name}'s Testimonial ({self.get_rating_display()})"
    
    @property
    def star_rating(self):
        """Return HTML stars for the rating"""
        return '★' * self.rating + '☆' * (5 - self.rating)
    
    @property
    def service_icon(self):
        """Return an icon based on service type"""
        icons = {
            'wedding': 'ri-heart-line',
            'portrait': 'ri-camera-line',
            'family': 'ri-group-line',
            'event': 'ri-calendar-event-line',
            'commercial': 'ri-building-line',
            'other': 'ri-star-line',
        }
        return icons.get(self.service_type, 'ri-star-line')
