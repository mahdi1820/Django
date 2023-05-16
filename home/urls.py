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
    
    path('admin-add-room', views.admin_add_room_view,name='admin-add-room'),
    path('admin-view-room', views.admin_view_room_view,name='admin-view-room'),
    path('delete-room-from-University/<int:pk>', views.delete_room_from_University_view,name='delete-room-from-University'),
    path('update-room/<int:pk>', views.update_room_view,name='update-room'),

    path('admin-duration-module', views.admin_duration_module,name='admin-duration-module'),
    path('admin-add-days', views.admin_add_day_view,name='admin-add-days'),
    path('admin-view-days', views.admin_view_day_view,name='admin-view-days'),
    path('delete-days-from-University/<int:pk>', views.delete_day_from_University_view,name='delete-days-from-University'),
    path('update-days/<int:pk>', views.update_day_view,name='update-days'),


    path('admin-add-module', views.admin_add_module_view,name='admin-add-module'),
    path('admin-view-module', views.admin_view_module_view,name='admin-view-module'),
    path('delete-module-from-University/<int:pk>', views.delete_module_from_University_view,name='delete-module-from-University'),
    path('update-module/<int:pk>', views.update_module_view,name='update-module'),


    path('admin-add-duration', views.admin_add_duration_view,name='admin-add-duration'),
    path('admin-view-duration', views.admin_view_duration_view,name='admin-view-duration'),
    path('delete-duration-from-University/<int:pk>', views.delete_duration_from_University_view,name='delete-duration-from-University'),
    path('update-duration/<int:pk>', views.update_duration_view,name='update-duration'),


    path('admin-Activities', views.admin_Activities,name='admin-Activities'),
    path('admin-add-Activities', views.admin_add_Activities_view,name='admin-add-Activities'),
    path('admin-view-Activities', views.admin_view_Activities_view,name='admin-view-Activities'),
    path('delete-Activities-from-University/<int:pk>', views.delete_Activities_from_University_view,name='delete-Activities-from-University'),
    path('update-Activities/<int:pk>', views.update_Activities_view,name='update-Activities'),

    path('admin-notice', views.admin_notice_view,name='admin-notice'),


    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
    path('teacher-view-mygroup', views.teacher_view_mygroup_view,name='teacher-view-mygroup'),
    path('teacher-view-myactivity', views.teacher_view_myactivity_view,name='teacher-view-myactivity'),

    path('teacher-attendance', views.teacher_attendance_view,name='teacher-attendance'),
    path('teacher-take-attendance/<str:lv>', views.teacher_take_attendance_view,name='teacher-take-attendance'),
    path('teacher-view-attendance/<str:cl>', views.teacher_view_attendance_view,name='teacher-view-attendance'),
    path('teacher-notice', views.teacher_notice_view,name='teacher-notice'),

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-attendance', views.student_attendance_view,name='student-attendance'),
    path('student-activity', views.student_activity_view,name='student-activity'),


]