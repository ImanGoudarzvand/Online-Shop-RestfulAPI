from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .task import notify_customers

def say_hello(request):

    notify_customers.delay('hello')


    return render(request, 'hello.html', {'name': 'Mosh'})
