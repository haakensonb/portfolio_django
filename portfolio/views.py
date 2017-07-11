from django.shortcuts import render


def index(request):
    return render(request, 'portfolio/index.html')

def portfolio(request):
    return render(request, 'portfolio/portfolio.html')
