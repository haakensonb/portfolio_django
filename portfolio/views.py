from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

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
            formatted_message = 'Name: {}\n\nEmail: {}\n\nMessage:{}'.format(name, email, message)
            try:
                send_mail('New Submission', formatted_message, email, ['brandon.haakenson@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found')

            messages.add_message(request, messages.SUCCESS, 'Your message was sent! I\'ll get back to you shortly.', extra_tags='fade in')
            return redirect('portfolio:contact')

    return render(request, 'portfolio/contact.html', {'form': form})
