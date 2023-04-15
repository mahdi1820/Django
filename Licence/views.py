from django.shortcuts import render, redirect ,HttpResponseRedirect
from django.urls import reverse

from .forms import StudyTimeForm , StudyTime
# Create your views here.



def create_study_time(request):
    if request.method == 'POST':
        form = StudyTimeForm(request.POST)
        if form.is_valid():
            study_time = form.save(commit=False)
            study_time.student = request.user
            study_time.save()
            return HttpResponseRedirect(reverse('timetable:create_study_time'))  # Replace 'view_name' with the actual name of the view that displays the timetable
    else:
        form = StudyTimeForm()
    return render(request, 'Licence/create_study_time.html', {'form': form})


def Licence(request):
    return render (request,'Licence/Licence.html')

def First_level(request):
    return render (request,'Licence/First_Level.html')

def view_timetable(request):
    study_times = StudyTime.objects.filter(student=request.user)
    return render(request, 'Licence/timetable.html', {'study_times': study_times})

