from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, FormView
from .models import Employee, Schedule, Manager, Userprofile
from .forms import NewUserForm
from django.contrib import messages


# Create your views here.


def home(request):
    return render(request, 'home.html')


class ManagerPage(ListView):
    template_name = 'manager.html'
    model = Employee
    context_object_name = 'employee_data'


class EmployeePage(ListView):
    template_name = 'employee.html'
    model = Schedule
    context_object_name = 'schedule_data'


def signup(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()

    return render(request, 'registration/signup.html', context={"register_form": form})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user.is_active:
                if user.is_superuser or user.is_staff:
                    login(request, user)
                    return redirect('/admin/')
                else:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('account')
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("account")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form": form})

@login_required
def myaccount(request):
    return render(request, 'account.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()


        messages.info(request, 'The changes was saved')

        return redirect('mccount')

    return render(request, 'edit_profile.html')