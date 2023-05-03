from django.urls import path 

from . import views



urlpatterns = [
    
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('Admin_SignUp/', views.signup, name='signup'),
    
    path('admin/logout/', views.Logout, name='admin_logout'),
    path('Master/', views.master,name="Master"),
    path('Doctorat/', views.master,name="Doctorat"),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    path('admin-add-admin', views.admin_signup_view,name='admin-add-admin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),   
    path('admin-admin', views.admin_admin_view,name='admin-admin'),
    path('admin-view-admin', views.admin_view_admin_view,name='admin-view-admin'),

    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-add-teacher', views.admin_add_teacher_view,name='admin-add-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    #path('admin-approve-teacher', views.admin_approve_teacher_view,name='admin-approve-teacher'),
    #path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('delete-teacher-from-school/<int:pk>', views.delete_teacher_from_school_view,name='delete-teacher-from-school'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    #path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,name='admin-view-teacher-salary'),


    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('delete-student-from-school/<int:pk>', views.delete_student_from_school_view,name='delete-student-from-school'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    #path('admin-approve-student', views.admin_approve_student_view,name='admin-approve-student'),
    #path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
    #path('admin-view-student-fee', views.admin_view_student_fee_view,name='admin-view-student-fee'),


    path('admin-attendance', views.admin_attendance_view,name='admin-attendance'),
    path('admin-take-attendance/<str:cl>', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance/<str:cl>', views.admin_view_attendance_view,name='admin-view-attendance'),

    path('admin-group', views.admin_group,name='admin-group'),
    path('admin-add-group', views.admin_add_group_view,name='admin-add-group'),
    path('admin-view-group', views.admin_view_group_view,name='admin-view-group'),

    #path('admin-fee', views.admin_fee_view,name='admin-fee'),
    #path('admin-view-fee/<str:cl>', views.admin_view_fee_view,name='admin-view-fee'),

    path('admin-notice', views.admin_notice_view,name='admin-notice'),



    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-attendance', views.teacher_attendance_view,name='teacher-attendance'),
    path('teacher-take-attendance/<str:cl>', views.teacher_take_attendance_view,name='teacher-take-attendance'),
    path('teacher-view-attendance/<str:cl>', views.teacher_view_attendance_view,name='teacher-view-attendance'),
    path('teacher-notice', views.teacher_notice_view,name='teacher-notice'),

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-attendance', views.student_attendance_view,name='student-attendance'),




    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
]