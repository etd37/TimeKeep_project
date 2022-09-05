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
from timetracking.timer import start_timer, stop_timer, discard_timer
from timetracking.views import (
    home,
    shop,
    signup,
    signin,
    account,
    edit_profile,
    change_password,
    logout_request,
    summary,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('shop', shop, name='shop'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('login/', signin, name='login'),
    path('logout/', logout_request, name='logout'),
    path('account/', account, name='account'),
    path('account/edit_profile', edit_profile, name='edit_profile'),
    path('account/change_password', change_password, name='change_password'),
    path('account/teams/', include('team.urls')),
    path('projects/', include('project.urls')),
    path('summary/', include('summary.urls')),
    path("timetracking/timer/start_timer/", start_timer, name='start_timer'),
    path("timetracking/timer/stop_timer/", stop_timer, name='stop_timer'),
    path("timetracking/timer/discard_timer/", discard_timer, name='discard_timer'),
]
