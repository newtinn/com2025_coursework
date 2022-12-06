from django.test import TestCase, Client
from django.db.backends.sqlite3.base import IntegrityError
from django.db import transaction

from .models import Team, Member, Fixture, Avaliability
from django.contrib.auth.models import User
from .forms import TeamCreationForm, FixtureCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect

class SportsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # creating a test team
        user = User(username="steve", email="steve@gmail.com")
        user.set_password('Password123')
        user.save()

        client = Client()

        client.login(username=user.username, password="Password123")

    # testing logging in
    def testLogin(self):
        login = self.client.login(username='steve', password='Password123') 
        self.assertTrue(login)

    # testing user home
    def testUserTeam(self):
        login = self.client.login(username='steve', password='Password123') 

        response = self.client.get('/app/home')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Your teams')
        self.assertContains(response, 'Upcoming fixtures')

    # testing team form
    def testTeamCreate(self):
        db_count = Team.objects.all().count()
        data = {
            "name": "Guildford Rugby",
            "leader": 1
        }

        form = TeamCreationForm(data)
        self.assertTrue(form.is_valid())

    # testing team deletion
    def testTeamDelete(self):
        db_count = Team.objects.all().count()

        newTeam = Team(name="Aldershot FC", leader=1)
        newTeam.save()

        response = self.client.post(path=reverse("deleteTeam", kwargs={"team": 1}))
        self.assertEqual(db_count, 0)

    # checking if the add member form is hidden when team page is loaded
    def testMemberFormHidden(self):
        newTeam = Team(name="Aldershot FC", leader=1)
        newTeam.save()

        # getting new team id
        teamID = newTeam.id

        response = self.client.get('/app/team/'+str(teamID))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, 'Username')
        self.assertNotContains(response, 'Password')

    # testing if member can be added to team
    def testMemberCreate(self):
        newTeam = Team(name="Aldershot FC", leader=1)
        newTeam.save()

        user = User(username="dave", email="dave@gmail.com", password="Password123")
        user.save()

        db_count = Member.objects.all().count()
        data = {
            "username": user.username,
            "admin": False
        }

        member = Member(userID=user,teamID=newTeam,teamAdmin=False)
        member.save()

        response = self.client.post(HttpResponseRedirect('/app/team/1'), data)
        self.assertEqual(Member.objects.count(), db_count+1)

    # testing fixture creation
    def testFixtureCreate(self):
        login = self.client.login(username='steve', password='Password123') 
        user = User.objects.filter(username='steve').first()

        newTeam = Team(name="Aldershot FC", leader=user.id)
        newTeam.save()

        member = Member(userID=user, teamID = newTeam, teamAdmin = True)
        member.save()

        data = {
            "name": "Woking FC",
            "date": "12/20/2022 14:30",
            "description": "Friendly vs Woking FC",
            "location": "The Laithwaite Community Stadium, Woking GU22 9AA"
        }

        form = FixtureCreationForm(data)
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse('fixtureCreate', kwargs={"team": newTeam.id}), data)
        self.assertEqual(Fixture.objects.all().count(), 1)

    # testing team deletion
    def testFixtureDelete(self):
        db_count = Fixture.objects.all().count()

        newTeam = Team(name="Aldershot FC", leader=1)
        newTeam.save()

        fixture = Fixture(name="Woking FC", date="2022-12-20 14:30", description="Friendly vs Woking FC", location="The Laithwaite Community Stadium, Woking GU22 9AA", teamID=newTeam)
        fixture.save()

        response = self.client.post(path=reverse("deleteFixture", kwargs={"fixture": 1}))
        self.assertEqual(db_count, 0)

    # testing team avaliability
    def testAvaliablity(self):
        login = self.client.login(username='steve', password='Password123') 

        user = User.objects.get(id=1)

        newTeam = Team(name="Aldershot FC", leader=1)
        newTeam.save()

        member = Member(userID=user,teamID=newTeam,teamAdmin=False)
        member.save()

        fixture = Fixture(name="Woking FC", date="2022-12-20 14:30", description="Friendly vs Woking FC", location="The Laithwaite Community Stadium, Woking GU22 9AA", teamID=newTeam)
        fixture.save()

        check = Avaliability(userID = user, fixtureID = fixture, avaliable = False)
        check.save()

        response = self.client.get('/app/fixture/1')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'steve')
