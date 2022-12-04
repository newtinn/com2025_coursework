from django.db import models
from django.forms import ModelForm
from .models import Team

class TeamCreationForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'leader']