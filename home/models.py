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
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


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
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



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

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)

    def __str__(self):
        return self.by


    
codeM = [('C','C'),('TD','TD'),('TP','TP')]

class Module(models.Model):
    name = models.CharField(max_length=50)
    codeM = models.CharField(max_length=10,choices=codeM,default='C')   
    level = models.CharField(max_length=10,choices=level,default='L1')
    
    def __str__(self):
        return self.name


class room(models.Model):
    name = models.CharField(max_length=40)
    ability = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name


class Days(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['order']

class Duration(models.Model):
    name = models.ForeignKey(Days, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

class Activities(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE)
    classroom = models.ForeignKey(room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherExtra, on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE , null=True)
    
    @property
    def get_name(self):
        return self.teacher.user.first_name+" "+self.teacher.user.last_name

    @property
    def get_module(self):
        return self.module.name+" "+"("+self.module.codeM+")"
    
    def __str__(self):
        return f"{self.module} {self.duration} {self.classroom} {self.teacher.user.first_name} {self.teacher.user.last_name} {self.group}"
    
    class Meta:
        ordering = ['duration']
class Attendance(models.Model):
    cl = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()
    present_status = models.CharField(max_length=10)
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE, null=True)
    
    @property
    def get_module(self):
        return self.activity.module.name+" "+"("+self.activity.module.codeM+")"

    @property
    def get_duration(self):
        start_time_str = self.activity.duration.start_time.strftime('%H:%M:%S')
        end_time_str = self.activity.duration.end_time.strftime('%H:%M:%S')
        return str(self.activity.duration.name) + " [" + start_time_str + " " + end_time_str + "]"