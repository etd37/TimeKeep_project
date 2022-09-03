from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from project.models import Entry
from team.models import Team
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

from .utilities import get_time_for_user_and_date, \
    get_time_for_team_and_month, \
    get_time_for_user_and_month, \
    get_time_for_user_and_project_and_month, \
    get_time_for_user_and_team_month

# Create your views here.

@login_required
def summary(request):
    if not request.user.userprofile.active_team_id:
        return redirect('account')

    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    all_projects = team.projects.all()
    members = team.members.all()

    num_days = int(request.GET.get('num_days', 0))
    date_user = datetime.now() - timedelta(days=num_days)
    date_entries = Entry.objects.filter(team=team, created_by=request.user, created_at__date=date_user, is_tracked=True)

    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)

    for project in all_projects:
        project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, project, request.user, user_month)

    team_num_months = int(request.GET.get('team_num_months', 0))
    team_month = datetime.now() - relativedelta(months=team_num_months)

    for member in members:
        member.time_for_user_and_team_month = get_time_for_user_and_team_month(team, member, team_month)


    context = {
        'team': team,
        'all_projects': all_projects,
        'date_entries': date_entries,
        'num_days': num_days,
        'date_user': date_user,
        'members': members,
        'user_num_months': user_num_months,
        'user_month': user_month,
        'time_for_user_and_month': get_time_for_user_and_month(team, request.user, user_month),
        'time_for_user_and_date': get_time_for_user_and_date(team, request.user, date_user),
        'time_for_team_and_month': get_time_for_team_and_month(team, team_month),
        'team_num_months': team_num_months,
        'team_month': team_month,

    }

    return render(request, 'summary.html', context)