from django.shortcuts import render, get_object_or_404
from .models import Portfolio

def portfolio_list(request):
    portfolios = Portfolio.objects.all().order_by('-event_date')
    return render(request, 'studio_portfolio/portfolio_list.html', {'portfolios': portfolios})

def portfolio_detail(request, slug):
    portfolio = get_object_or_404(Portfolio, slug=slug)
    return render(request, 'studio_portfolio/portfolio_detail.html', {'portfolio': portfolio})

def view_all_portfolios(request):
    portfolios = Portfolio.objects.all().order_by('-event_date')
    return render(request, 'studio_portfolio/portfolio_list.html', {'portfolios': portfolios})

def portfolio_category(request, category):
    portfolios = Portfolio.objects.filter(category=category).order_by('-event_date')
    return render(request, 'studio_portfolio/portfolio_list.html', {
        'portfolios': portfolios,
        'category': category
    })
