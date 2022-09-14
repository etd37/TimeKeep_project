from datetime import datetime

from team.models import Team

def num_of_teams(team, user):
    teams = Team.objects.filter(team=team, created_by=user).count()

    return sum(teams)

