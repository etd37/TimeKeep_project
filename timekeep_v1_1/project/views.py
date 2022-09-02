from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# Create your views here.

from .models import Project, Entry
from team.models import Team


@login_required
def projects(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = team.projects.all()

    if request.method == 'POST':
        title = request.POST.get('title')


    return render(request, 'project/projects.html', {'team': team, 'projects': projects})

@login_required
def project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        minutes_total = (hours * 60) + minutes

        entry = Entry.objects.create(team=team, project=project, minutes=minutes_total, created_by=request.user, created_at=date, is_tracked=True)

    return render(request, 'project/project.html', {'today': datetime.today(), 'team': team, 'project': project})

@login_required
def add(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            project = Project.objects.create(team=team, title=title, created_by=request.user)
            project.save()


            return redirect('project:projects')

    return render(request, 'project/add.html')


@login_required
def edit(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            project.title = title
            project.save()

            messages.info(request, 'The changes was saved!')

            return redirect('project:project', project_id=project.id)

    return render(request, 'project/edit.html', {'team': team, 'project': project})