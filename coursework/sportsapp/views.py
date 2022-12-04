from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import TeamCreationForm

from .models import Team
from django.contrib.auth.models import User

def userHome(request):
    if (request.user.is_authenticated):
        return render(request, "userHome.html", {})
    else:
        return HttpResponseRedirect('/')

def teamPage(request, team):
    context = { "team": None }

    data = Team.objects.filter(id=team).first()

    if (data):
        teamID = team

        leader = User.objects.filter(id=data.leader).first()

        if (leader):
            context = { "team": data, "leader": leader }
        else:
            context = { "team": data }    

        

    return render(request, "team/teamHome.html", context)

'''
def teamCreate(request):
    if (request.method == 'POST'):
        form = TeamCreationForm(request.POST)

        if (form.is_valid()):
            return 
'''