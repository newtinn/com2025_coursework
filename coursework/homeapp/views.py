from django.core.mail import send_mail, BadHeaderError 
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, redirect 
from django.urls import reverse
from .forms import ContactForm 
from django.contrib import messages 

def home(request):
    context = {}
    return render(request, 'home.html', context)

def contact(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'] 
            subject = form.cleaned_data['subject'] 
            email = form.cleaned_data['email'] 
            message = name + ':\n' + form.cleaned_data['message'] 
            try:
                send_mail(subject, message, email, ["admin@example.com"])
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Message Not Sent') 
                return HttpResponseRedirect("contact") 
            return redirect(reverse('home'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Message Not Sent')
    return render(request, "contact.html", {"form": form})    