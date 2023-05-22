from django.shortcuts import render ,HttpResponseRedirect,redirect,reverse, get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth.decorators import login_required , user_passes_test
from . import forms,models
from django.db.models import Sum 
from django.core.mail import send_mail
from datetime import datetime
from django.db import IntegrityError
from django.db.models import Q
from .forms import TeacherUserForm ,TeacherExtraForm,DurationForm,Activities
# Create your views here.

@login_required(login_url = 'login')
def home(request):
    return render (request,'school/index.html')


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')    
        user = authenticate(request, username = username ,password = pass1)
        if user is not None:
            auth_login(request,user)
            if is_admin(request.user):
                return redirect('home')            
            elif is_teacher(request.user):
                return redirect('home')  
            elif is_student(request.user):
                return redirect('student-dashboard')
        else:
            messages.error(request,'Invalid username or password . Please try again.')
    return render (request,'school/Alogin.html')

@login_required(login_url = 'login')
def Logout(request):
    logout(request)
    return redirect('login')  



@login_required(login_url = 'login')
def master(request):
    return render (request,'school/master.html')
#------------------------------------------------------------------

def admin_admin_view(request):
    return render(request,'school/admin-admin.html')

def admin_signup_view(request):
    form=forms.AdminSignupForm()
    form2=forms.AdminExtraForm()
    mydict={'form':form,'form2':form2}
    if request.method=='POST':
        form=forms.AdminSignupForm(request.POST)
        form2=forms.AdminExtraForm(request.POST)
        if form.is_valid() and form2.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()
            
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('admin-add-admin')
    return render(request,'school/admin_add_admin.html',context=mydict)

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        return redirect('teacher-dashboard')  
    

#for dashboard of adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    
    studentcount=models.StudentExtra.objects.all().filter(status=True).count()

    groupcount = models.Group.objects.all().count()

    roomcount = models.room.objects.all().count()

    admincount = models.AdminExtra.objects.all().filter(status=True).count()

    modulecount = models.Module.objects.all().count()

    dayswork = models.Days.objects.all().count()

    activity = models.Activities.objects.all().count()

    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,

        'studentcount':studentcount,
        
        'groupcount':groupcount,

        'roomcount':roomcount,

        'admincount':admincount,

        'modulecount':modulecount,

        'dayswork':dayswork,

        'activity':activity,

        'notice':notice
    }
    return render(request,'school/admin_dashboard.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_admin_view(request):
    admins = models.AdminExtra.objects.all()
    return render(request,'school/admin_view_admin.html',{'admins':admins})

@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_admin_from_University_view(request,pk):
    admin=models.AdminExtra.objects.get(id=pk)
    user=models.User.objects.get(id=admin.user_id)
    user.delete()
    admin.delete()
    return redirect('admin-view-admin')

@login_required(login_url="login")
@user_passes_test(is_admin)
def update_admin_view(request,pk):
    admin=models.AdminExtra.objects.get(id=pk)
    user=models.User.objects.get(id=admin.user_id)
    form=forms.AdminSignupForm(instance=user)
    form2=forms.AdminExtraForm(instance=admin)
    mydict={'form':form,'form2':form2}
    if request.method=='POST':
        form=forms.AdminSignupForm(request.POST,instance=user)
        form2=forms.AdminExtraForm(request.POST,instance=admin)
        
        if form.is_valid() and form2.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-admin')
    return render(request,'school/admin_update_admin.html',context=mydict)



#for teacher sectionnnnnnnn by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers = models.TeacherExtra.objects.all()
    teacher_groups = {}
    for teacher in teachers:
        teacher_groups[teacher.id] = teacher.groups.all()
    return render(request,'school/admin_view_teacher.html',{'teachers':teachers, 'teacher_groups':teacher_groups})


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1 = TeacherUserForm()
    form2 = TeacherExtraForm()
    mydict = {'form1': form1, 'form2': form2}

    if request.method == 'POST':
        form1 = TeacherUserForm(request.POST)
        form2 = TeacherExtraForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.set_password(user.password)
            user.save()

            teacher_extra = form2.save(commit=False)
            teacher_extra.user = user
            teacher_extra.status = True
            teacher_extra.save()

            teacher_group, created = Group.objects.get_or_create(name='TEACHER')
            teacher_group.user_set.add(user)

            selected_groups = form2.cleaned_data.get('groups', None)
            if selected_groups:
                for group in selected_groups:
                    teacher_extra.groups.add(group)

                    # Add the teacher_extra to the selected group
                    group.teacherextra_set.add(teacher_extra)

            return HttpResponseRedirect(reverse('admin-teacher'))

    groups = models.Group.objects.all()
    mydict['groups'] = groups

    return render(request, 'school/admin_add_teacher.html', context=mydict)


@login_required(login_url="login")
@user_passes_test(is_admin)
def update_teacher_view(request, pk):
    teacher_extra = models.TeacherExtra.objects.get(id=pk)
    user = models.User.objects.get(id=teacher_extra.user_id)

    form1 = forms.TeacherUserForm(instance=user)
    form2 = forms.TeacherExtraForm(instance=teacher_extra)
    mydict = {'form1': form1, 'form2': form2}

    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST, instance=user)
        form2 = forms.TeacherExtraForm(request.POST, instance=teacher_extra)

        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.set_password(user.password)
            user.save()

            teacher_extra = form2.save(commit=False)
            teacher_extra.user = user
            teacher_extra.status = True
            teacher_extra.save()

            # Remove the teacher from the current groups
            current_groups = teacher_extra.groups.all()
            for group in current_groups:
                group.teacherextra_set.remove(teacher_extra)

            selected_groups = form2.cleaned_data.get('groups', None)
            if selected_groups:
                for group in selected_groups:
                    teacher_extra.groups.add(group)

                    # Add the user to the selected group
                    group.teacherextra_set.add(teacher_extra)

            return redirect('admin-view-teacher')

    return render(request, 'school/admin_update_teacher.html', context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_teacher_from_University_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


#for student by admin


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    groups = models.Group.objects.all()
    context = {
        'students': students,
        'groups': groups,
    }
    return render(request,'school/admin_view_student.html',context)


@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_student_from_University_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')

@login_required(login_url="login")
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'school/admin_update_student.html',context=mydict)




