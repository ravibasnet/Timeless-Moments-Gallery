from django.shortcuts import render
from studio_services.models import ServiceType
from studio_portfolio.models import Portfolio

def home(request):
    """
    View for the home page
    """
    services = ServiceType.objects.all()[:4]
    portfolios = Portfolio.objects.order_by('-event_date')
    
    context = {
        'services': services,
        'portfolios': portfolios,
    }
    return render(request, 'studio_main/home.html', context)

def contact(request):
    """
    View for the contact page
    """
    if request.method == 'POST':
        # Add contact form processing logic here
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
    return render(request, 'studio_main/contact.html')
