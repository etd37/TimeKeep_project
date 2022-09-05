from django.urls import path, include

from .views import summary

app_name = 'summary'

urlpatterns = [
    path('', summary, name='summary'),


]