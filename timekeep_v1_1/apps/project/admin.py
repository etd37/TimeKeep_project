from django.contrib import admin

# Register your models here.

from .models import Project, Entry

admin.site.register(Project)
admin.site.register(Entry)