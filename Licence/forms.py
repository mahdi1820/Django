from django import forms
from django.contrib.auth.models import User
from .models import StudyTime

class StudyTimeForm(forms.ModelForm):
    class Meta:
        model = StudyTime
        fields = ['student', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'}),
        }

