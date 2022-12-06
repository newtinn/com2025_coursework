from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import TeamCreationForm, FixtureCreationForm, RegisterForm

from .models import Team, Member, Fixture, Avaliability
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def register(response):
    if (response.method == "POST"):
        form = RegisterForm(response.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/accounts/login')
    else:
        form = RegisterForm()
    
    return render(response, "registration/register.html", {"form": form})

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

            user = User.objects.get(id=request.user.id)

            member = Member(userID=request.user, teamID=team, teamAdmin=True)
            member.save()

            return HttpResponseRedirect('/app/team/'+str(team.id))
        else:
            return HttpResponseRedirect('/team/create')
    else:
        form = TeamCreationForm()
        context = {'form': form}
        return render(request, "team/teamCreation.html", context)

@login_required(login_url='/accounts/login/')
def teamDelete(request, team):
    # checking if the user is an admin
    user = Member.objects.filter(userID=request.user).first()
    if (user):
        if (user.teamAdmin == True):
            team = Team.objects.get(id=team)
            team.delete()
    
    return HttpResponseRedirect('/app/home')

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

@login_required(login_url='/accounts/login/')
def fixtureHome(request, fixture):
    context = {}
    
    # checking if user is an admin
    currentMember = Member.objects.filter(userID=request.user).first()

    if (currentMember.teamAdmin == True):
        context["admin"] = True

    currentFixture = Fixture.objects.filter(id=fixture).first()
    if (currentFixture):
        context["fixture"] = currentFixture

        # getting the people that are avaliable
        usersAvaliableList = []
        usersAvaliable = Avaliability.objects.filter(fixtureID=currentFixture, avaliable=True).all()
        if (usersAvaliable):
            for user in usersAvaliable:
                currentUser = User.objects.filter(id=user.userID.id).first()
                usersAvaliableList.append(currentUser)
            
            context["avaliable"] = usersAvaliableList

        usersUnavaliableList = []
        usersUnavaliable = Avaliability.objects.filter(fixtureID=currentFixture, avaliable=False).all()
        if (usersUnavaliable):
            for user in usersUnavaliable:
                currentUser = User.objects.filter(id=user.userID.id).first()
                usersUnavaliableList.append(currentUser)
            
            context["unavaliable"] = usersUnavaliableList

        if (request.method == "POST"):
            user = User.objects.filter(id=request.user.id).first()

            checkAvaliability = Avaliability.objects.filter(userID=request.user, fixtureID=currentFixture).first()

            if (request.POST.get("avaliable")):
                # checking if the user has already voted
                if (checkAvaliability):
                    checkAvaliability.avaliable = True
                    checkAvaliability.save()
                else:
                    avaliability = Avaliability(userID=request.user, fixtureID=currentFixture, avaliable=True)
                    avaliability.save()
            
            if (request.POST.get("unavaliable")):
                if (checkAvaliability):
                    checkAvaliability.avaliable = False
                    checkAvaliability.save()
                else:
                    avaliable = Avaliability(userID=request.user, fixtureID=currentFixture, avaliable=False)
                    avaliable.save()

            return HttpResponseRedirect('/app/fixture/'+str(fixture))
    else:
        context["error"] = True

    return render(request, "fixtures/fixtureHome.html", context)

@login_required(login_url='/accounts/login/')
def fixtureDelete(request, fixture):
    # checking if the user is an admin
    user = Member.objects.filter(userID=request.user).first()
    if (user):
        if (user.teamAdmin == True):
            currentFixture = Fixture.objects.get(id=fixture)
            currentFixture.delete()
    
    return HttpResponseRedirect('/app/home')