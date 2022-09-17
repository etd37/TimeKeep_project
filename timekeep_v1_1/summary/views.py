import calendar
from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from project.models import Entry
from project.models import Project
from team.models import Team, Invitation
from .utilities import get_time_for_user_and_date, \
    get_time_for_team_and_month, \
    get_time_for_user_and_month, \
    get_time_for_user_and_project_and_month, \
    get_time_for_user_and_team_month


# Create your views here.

@login_required
def summary(request):
    if not request.user.userprofile.active_team_id:
        teams = request.user.teams.exclude(pk=request.user.userprofile.active_team_id)
        invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)
        # create add team form for modal
        if request.method == 'POST':
            title = request.POST.get('add_team')

            if title:
                team = Team.objects.create(title=title, created_by=request.user)
                team.members.add(request.user)
                team.save()

                userprofile = request.user.userprofile
                userprofile.active_team_id = team.id
                userprofile.save()

                return redirect('summary:summary')

        return render(request, 'summary.html', {'teams': teams, 'invitations': invitations})

    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)
    all_projects = team.projects.all()
    members = team.members.all()

    num_days = int(request.GET.get('num_days', 0))
    date_user = datetime.now() - timedelta(days=num_days)
    date_entries = Entry.objects.filter(team=team, created_by=request.user, created_at__date=date_user, is_tracked=True)

    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)

    for project in all_projects:
        project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, project,
                                                                                              request.user, user_month)

    team_num_months = int(request.GET.get('team_num_months', 0))
    team_month = datetime.now() - relativedelta(months=team_num_months)

    for member in members:
        member.time_for_user_and_team_month = get_time_for_user_and_team_month(team, member, team_month)

    untracked_entries = Entry.objects.filter(team=team, created_by=request.user, is_tracked=False).order_by(
        '-created_at')

    for untracked_entry in untracked_entries:
        untracked_entry.minutes_since = int(
            (datetime.now(timezone.utc) - untracked_entry.created_at).total_seconds() / 60)

    monthly_days_count = 0
    cal = calendar.Calendar()

    for week in cal.monthdayscalendar(datetime.now().year, datetime.now().month):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            if day == 0 or i >= 5:
                continue
            # or some other control if desired...
            monthly_days_count += 1
    monthly_hour_count = monthly_days_count * 8
    time_for_user_and_month = get_time_for_user_and_month(team, request.user, user_month)
    avg_hours_per_day = round(float(time_for_user_and_month / 60) / float(monthly_days_count), 2)
    hour_percent = round(100 * float(time_for_user_and_month / 60) / float(monthly_hour_count))

    context = {
        'team': team,
        'invitations': invitations,
        'all_projects': all_projects,
        'projects': all_projects[0:3],
        'date_entries': date_entries,
        'num_days': num_days,
        'date_user': date_user,
        'members': members,
        'untracked_entries': untracked_entries,
        'user_num_months': user_num_months,
        'user_month': user_month,
        'time_for_user_and_month': get_time_for_user_and_month(team, request.user, user_month),
        'time_for_user_and_date': get_time_for_user_and_date(team, request.user, date_user),
        'time_for_team_and_month': get_time_for_team_and_month(team, team_month),
        'team_num_months': team_num_months,
        'team_month': team_month,
        'monthly_days_count': monthly_days_count,
        'monthly_hour_count': monthly_hour_count,
        'avg_hours_per_day': avg_hours_per_day,
        'hour_percent': hour_percent,
    }
    # create add project form for modal
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    if request.method == 'POST':
        title = request.POST.get('add_proj')

        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)
            project.save()

            return redirect('summary:summary')

    if 'home' and not 'dashboard' in request.META['PATH_INFO']:
        return render(request, 'summary.html', context)
    if 'dashboard' in request.META['PATH_INFO']:
        return render(request, 'dashboard.html', context)


@login_required
def view_user(request, user_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    all_projects = team.projects.all()
    user = team.members.all().get(id=user_id)

    num_days = int(request.GET.get('num_days', 0))
    date_user = datetime.now() - timedelta(days=num_days)
    date_entries = Entry.objects.filter(team=team, created_by=request.user, created_at__date=date_user, is_tracked=True)

    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)

    for project in all_projects:
        project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, project,
                                                                                              request.user, user_month)

    context = {
        'team': team,
        'user': user,
        'all_projects': all_projects,
        'date_entries': date_entries,
        'num_days': num_days,
        'date_user': date_user,
        'user_num_months': user_num_months,
        'user_month': user_month,
        'time_for_user_and_month': get_time_for_user_and_month(team, request.user, user_month),
        'time_for_user_and_date': get_time_for_user_and_date(team, request.user, date_user),

    }

    return render(request, 'view_user.html', context)
