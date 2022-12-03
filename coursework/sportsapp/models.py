from django.db import models
from django.contrib.auth.models import User

'''
class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL)

# Composite primary key
class Member(models.Model):
    userID = models.IntegerField()
    teamID = models.IntegerField()

'''

'''
class Fixture(models.Model):
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    teamID = '''