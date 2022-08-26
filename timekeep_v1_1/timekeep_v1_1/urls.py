"""timekeep_v1_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from timetracking.views import (
                        home,
                        ManagerPage,
                        EmployeePage,
                        signup,
                        signin,
                        myaccount,
                        edit_profile,
                        change_password,
                        logout_request
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('manager/', ManagerPage.as_view(), name='manager_page'),
    path('employee/', EmployeePage.as_view(), name='employee_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path("login/", signin, name="login"),
    path("logout/", logout_request, name="logout"),
    path("account/", myaccount, name="account"),
    path("account/edit_profile", edit_profile, name="edit_profile"),
    path("account/change_password", change_password, name="change_password"),
    path("account/teams/", include('team.urls'), name="change_password"),
    path("projects/", include('apps.project.urls'), name="change_password"),
]