#attendance related viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_attendance_view(request):
    groups=models.Group.objects.all()
    return render(request,'school/admin_attendance.html',{'groups':groups})


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_take_attendance_view(request, lv):
    group = models.Group.objects.get(name=lv)
    students = models.StudentExtra.objects.filter(cl=group)
    activities = models.Activities.objects.filter(group=group).select_related('module', 'duration')

    if request.method == 'POST':
        date = request.POST.get('date')
        attendance_data = []
        error_messages = []

        for student in students:
            activity_id = request.POST.get(f'activity_{student.id}')
            present_status = request.POST.get(f'attendance_{student.id}', 'absent')

            # Retrieve the activity object for the current student
            activity = activities.get(id=activity_id)

            # Check if attendance already exists for this student, activity, and date
            if models.Attendance.objects.filter(student=student, activity=activity, date=date).exists():
                error_messages.append(f'Attendance already marked for {student.get_name} for this activity on the selected date.')

            attendance_data.append(models.Attendance(
                cl=group,
                date=date,
                present_status=present_status,
                student=student,
                activity=activity,
            ))

        if error_messages:
            for error in error_messages:
                messages.error(request, error)
            return redirect('admin-take-attendance', lv=lv)

        models.Attendance.objects.bulk_create(attendance_data)
        messages.success(request, 'Attendance recorded successfully.')
        return redirect('admin-take-attendance', lv=lv)

    context = {
        'students': students,
        'group': group,
        'activities': activities,
    }

    return render(request, 'school/admin_take_attendance.html', context)


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_attendance_view(request, cl):
    group = models.Group.objects.get(name=cl)
    students = models.StudentExtra.objects.filter(cl=group)
    activities = models.Activities.objects.filter(group=group).select_related('module', 'duration')

    if request.method == 'POST':
        date = request.POST.get('date')
        attendance_data = models.Attendance.objects.filter(date=date, cl=group)
        context = {
            'group': group,
            'date': date,
            'attendance_data': attendance_data,
        }
        return render(request, 'school/admin_view_attendance_page.html', context)

    form = forms.AskDateForm()
    context = {
        'students': students,
        'group': group,
        'activities': activities,
        'form': form,
    }
    return render(request, 'school/admin_view_attendance_ask_date.html', context)
