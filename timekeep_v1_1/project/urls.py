from django.urls import path

from .views import projects, project, edit_entry, add_entry, delete_entry, delete_untracked_entry

app_name = 'project'

urlpatterns = [
    path('', projects, name='projects'),
    path('<int:project_id>/', project, name='project'),
    path('<int:project_id>/<int:entry_id>/edit/', edit_entry, name='edit_entry'),
    path('<int:project_id>/<int:entry_id>/delete/', delete_entry, name='delete_entry'),
    path('add_entry/<int:entry_id>/', add_entry, name='add_entry'),
    path('delete_untracked_entry/<int:entry_id>/', delete_untracked_entry, name='delete_untracked_entry'),


]