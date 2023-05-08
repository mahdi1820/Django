from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
from datetime import datetime

class AdminExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    


level=[('L1','L1'),('L2','L2'),('L3','L3')]

class Group(models.Model):
    LEVEL_CHOICES = [
        ('L1', 'L1'),
        ('L2', 'L2'),
        ('L3', 'L3'),
    ]

    name = models.CharField(max_length=60)
    ability = models.PositiveIntegerField(null=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='L1')
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name'] 

class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    



class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=40,null=True)
    lv = models.CharField(max_length=10,choices=level,default='L1')
    cl= models.ForeignKey(Group,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Attendance(models.Model):
    date=models.DateField()
    cl=models.ForeignKey(Group,on_delete=models.CASCADE)
    present_status = models.CharField(max_length=10)
    

class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)

    def __str__(self):
        return self.by


    
codeM = [('C','C'),('TD','TD'),('TP','TP')]

class material (models.Model):
    name = models.CharField(max_length=50)
    codeM = models.CharField(max_length=10,choices=codeM,default='C')   
    
class room(models.Model):
    name = models.CharField(max_length=40)
    ability = models.PositiveIntegerField(null=True)