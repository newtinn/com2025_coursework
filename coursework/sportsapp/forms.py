from django.db import models
from django.forms import ModelForm
from .models import Team, Fixture

class TeamCreationForm(ModelForm):
    class Meta:
        model = Team
        fields = ["name"]

class FixtureCreationForm(ModelForm):
    class Meta:
        model =Fixture
        fields = ["name", "date", "description", "location"]