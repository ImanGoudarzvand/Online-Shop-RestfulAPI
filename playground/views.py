from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import requests
from rest_framework.views import APIView
from django.utils.decorators import method_decorator


class HelloView(APIView):
    
    @method_decorator(cache_page(2*60))
    def get(self, request):
        response = requests.get("https://httpbin.org/delay/2") # simulate a slow api
        data = response.json()
        return render(request, 'hello.html', {'name': data})
