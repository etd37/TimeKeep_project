from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from .models import Project, Entry
from team.models import Team


@login_required
def projects(request):
    teams = Team.objects.filter(members=request.user)
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project_team_id = Team.objects.filter(members=request.user).values_list('id', flat=True)
    projects = team.projects.all()

    if request.method == 'POST':
        title = request.POST.get('add_proj')

        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)
            project.save()

            return redirect('project:projects')

    for x in project_team_id:
        projects_for_teams = Project.objects.filter(team_id=x)

    return render(request, 'project/projects.html',
                  {'team': team, 'projects': projects, 'project_team_id': project_team_id,
                   'projects_for_teams': projects_for_teams, 'teams': teams, })


@login_required
def project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == 'POST':
        form_type = request.POST.get('type', None)
        if form_type == 'edit_projct':
            title = request.POST.get('edit_proj')

            if title:
                project.title = title
                project.save()

                messages.info(request, 'The changes was saved!')

                return redirect('project:project', project_id=project.id)

        if form_type == 'add_time':
            hours = int(request.POST.get('hours', 0))
            minutes = int(request.POST.get('minutes', 0))
            date = '%s %s' % (request.POST.get('date'), datetime.now().time())
            minutes_total = int(hours) * 60 + int(minutes)

            entry = Entry.objects.create(team=team, project=project, minutes=minutes_total, created_by=request.user,
                                         created_at=date, is_tracked=True)
            return redirect('project:project', project_id=project.id)
    return render(request, 'project/project.html', {'today': datetime.today(), 'team': team, 'project': project})





@login_required
def edit_entry(request, project_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())

        entry.created_at = date
        entry.minutes = (hours * 60) + minutes
        entry.save()

        messages.info(request, 'The changes was saved!')

        return redirect('project:project', project_id=project.id)

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'team': team,
        'project': project,
        'entry': entry,
        'hours': hours,
        'minutes': minutes

    }

    return render(request, 'project/edit_entry.html', context)


@login_required
def add_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    projects = team.projects.all()

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        project = request.POST.get('project')

        if project:
            entry.project_id = project
            entry.minutes = (hours * 60) + minutes
            entry.created_at = '%s %s' % (request.POST.get('date'), entry.created_at.time())
            entry.is_tracked = True
            entry.save()

            messages.info(request, 'The time was tracked')

            return redirect('home')
        else:
            messages.error(request, '"Project" can not be empty! Choose a project.')

    hours, minutes = divmod(entry.minutes, 60)

    context = {
        'hours': hours,
        'minutes': minutes,
        'team': team,
        'projects': projects,
        'entry': entry
    }

    return render(request, 'project/add_entry.html', context)


@login_required
def delete_entry(request, project_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, 'Entry was deleted!')

    return redirect('project:project', project_id=project.id)



@login_required
def delete_untracked_entry(request, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)

    entry = get_object_or_404(Entry, pk=entry_id, team=team)
    entry.delete()

    messages.info(request, 'Entry was deleted!')

    return redirect(request.META['HTTP_REFERER'])