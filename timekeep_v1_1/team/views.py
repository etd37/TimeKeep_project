from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import random
from datetime import datetime, timedelta, timezone, date
from dateutil.relativedelta import relativedelta

from .models import Team, Invitation
from project.models import Project
from .mail import send_invitation, send_invitation_accepted
from summary.utilities import get_time_for_user_and_date, \
    get_time_for_team_and_month, \
    get_time_for_user_and_month, \
    get_time_for_user_and_project_and_month, \
    get_time_for_user_and_team_month



@login_required
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            team = Team.objects.create(title=title, created_by=request.user)
            team.members.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()

            return redirect('account')

    return render(request, 'team/add.html')


@login_required
def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    invitations = team.invitations.filter(status=Invitation.INVITED)
    all_projects = team.projects.all()
    members = team.members.all()
    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)

    for project in all_projects:
        project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, project, request.user, user_month)

    if request.method == 'POST':
        title = request.POST.get('add_proj')

        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)
            project.save()

            return redirect('team:team', team_id=team.id)

    context = {
        'team': team,
        'invitations': invitations,
        'all_projects': all_projects,
        'projects': all_projects,
        'members': members,

    }

    return render(request, 'team/team.html', context)

@login_required
def teams(request):
    teams = request.user.teams.exclude(pk=request.user.userprofile.active_team_id)
    invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)

    if request.method == 'POST':
        title = request.POST.get('add_team')

        if title:
            team = Team.objects.create(title=title, created_by=request.user)
            team.members.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()

            return redirect('team:teams')

    return render(request, 'team/teams.html', {'teams': teams, 'invitations': invitations})


@login_required
def edit(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE,
                             members__in=[request.user])

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            team.title = title
            team.save()

            messages.info(request, 'The changes was saved')

            return redirect('team:team', team_id=team.id)

    return render(request, 'team/edit.html', {'team': team})


@login_required
def activate_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    userprofile = request.user.userprofile
    userprofile.active_team_id = team.id
    userprofile.save()

    messages.info(request, 'The team was activated')

    return redirect(request.META['HTTP_REFERER'])


@login_required
def invite(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            invitations = Invitation.objects.filter(team=team, email=email)

            if not invitations:
                code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz123456789') for i in range(8))
                invitation = Invitation.objects.create(team=team, email=email, code=code)

                messages.info(request, 'The user was invited')

                send_invitation(email, code, team)

                return redirect('team:team', team_id=team.id)
            else:
                messages.info(request, 'The users has already been invited')

    return render(request, 'team/invite.html', {'team': team})

@login_required
def plans(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)


    context= {
        'team': team,

    }
    return render(request, 'team/plans.html', context)