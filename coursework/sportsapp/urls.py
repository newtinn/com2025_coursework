from django.urls import path
from . import views

urlpatterns = [
    path('home', views.userHome, name='userHome'),
    path('team/<int:team>', views.teamPage, name='teamPage')
]