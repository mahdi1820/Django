from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import TimeInput
from django.core.exceptions import ValidationError


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
        widget=forms.CheckboxSelectMultiple,
        required=False
    )



    class Meta:
        model = models.TeacherExtra
        fields = ['groups', 'mobile', 'status']







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
        fields=['name','order']

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

class Activities(forms.ModelForm):
    module = forms.ModelChoiceField(queryset=models.Module.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    duration = forms.ModelChoiceField(queryset=models.Duration.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    classroom = forms.ModelChoiceField(queryset=models.room.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    teacher = forms.ModelChoiceField(queryset=models.TeacherExtra.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(queryset=models.Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = models.Activities
        fields = ['module', 'duration', 'classroom', 'teacher','group']
        
    def __init__(self, *args, **kwargs):
        super(Activities, self).__init__(*args, **kwargs)
        
        # Modify the label of each option in the dropdown menu for each field
        self.fields['module'].label_from_instance = lambda obj: f'{obj.name} ({obj.codeM}) - {obj.level}'
        self.fields['duration'].label_from_instance = lambda obj: f'{obj.name} [{obj.start_time} - {obj.end_time}]'
        self.fields['classroom'].label_from_instance = lambda obj: f'{obj.name} '
        self.fields['teacher'].label_from_instance = lambda obj: f'{obj.user.first_name} {obj.user.last_name} '
        self.fields['group'].label_from_instance = lambda obj: f'{obj.name} '

    def clean(self):
        cleaned_data = super().clean()

        # Check if there is already an activity with the selected duration, classroom, teacher, group, and module
        duration = cleaned_data.get('duration')
        classroom = cleaned_data.get('classroom')
        teacher = cleaned_data.get('teacher')
        module = cleaned_data.get('module')
        group = cleaned_data.get('group')
        if duration and teacher :
            conflicting_activities = models.Activities.objects.filter(
                duration=duration,
                teacher=teacher,
            ).exclude(pk=self.instance.pk if self.instance else None)
            if conflicting_activities.exists():
                msg = "An activity with the name  already exists."
                raise ValidationError(msg)
        elif classroom and duration and group:
            conflicting_activities = models.Activities.objects.filter(
                classroom=classroom,
                duration=duration,
                group=group,
            ).exclude(pk=self.instance.pk if self.instance else None)
            if conflicting_activities.exists():
                msg = "An activity with the name  already exists."
                raise ValidationError(msg)

        return cleaned_data

    def save(self, commit=True):
        # Get the instance of the model being edited
        instance = super().save(commit=False)

        # Set the values of the fields
        instance.module = self.cleaned_data['module']
        instance.duration = self.cleaned_data['duration']
        instance.classroom = self.cleaned_data['classroom']
        instance.teacher = self.cleaned_data['teacher']
        instance.group = self.cleaned_data['group']

        # Check if there is already an activity with the selected duration, classroom, teacher, group, and module
        conflicting_activities = models.Activities.objects.filter(
            duration=instance.duration,
            classroom=instance.classroom,
            teacher=instance.teacher,
            group=instance.group,
            module=instance.module,
        ).exclude(pk=instance.pk if instance.pk else None)

        if conflicting_activities.exists():
            # Do not save the instance if a conflicting activity already exists
            return None

        # Save the instance to the database
        if commit:
            instance.save()
        return instance




#for Attendance related form
class AttendanceForm(forms.Form):
    present_status = forms.ChoiceField(choices=(('Present', 'Present'), ('Absent', 'Absent')))
    date = forms.DateField()
    group = forms.ModelChoiceField(queryset=models.Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    activity = forms.ModelChoiceField(queryset=models.Activities.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activity'].queryset = models.Activities.objects.none()

        if 'group' in self.data:
            group_id = int(self.data.get('group'))
            self.fields['activity'].queryset = models.Activities.objects.filter(group_id=group_id)

    def clean(self):
        cleaned_data = super().clean()
        activity = cleaned_data.get('activity')
        date = cleaned_data.get('date')

        if activity and date:
            # Check if attendance has already been marked for this activity on the selected date
            if models.Attendance.objects.filter(activity=activity, date=date).exists():
                msg = 'Attendance has already been marked for this activity on the selected date.'
                self.add_error('date', msg)
                self.add_error('activity', msg)

            # Check if attendance has already been marked for any student for this activity on the selected date
            if models.Attendance.objects.filter(activity=activity, date=date, student__in=models.StudentExtra.objects.filter(cl=cleaned_data['group'])).exists():
                msg = 'Attendance has already been marked for a student for this activity on the selected date.'
                self.add_error('date', msg)
                self.add_error('activity', msg)

        return cleaned_data



#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'
