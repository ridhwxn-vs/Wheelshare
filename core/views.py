from django.http import HttpResponse
from django.shortcuts import redirect,render

def home(request):
    return render(request,'landingpg.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')
