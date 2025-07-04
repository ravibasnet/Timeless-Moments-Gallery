from django.shortcuts import render, get_object_or_404
from .models import ServiceType

# Create your views here.

def service_list(request):
    """
    View for listing all available services
    """
    services = ServiceType.objects.all()
    return render(request, 'studio_services/service_list.html', {'services': services})

def service_detail(request, slug):
    """
    View for displaying details of a specific service
    """
    service = get_object_or_404(ServiceType, slug=slug)
    return render(request, 'studio_services/service_detail.html', {
        'service': service,
    })
