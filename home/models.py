from django.db import models
import datetime

# Create your models here.
class Person(models.Model):
    personId = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=False)
    age = models.IntegerField(default=1)
    email = models.EmailField(null=True)
    frame = models.IntegerField(default=50)
    register_time = models.DateField(auto_now_add=True)
    class Meta:
        abstract = True

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    type = models.BooleanField(default=1)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=False)
    userage = models.IntegerField(default=1)
    email = models.EmailField(null=True)
    frame = models.IntegerField(default=50)
    register_time = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'user'

class Developer(models.Model):
    deveId = models.AutoField(primary_key=True)
    type = models.BooleanField(default=0)
    devename = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    deveage = models.IntegerField(default=1)
    email = models.EmailField()
    frame = models.IntegerField(default=100)
    register_time = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'developer'

class Challenge(models.Model):
    chId = models.AutoField(primary_key=True)
    type = models.BooleanField(default=0)
    chtype = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=False)
    requirment = models.TextField()
    award = models.IntegerField(default=0)
    technology = models.CharField(max_length=100, null=True)
    viewer_num = models.IntegerField(default=0)
    release_time = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=0)
    hoster = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    user_task = models.ManyToManyField('Developer')
    class Meta:
        db_table = 'challenge'

class SolutionFile(models.Model):
    fileId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    file = models.FileField(upload_to='SolutionFiles')
    size = models.DecimalField(max_digits=10, decimal_places=0)
    path = models.CharField(max_length=500)
    upload_time = models.DateTimeField(auto_now_add=True)
    auther = models.ForeignKey('Developer', on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey('Challenge', on_delete=models.CASCADE, null=True)

# class Task(models.Model):
#     taskId = models.AutoField(primary_key=True)
#     type = models.BooleanField(default=1)
#     title = models.CharField(max_length=100, null=False)
#     requirment = models.TextField()
#     viewer_num = models.IntegerField(default=0)
#     release_time = models.DateField(auto_now_add=True)
#     # release_time = models.DateField(default=datetime.datetime.now().strftime('%Y-%m-%d'))
#     status = models.BooleanField(default=0)
#
#     class Meta:
#         db_table = 'Task'