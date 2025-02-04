from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def about(request):
    return HttpResponse("This is the about page.")

def login(request):
    return render(request, 'login.html')

@login_required
def secured_view(request):
    return render(request, 'secured.html')