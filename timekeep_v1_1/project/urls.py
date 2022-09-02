from django.urls import path

from .views import projects, add, project, edit

app_name = 'project'

urlpatterns = [
    path('', projects, name='projects'),
    path('<int:project_id>/', project, name='project'),
    path('add/', add, name='add'),
    path('<int:project_id>/edit/', edit, name='edit'),

]