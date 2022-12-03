from django.shortcuts import render
from django.http import HttpResponseRedirect

def userHome(request):
    if (request.user.is_authenticated):
        return render(request, "userHome.html", {})
    else:
        return HttpResponseRedirect('/')