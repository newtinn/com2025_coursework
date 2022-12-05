from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = {}
    return render(request, 'home.html', context)

def contact(request):
    context = {}
    return render(request, 'contact.html', context)