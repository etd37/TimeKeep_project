from django.contrib import admin
from .models import Manager, Employee, Schedule

# Register your models here.
admin.site.register(Manager)
admin.site.register(Employee)
admin.site.register(Schedule)
