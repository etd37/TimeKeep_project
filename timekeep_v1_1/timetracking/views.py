from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import NewUserForm, EditProfileForm
from django.contrib import messages
from team.models import Invitation
from team.mail import send_invitation_accepted


# Create your views here.


def home1(request):
    return render(request, 'home.html')

def home(request):
    if request.user.is_authenticated:
        return redirect("home/")
    else:
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
                        else:
                            login(request, user)
                            messages.info(request, f"You are now logged in as {username}.")
                            return redirect('summary:summary')
                    if user is not None:
                        login(request, user)
                        messages.info(request, f"You are now logged in as {username}.")
                        return redirect("summary:summary")
                    else:
                        messages.error(request, "Invalid username or password.")

                else:
                    messages.error(request, "Invalid username or password.")
                    return render(request, 'home.html')
            if form_type == 'registration':
                registration_form = NewUserForm(request.POST)
                if registration_form.is_valid():
                    user = registration_form.save()
                    login(request, user)
                    messages.success(request, "Registration successful.")
                    return redirect('summary:summary')
                messages.error(request, "Unsuccessful registration. Invalid information.")
                return render(request, 'home.html')
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")

        else:
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
    return render(request, 'account.html', {'teams':teams, 'invitations':invitations})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            messages.info(request, 'The changes were saved')
            return redirect('account')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'The changes were saved')
            return redirect('account')
        else:
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
        else:
            messages.info(request, 'Invitation was not found')
    else:
        return render(request, 'accept_invitation.html')

