from django.db import models
from django.forms import ModelForm, EmailField
from .models import Team, Fixture

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class TeamCreationForm(ModelForm):
    class Meta:
        model = Team
        fields = ["name"]

class FixtureCreationForm(ModelForm):
    class Meta:
        model =Fixture
        fields = ["name", "date", "description", "location"]