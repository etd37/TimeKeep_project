from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, EditProfileForm
from django.contrib import messages
from team.models import Invitation, Team
from project.models import Project, Entry
from django.db import models
from team.mail import send_invitation_accepted
import calendar
from datetime import datetime, timedelta, timezone, date
from dateutil.relativedelta import relativedelta

from summary.utilities import get_time_for_user_and_month


def home1(request):
    return render(request, 'home.html')


def home(request):
    if request.user.is_authenticated:
        return redirect("home/")
    else: # remove else fix tabs
        if request.method == 'POST':
            form_type = request.POST.get('type', None)
            if form_type == 'login':
                login_form = AuthenticationForm(request, data=request.POST)
                if login_form.is_valid():
                    username = login_form.cleaned_data.get('username')
                    password = login_form.cleaned_data.get('password')
                    user = authenticate(username=username, password=password)
                    if user.is_active:
                        if user.is_superuser or user.is_staff:
                            login(request, user)
                            return redirect('/admin/')

                        login(request, user)
                        messages.info(request, f"You are now logged in as {username}.")
                        return redirect('summary:summary')
                    if user is not None: # if user
                        login(request, user)
                        messages.info(request, f"You are now logged in as {username}.")
                        return redirect("summary:summary")

                    messages.error(request, "Invalid username or password.")


                messages.error(request, "Invalid username or password.")
                return render(request, 'home.html')
            if form_type == 'registration':
                registration_form = NewUserForm(request.POST)
                if registration_form.is_valid():
                    user = registration_form.save()
                    login(request, user)
                    messages.success(request, "Registration successful.")
                    invitations = Invitation.objects.filter(email=user.email, status=Invitation.INVITED)

                    if invitations:
                        return redirect('accept_invitation')

                    return redirect('summary:summary')
                messages.error(request, "Unsuccessful registration. Invalid information.")
                return render(request, 'home.html')

            messages.error(request, "Unsuccessful registration. Invalid information.")


        login_form = AuthenticationForm()
        registration_form = NewUserForm()

        context = {'login_form': login_form, 'registration_form': registration_form}
        return render(request, 'home.html', context)


def shop(request):
    return render(request, 'shop.html')


def summary(request):
    return render(request, 'summary.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


@login_required
def account(request):
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

            return redirect('account')
    return render(request, 'account.html', {'teams': teams, 'invitations': invitations})


@login_required
def acc(request):

    teams = request.user.teams.exclude(pk=request.user.userprofile.active_team_id)
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id)
    invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)
    user_num_months = int(request.GET.get('user_num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)
    time_for_user_and_month = get_time_for_user_and_month(team, request.user, user_month)
    team_count = Team.objects.filter(created_by=request.user).count()
    team_member_at_count = Team.objects.filter(members=request.user).count()
    project_team_id = Team.objects.filter(members=request.user).values_list('id', flat=True)
    project_count = 0
    for x in project_team_id:
        project_count += Project.objects.filter(team_id=x).count()

    import calendar

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
    avg_hours_per_day = round(float(time_for_user_and_month / 60) / float(monthly_days_count),2)
    hour_percent = round(100 * float(time_for_user_and_month / 60)/float(monthly_hour_count))



    if request.method == 'POST':
        form_type = request.POST.get('type', None)
        if form_type == 'edit_user':
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()

            if request.FILES:
                avatar = request.FILES['avatar']
                userprofile = request.user.userprofile
                userprofile.avatar = avatar
                userprofile.save()

            messages.info(request, 'The changes were saved')
            return redirect('account')
        if form_type == 'edit_pass':
            form = PasswordChangeForm(data=request.POST, user=request.user)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.info(request, 'The changes were saved')
                return redirect('account')
            form = PasswordChangeForm(user=request.user)
            messages.info(request, 'Something went wrong')
            args = {'form': form}
            return render(request, 'change_password.html', args)





    return render(request, 'acc.html', {
        'teams': teams,
        'invitations': invitations,
        'time_for_user_and_month':time_for_user_and_month ,
        'team_count':team_count,
        'team_member_at_count':team_member_at_count,
        'project_count':project_count,
        'monthly_days_count':monthly_days_count,
        'monthly_hour_count':monthly_hour_count,
        'avg_hours_per_day':avg_hours_per_day,
        'hour_percent':hour_percent
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        if request.FILES:
            avatar = request.FILES['avatar']
            userprofile = request.user.userprofile
            userprofile.avatar = avatar
            userprofile.save()

        messages.info(request, 'The changes were saved')
        return redirect('account')

    return render(request, 'edit_profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'The changes were saved')
            return redirect('account')

        return redirect('change_password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'change_password.html', args)


@login_required
def accept_invitation(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        invitations = Invitation.objects.filter(code=code, email=request.user.email)

        if invitations:
            invitation = invitations[0]
            invitation.status = Invitation.ACCEPTED
            invitation.save()

            team = invitation.team
            team.members.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()

            messages.info(request, 'Invitation accepted')

            send_invitation_accepted(team, invitation)

            return redirect('summary:summary')

        messages.info(request, 'Invitation was not found')

    return render(request, 'accept_invitation.html')
