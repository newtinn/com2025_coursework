from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.IntegerField()

# Composite primary key
class Member(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    teamID = models.ForeignKey(Team, on_delete=models.CASCADE)
    teamAdmin = models.BooleanField(default=False)

class Fixture(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    teamID = models.ForeignKey(Team, on_delete=models.CASCADE)

class Avaliability(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    fixtureID = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    avaliable = models.BooleanField(default=False)