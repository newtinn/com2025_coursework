from django.urls import path
from . import views

urlpatterns = [
    path('home', views.userHome, name='userHome'),
    path('team/<int:team>', views.teamPage, name='teamPage'),
    path('team/create', views.teamCreate, name='teamCreate'),
    path('team/newFixture/<int:team>', views.fixtureCreate, name='fixtureCreate'),
    path('fixture/<int:fixture>', views.fixtureHome, name='fixtureHome'),
    path('register/', views.register, name='register'),
    path('delete/team/<int:team>', views.teamDelete, name='deleteTeam'),
    path('delete/fixture/<int:fixture>', views.fixtureDelete, name='deleteFixture')
]