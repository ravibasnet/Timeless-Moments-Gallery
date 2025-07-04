from django import template
from ..models import Testimonial

register = template.Library()

@register.inclusion_tag('testimonials/includes/testimonial_slider.html', takes_context=True)
def testimonial_slider(context, limit=6, show_title=True, show_view_all=True):
    """
    Display a slider of featured testimonials.
    
    Usage: {% load testimonial_tags %}
           {% testimonial_slider limit=6 show_title=True show_view_all=True %}
    """
    testimonials = Testimonial.objects.filter(is_featured=True).order_by('-created_at')[:limit]
    
    return {
        'testimonials': testimonials,
        'show_title': show_title,
        'show_view_all': show_view_all,
        'request': context.get('request'),
    }

@register.inclusion_tag('testimonials/includes/testimonial_slider.html', takes_context=True)
def testimonial_slider(context, limit=6, show_title=True, show_view_all=True):
    """
    Display an improved slider of featured testimonials with enhanced design.
    
    Usage: {% load testimonial_tags %}
           {% testimonial_slider limit=6 show_title=True show_view_all=True %}
    """
    testimonials = Testimonial.objects.filter(is_featured=True).order_by('-created_at')[:limit]
    
    return {
        'testimonials': testimonials,
        'show_title': show_title,
        'show_view_all': show_view_all,
        'request': context.get('request'),
    }
