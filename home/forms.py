from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import TimeInput
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
class AdminExtraForm(forms.ModelForm):
    class Meta:
        model=models.AdminExtra
        fields=['mobile','status']


#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['mobile','cl','lv','status']


#for teacher related form
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
class TeacherExtraForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=models.Group.objects.all(), 
        widget=CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model=models.TeacherExtra
        fields=['groups','mobile','status']




#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()
    

class AskDateForm(forms.Form):
    date=forms.DateField()

class Groups(forms.ModelForm):
    class Meta:
        model=models.Group
        fields=['name','ability','level']

class Rooms(forms.ModelForm):
    class Meta:
        model=models.room
        fields=['name','ability']

class Days(forms.ModelForm):
    class Meta:
        model=models.Days
        fields=['name']

class Modules(forms.ModelForm):
    class Meta:
        model=models.Module
        fields=['name','codeM','level']




class Time24HInput(TimeInput):
    input_type = 'time'
    format = '%H:%M'
class DurationForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=models.Days.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), to_field_name='name')
    start_time = forms.TimeField(widget=Time24HInput, label='Start Time')
    end_time = forms.TimeField(widget=Time24HInput, label='End Time')
    class Meta:
        model = models.Duration
        fields = ['name', 'start_time', 'end_time']




#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'
