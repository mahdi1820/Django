from django.shortcuts import render ,HttpResponseRedirect,redirect,reverse, get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth.decorators import login_required , user_passes_test
from . import forms,models
from django.db.models import Sum 
from django.core.mail import send_mail
from datetime import datetime
from .forms import TeacherUserForm ,TeacherExtraForm
# Create your views here.
@login_required(login_url = 'login')
def home(request):
    return render (request,'home/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        
        user = authenticate(request, username = username ,password = pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password . Please try again.')
    return render (request,'home/Alogin.html')

@login_required(login_url = 'login')
def Logout(request):
    logout(request)
    return redirect('login')  

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url = 'login')
def master(request):
    return render (request,'home/master.html')
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
    elif is_student(request.user):
        return redirect('student-dashboard')

#for dashboard of adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=models.TeacherExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

    groupcount = models.Group.objects.all().count()

    admincount = models.AdminExtra.objects.all().filter(status=True).count()
  
    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,

        'studentcount':studentcount,
        
        'groupcount':groupcount,

        'admincount':admincount,

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

                    # Add the user to the selected group and remove from the default "TEACHER" group
                    group.user_set.add(user)
                    teacher_group.user_set.remove(user)

            return HttpResponseRedirect(reverse('admin-teacher'))

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
    return render(request,'school/admin_view_student.html',{'students':students})


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
        print(form1)
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
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=group
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request,'school/admin_take_attendance.html',{'students':students,'aform':aform})

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_view_attendance_view(request, cl):
    group = models.Group.objects.get(name=cl)
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.filter(date=date, cl=group)
            studentdata = models.StudentExtra.objects.filter(cl=group)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/admin_view_attendance_page.html', {'cl': cl, 'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'school/admin_view_attendance_ask_date.html', {'cl': cl, 'form': form})

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
    return render(request,'home/admin_teacher.html')

    
@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'mobile':teacherdata[0].mobile,
        'date': teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)

@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_view_mygroup_view(request):
    teacher = models.TeacherExtra.objects.get(user=request.user)
    groups = teacher.groups.all()
    return render(request,'school/teacher_view_mygroup.html',{'groups':groups})


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    teacher = models.TeacherExtra.objects.get(user=request.user)
    groups = teacher.groups.all()
    return render(request,'school/teacher_attendance.html',{'groups':groups})


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,lv):
    group = models.Group.objects.get(name=lv)
    students = models.StudentExtra.objects.filter(cl=group)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=group
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'school/teacher_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    group = models.Group.objects.get(name=cl)
    form = forms.AskDateForm()
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            attendancedata = models.Attendance.objects.filter(date=date, cl=group)
            studentdata = models.StudentExtra.objects.filter(cl=group)
            mylist = zip(attendancedata, studentdata)
            return render(request, 'school/teacher_view_attendance_page.html', {'cl': cl, 'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'school/teacher_view_attendance_ask_date.html', {'cl': cl, 'form': form})


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
    studentdata = None  # assign None initially
    if request.method == 'POST':
        form = forms.AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            studentdata = models.StudentExtra.objects.all().filter(user_id=request.user.id).first()
            if studentdata is None:
                # handle case where studentdata is not found
                pass
            else:
                attendancedata = models.Attendance.objects.all().filter(date=date, cl=studentdata.cl)
                mylist = zip(attendancedata, [studentdata])
                return render(request, 'school/student_view_attendance_page.html', {'mylist': mylist, 'date': date})
        else:
            print('form invalid')
    return render(request, 'school/student_view_attendance_ask_date.html', {'form': form})

# for aboutus and contact ussssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form':sub})