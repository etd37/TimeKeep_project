from django.urls import path
from .views import teams, add, team, edit, activate_team, invite, plans

app_name = 'team'

urlpatterns = [
    path('', teams, name='teams'),
    path('add/', add, name='add'),
    path('<int:team_id>/', team, name='team'),
    path('edit/', edit, name='edit'),
    path('invite/', invite, name='invite'),
    path('plans/', plans, name='plans'),
    path('activate_team/<int:team_id>/', activate_team, name='activate_team')
]