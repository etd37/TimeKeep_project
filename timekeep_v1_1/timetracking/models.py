from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    active_team_id = models.IntegerField(default=0)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    photo = models.ImageField(blank=True, null=True, upload_to='img/')
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField()
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Manager(models.Model):
    name = models.CharField(max_length=100)
    employees = models.ManyToManyField(Employee, blank=True, null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    days_worked = models.PositiveIntegerField(blank=True, null=True)
    started = models.TimeField(blank=True, null=True)
    finished = models.TimeField(blank=True, null=True)
    pause_start = models.TimeField(blank=True, null=True)
    pause_finish = models.TimeField(blank=True, null=True)
