from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

from .forms import ContactForm


def index(request):
    return render(request, 'portfolio/index.html')

def portfolio(request):
    return render(request, 'portfolio/portfolio.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail('New Submission', message, email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return redirect('portfolio:success')

    return render(request, 'portfolio/contact.html', {'form': form})

def success(request):
    return HttpResponse('I think it was successful')
