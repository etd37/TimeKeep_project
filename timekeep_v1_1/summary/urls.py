from django.urls import path, include
from . import views
from .views import summary, view_user

app_name = 'summary'

urlpatterns = [
    path('', summary, name='summary'),
    path('dashboard/', summary, name='dashboard'),
    path('view_user=<int:user_id>', view_user, name='view_user'),




]