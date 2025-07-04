from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Count
from .models import Testimonial

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 9
    
    def get_queryset(self):
        return Testimonial.objects.filter(is_featured=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_types'] = Testimonial.SERVICE_CHOICES
        context['average_rating'] = Testimonial.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        context['total_testimonials'] = Testimonial.objects.count()
        return context

class TestimonialDetailView(DetailView):
    model = Testimonial
    template_name = 'testimonials/testimonial_detail.html'
    context_object_name = 'testimonial'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related testimonials (same service type, excluding current)
        context['related_testimonials'] = Testimonial.objects.filter(
            service_type=self.object.service_type
        ).exclude(id=self.object.id).order_by('-is_featured', '-created_at')[:3]
        return context

def service_testimonials(request, service_type):
    """View for filtering testimonials by service type"""
    testimonials = Testimonial.objects.filter(
        service_type=service_type,
        is_featured=True
    ).order_by('-created_at')
    
    service_name = dict(Testimonial.SERVICE_CHOICES).get(service_type, 'Testimonials')
    
    context = {
        'testimonials': testimonials,
        'service_type': service_type,
        'service_name': service_name,
        'service_icon': Testimonial(service_type=service_type).service_icon,
        'service_types': Testimonial.SERVICE_CHOICES,
        'average_rating': Testimonial.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,
        'total_testimonials': Testimonial.objects.count(),
    }
    return render(request, 'testimonials/testimonial_list.html', context)
