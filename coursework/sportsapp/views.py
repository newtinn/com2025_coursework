from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import TeamCreationForm, FixtureCreationForm

from .models import Team, Member, Fixture
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def userHome(request):
    if (request.user.is_authenticated):
        # getting the teams that the user is a part of
        teams = Member.objects.filter(userID=request.user).all()

        # getting the fixtures for the user
        fixtures = []

        for team in teams:
            teamFixtures = Fixture.objects.filter(teamID=team.teamID).all()
            for fixture in teamFixtures:
                fixtures.append(fixture)

        fixtures.sort(key = lambda x: x.date)

        return render(request, "userHome.html", {"teams": teams, "fixtures": fixtures})
    else:
        return HttpResponseRedirect('/')

def teamPage(request, team):
    context = { "team": None, "members": None, "error": None }

    currentTeam = Team.objects.filter(id=team).first()

    if (currentTeam):
        teamID = team
        context["team"] = currentTeam

        leader = User.objects.filter(id=currentTeam.leader).first()

        if (leader):
            context["leader"] = leader

        # listing the members of the team
        members = Member.objects.filter(teamID=currentTeam).all()
        if (members):
            context["members"] = members

        # showing fixtures
        fixtures = Fixture.objects.filter(teamID=currentTeam).all().order_by('date')
        if (fixtures):
            context["fixtures"] = fixtures
        
        # checking if the user is an admin
        if (request.user.is_authenticated):
            currentMember = Member.objects.filter(userID=request.user).first()
            if (currentMember.teamAdmin == True):
                context['admin'] = True
            else:
                context['admin'] = False
        
            # add member form
            if (context['admin'] == True):
                if (request.method == 'POST'):
                    newMember = request.POST['username']
                    if ('admin' in request.POST):
                        isAdmin = True
                    else:
                        isAdmin = False

                    # checking if the user exists
                    users = User.objects.filter(username=newMember).first()
                    if (users):
                        # user exists

                        # checking if member is not already in team
                        members = Member.objects.filter(userID=users, teamID=currentTeam)
                        if (members):
                            print("")
                        else:
                            member = Member(userID=users, teamID=currentTeam, teamAdmin=isAdmin)
                            member.save()

                        return HttpResponseRedirect('/app/team/'+str(currentTeam.id))

                
        
    return render(request, "team/teamHome.html", context)

@login_required(login_url='/accounts/login/')
def teamCreate(request):
    if (request.method == 'POST'):
        form = TeamCreationForm(request.POST)

        if (form.is_valid()):
            # Adding a new team record
            data = form.cleaned_data
            team = Team(name=data['name'], leader=request.user.id)
            team.save()
            teamID = str(Team.objects.latest('id'))

            member = Member(userID=request.user.id, teamID=teamID, teamAdmin=True)

            return HttpResponseRedirect('team/'+teamID)
        else:
            return HttpResponseRedirect('/team/create')
    else:
        form = TeamCreationForm()
        context = {'form': form}
        return render(request, "team/teamCreation.html", context)

@login_required(login_url='/accounts/login/')
def fixtureCreate(request, team):
    # checking if the user is an admin
    currentMember = Member.objects.filter(userID=request.user).first()

    if (currentMember.teamAdmin == True):
        if (request.method == 'POST'):
            currentTeam = Team.objects.filter(id=team).first()
            teamID = str(currentTeam.id)

            form = FixtureCreationForm(request.POST)

            if (form.is_valid()):
                # Adding a new team record
                data = form.cleaned_data
                fixture = Fixture(name=data['name'], date=data['date'], description=data['description'], location=data['location'], teamID=currentTeam)
                fixture.save()

                return HttpResponseRedirect('/app/team/'+teamID)
            else:
                # return message
                print(form.errors)

                return HttpResponseRedirect('/app/team/newFixture/'+teamID)
        else:
            form = FixtureCreationForm()
            context = {'form': form}
            return render(request, "fixtures/fixtureCreation.html", context)
    else:
        return HttpResponseRedirect('/')