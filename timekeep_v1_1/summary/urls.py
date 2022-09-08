from django.urls import path, include
from . import views
from .views import summary

app_name = 'summary'

urlpatterns = [
    path('', summary, name='summary'),
    path('dashboard/', summary, name='dashboard'),




]