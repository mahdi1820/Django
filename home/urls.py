from django.urls import path 

from . import views



urlpatterns = [
    
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    
    path('admin/logout/', views.Logout, name='admin_logout'),
    path('Master/', views.master,name="Master"),
    path('Doctorat/', views.master,name="Doctorat"),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    path('admin-add-admin', views.admin_signup_view,name='admin-add-admin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),   
    path('admin-admin', views.admin_admin_view,name='admin-admin'),
    path('admin-view-admin', views.admin_view_admin_view,name='admin-view-admin'),
    path('delete-admin-from-University/<int:pk>', views.delete_admin_from_University_view,name='delete-admin-from-University'),
    path('update-admin/<int:pk>', views.update_admin_view,name='update-admin'),

    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-add-teacher', views.admin_add_teacher_view,name='admin-add-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('delete-teacher-from-University/<int:pk>', views.delete_teacher_from_University_view,name='delete-teacher-from-University'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('delete-student-from-University/<int:pk>', views.delete_student_from_University_view,name='delete-student-from-University'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),

    path('admin-attendance', views.admin_attendance_view,name='admin-attendance'),
    path('admin-take-attendance/<str:lv>/', views.admin_take_attendance_view,name='admin-take-attendance'),
    path('admin-view-attendance/<str:cl>/', views.admin_view_attendance_view,name='admin-view-attendance'),

    path('admin-group', views.admin_group,name='admin-group'),
    path('admin-add-group', views.admin_add_group_view,name='admin-add-group'),
    path('admin-view-group', views.admin_view_group_view,name='admin-view-group'),
    path('delete-group-from-University/<int:pk>', views.delete_group_from_University_view,name='delete-group-from-University'),
    path('update-group/<int:pk>', views.update_group_view,name='update-group'),
    
    path('admin-notice', views.admin_notice_view,name='admin-notice'),


    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-view-mygroup', views.teacher_view_mygroup_view,name='teacher-view-mygroup'),
    path('teacher-attendance', views.teacher_attendance_view,name='teacher-attendance'),
    path('teacher-take-attendance/<str:lv>', views.teacher_take_attendance_view,name='teacher-take-attendance'),
    path('teacher-view-attendance/<str:cl>', views.teacher_view_attendance_view,name='teacher-view-attendance'),
    path('teacher-notice', views.teacher_notice_view,name='teacher-notice'),

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-attendance', views.student_attendance_view,name='student-attendance'),

]