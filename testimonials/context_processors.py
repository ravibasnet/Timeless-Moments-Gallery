from .models import Testimonial

def featured_testimonials(request):
    """Add featured testimonials to the template context."""
    return {
        'featured_testimonials': Testimonial.objects.filter(
            is_featured=True
        ).order_by('-created_at')[:3]
    }