#group related view by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_group(request):
    return render(request, 'school/admin-group.html')


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_group_view(request):
    form=forms.Groups()
    if request.method=='POST':
        form=forms.Groups(request.POST)
        if  form.is_valid():
            
            Group=form.save()
            Group.save()

        return HttpResponseRedirect('admin-group')
    return render(request,'school/admin_add_group.html',{'form':form})


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_group_view(request):
    groups=models.Group.objects.all()
    return render(request,'school/admin_view_group.html',{'groups':groups})

@login_required(login_url="login")
@user_passes_test(is_admin)
def update_group_view(request,pk):
    group=models.Group.objects.get(id=pk)
    form=forms.Groups(instance=group)
    mydict={'form':form}
    if request.method=='POST':
        form=forms.Groups(request.POST,instance=group)
        if  form.is_valid():
            Group=form.save()
            Group.save()
            return redirect('admin-view-group')
    return render(request,'school/admin_update_group.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_group_from_University_view(request,pk):
    group=models.Group.objects.get(id=pk)
    group.delete()
    return redirect('admin-view-group')
#notice related viewsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_room_view(request):
    form=forms.Rooms()
    if request.method=='POST':
        form=forms.Rooms(request.POST)
        if  form.is_valid():
            
            Room=form.save()
            Room.save()

        return HttpResponseRedirect('admin-add-room')
    return render(request,'school/admin_add_room.html',{'form':form})


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_room_view(request):
    rooms = models.room.objects.all()
    return render(request,'school/admin_view_classrooms.html',{'rooms':rooms})

@login_required(login_url="login")
@user_passes_test(is_admin)
def update_room_view(request,pk):
    rooms = models.room.objects.get(id=pk)
    form=forms.Rooms(instance=rooms)
    mydict={'form':form}
    if request.method=='POST':
        form=forms.Rooms(request.POST,instance=rooms)
        if  form.is_valid():
            rooms=form.save()
            rooms.save()
            return redirect('admin-view-room')
    return render(request,'school/admin_update_classrooms.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_room_from_University_view(request,pk):
    rooms=models.room.objects.get(id=pk)
    rooms.delete()
    return redirect('admin-view-room')


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_duration_module(request):
    return render(request, 'school/admin-duration-module.html')



@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_day_view(request):
    form=forms.Days()
    
    if request.method=='POST':
        form=forms.Days(request.POST)
        if  form.is_valid():
            Day=form.save()
            Day.save()

        return HttpResponseRedirect('admin-add-days')
    return render(request,'school/admin_add_days.html',{'form':form})

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_day_view(request):
    days = models.Days.objects.order_by('order')
    return render(request, 'school/admin_view_days.html', {'days': days})



@login_required(login_url="login")
@user_passes_test(is_admin)
def update_day_view(request,pk):
    days = models.Days.objects.get(id=pk)
    form=forms.Days(instance=days)
    mydict={'form':form}
    if request.method=='POST':
        form=forms.Days(request.POST,instance=days)
        if  form.is_valid():
            days=form.save()
            days.save()
            return redirect('admin-view-days')
    return render(request,'school/admin_update_days.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_day_from_University_view(request,pk):
    days=models.Days.objects.get(id=pk)
    days.delete()
    return redirect('admin-view-days')




@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_module_view(request):
    form=forms.Modules()
    if request.method=='POST':
        form=forms.Modules(request.POST)
        if  form.is_valid():
            Module=form.save()
            Module.save()
        return HttpResponseRedirect('admin-add-module')
    return render(request,'school/admin_add_module.html',{'form':form})

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_module_view(request):
    module = models.Module.objects.all()
    return render(request,'school/admin_view_module.html',{'module':module})

@login_required(login_url="login")
@user_passes_test(is_admin)
def update_module_view(request,pk):
    module = models.Module.objects.get(id=pk)
    form=forms.Modules(instance=module)
    mydict={'form':form}
    if request.method=='POST':
        form=forms.Modules(request.POST,instance=module)
        if  form.is_valid():
            module=form.save()
            module.save()
            return redirect('admin-view-module')
    return render(request,'school/admin_update_module.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_module_from_University_view(request,pk):
    module=models.Module.objects.get(id=pk)
    module.delete()
    return redirect('admin-view-module')




@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_duration_view(request):
    form = DurationForm()
    if request.method == 'POST':
        form = DurationForm(request.POST)
        if form.is_valid():
            duration = form.save(commit=False)
            duration.name = form.cleaned_data['name']
            duration.start_time = form.cleaned_data['start_time']
            duration.end_time = form.cleaned_data['end_time']
            duration.save()
            return HttpResponseRedirect('admin-add-duration')
    return render(request, 'school/admin_add_duration.html', {'form': form})

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_duration_view(request):
    duration = models.Duration.objects.all()
    return render(request,'school/admin_view_duration.html',{'duration':duration})

@login_required(login_url="login")
@user_passes_test(is_admin)
def update_duration_view(request,pk):
    duration = models.Duration.objects.get(id=pk)
    form=forms.DurationForm(instance=duration)
    mydict={'form':form}
    if request.method=='POST':
        form=forms.DurationForm(request.POST,instance=duration)
        if  form.is_valid():
            duration=form.save()
            duration.save()
            return redirect('admin-view-duration')
    return render(request,'school/admin_update_duration.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_duration_from_University_view(request,pk):
    duration=models.Duration.objects.get(id=pk)
    duration.delete()
    return redirect('admin-view-duration')



@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_Activities(request):
    return render(request, 'school/admin-Activities.html')

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_Activities_view(request):
    form = Activities()
    if request.method == 'POST':
        form = Activities(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
            return HttpResponseRedirect('admin-add-Activities')
    return render(request, 'school/admin_add_Activities.html', {'form': form})

    
@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_Activities_view(request):
    activities = models.Activities.objects.all()
    teachers = models.TeacherExtra.objects.all()  # Retrieve id and name only
    durations = models.Days.objects.all()
    groups = models.Group.objects.all()

    context = {
        'activities': activities,
        'teachers': teachers,
        'durations': durations,
        'groups': groups,
    }
    return render(request, 'school/admin_view_Activities.html', context)

@login_required(login_url="login")
@user_passes_test(is_admin)
def update_Activities_view(request,pk):
    Activities = models.Activities.objects.get(id=pk)
    form=forms.Activities(instance=Activities)
    mydict={'form':form}
    if request.method=='POST':
        form=forms.Activities(request.POST,instance=Activities)
        if  form.is_valid():
            Activities=form.save()
            Activities.save()
            return redirect('admin-view-Activities')
    return render(request,'school/admin_update_Activities.html',context=mydict)



@login_required(login_url="login")
@user_passes_test(is_admin)
def delete_Activities_from_University_view(request,pk):
    Activities=models.Activities.objects.get(id=pk)
    Activities.delete()
    return redirect('admin-view-Activities')


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name 
            form.save()
            return redirect('admin-dashboard')
    return render(request,'school/admin_notice.html',{'form':form})




#for TEACHER  LOGIN    SECTIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN



def admin_teacher_view(request):
    return render(request,'school/admin_teacher.html')

    
@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    teacher = models.TeacherExtra.objects.get(user=request.user)
    activity = models.Activities.objects.all().filter(teacher=teacher).count()
    groups = teacher.groups.all().count()
    notice=models.Notice.objects.all()
    mydict={
        'activity':activity,
        'groups':groups,
        'mobile':teacherdata[0].mobile,
        'date': teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_view_mygroup_view(request):
    teacher = models.TeacherExtra.objects.get(user=request.user)
    groups = teacher.groups.all().distinct()
    return render(request, 'school/teacher_view_mygroup.html', {'groups': groups})


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_view_myactivity_view(request):
    teacher = models.TeacherExtra.objects.get(user=request.user)
    activities = models.Activities.objects.filter(teacher=teacher)
    groups = models.Group.objects.filter(activities__in=activities).distinct().values('id', 'name', 'level')
    modules = models.Module.objects.filter(activities__in=activities).distinct().values_list('name', flat=True)

    return render(request, 'school/teacher_view_myactivity.html', {
        'activities': activities,
        'groups': groups,
        'modules': modules
    })







@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    teacher = models.TeacherExtra.objects.get(user=request.user)
    groups = teacher.groups.all()
    return render(request,'school/teacher_attendance.html',{'groups':groups})


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request, lv):
    teacher = models.TeacherExtra.objects.get(user=request.user)
    group = models.Group.objects.get(name=lv)
    students = models.StudentExtra.objects.filter(cl=group)
    activities = models.Activities.objects.filter(group=group, teacher=teacher).select_related('module', 'duration')

    if request.method == 'POST':
        date = request.POST.get('date')
        attendance_data = []
        error_messages = []

        for student in students:
            activity_id = request.POST.get(f'activity_{student.id}')
            present_status = request.POST.get(f'attendance_{student.id}', 'absent')

            # Retrieve the activity object for the current student
            activity = activities.get(id=activity_id)

            # Check if attendance already exists for this student, activity, and date
            if models.Attendance.objects.filter(student=student, activity=activity, date=date).exists():
                error_messages.append(f'Attendance already marked for {student.get_name} for this activity on the selected date.')

            attendance_data.append(models.Attendance(
                cl=group,
                date=date,
                present_status=present_status,
                student=student,
                activity=activity,
            ))

        if error_messages:
            for error in error_messages:
                messages.error(request, error)
            return redirect('teacher-take-attendance', lv=lv)

        models.Attendance.objects.bulk_create(attendance_data)
        messages.success(request, 'Attendance recorded successfully.')
        return redirect('teacher-take-attendance', lv=lv)

    context = {
        'students': students,
        'group': group,
        'activities': activities,
    }

    return render(request, 'school/teacher_take_attendance.html', context)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request, cl):
    group = models.Group.objects.get(name=cl)
    students = models.StudentExtra.objects.filter(cl=group)
    activities = models.Activities.objects.filter(group=group).select_related('module', 'duration')

    if request.method == 'POST':
        date = request.POST.get('date')
        attendance_data = models.Attendance.objects.filter(date=date, cl=group)
        context = {
            'group': group,
            'date': date,
            'attendance_data': attendance_data,
        }
        return render(request, 'school/teacher_view_attendance_page.html', context)

    form = forms.AskDateForm()
    context = {
        'students': students,
        'group': group,
        'activities': activities,
        'form': form,
    }
    return render(request, 'school/teacher_view_attendance_ask_date.html', context)

@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'school/teacher_notice.html',{'form':form})

#FOR STUDENT AFTER THEIR Loginnnnnnnnnnnnnnnnnnnnn

@login_required(login_url="login")
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    
    mydict={
        'group': studentdata[0].cl,
        'mobile':studentdata[0].mobile,
        'level': studentdata[0].lv,
        'notice':notice
    }
    return render(request,'school/student_dashboard.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_student)
def student_attendance_view(request):
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            student = models.StudentExtra.objects.filter(user=request.user).first()
            if student is not None:
                attendance_data = models.Attendance.objects.filter(date=date, student=student)
                return render(request, 'school/student_view_attendance_page.html', {'attendance_data': attendance_data, 'date': date, 'student': student})
    return render(request, 'school/student_view_attendance_ask_date.html', {'form': form})

@login_required(login_url="login")
@user_passes_test(is_student)
def student_activity_view(request):
    student = models.StudentExtra.objects.get(user=request.user)
    group = student.cl
    activities = models.Activities.objects.filter(group=group)
    teachers = models.TeacherExtra.objects.filter(activities__in=activities).distinct()
    modules = models.Module.objects.filter(activities__in=activities).distinct().values_list('name', flat=True)
    durations = models.Days.objects.all()

    return render(request, 'school/student-activity.html', {
        'activities': activities,
        'teachers': teachers,
        'modules': modules,
        'durations': durations,
    })
