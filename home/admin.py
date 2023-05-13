from django.contrib import admin
from .models import Attendance,StudentExtra,TeacherExtra,Notice,Group,AdminExtra,room,Module,Days,Duration,Activities
# Register your models here.

admin.site.site_header = 'FNTIC-UKMO-ADMIN'
admin.site.site_title = 'FNTIC-UKMO'


class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(TeacherExtra, TeacherExtraAdmin)

class AdminExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(AdminExtra, AdminExtraAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['cl','date', 'present_status','activity','student']
admin.site.register(Attendance, AttendanceAdmin)

admin.site.register(Group)

admin.site.register(room)

admin.site.register(Module)


class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ['module','duration', 'classroom','teacher','group']
admin.site.register(Activities,ActivitiesAdmin)

class DurationAdmin(admin.ModelAdmin):
    list_display = ['name','start_time', 'end_time']
admin.site.register(Duration,DurationAdmin)

admin.site.register(Days)
class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)
