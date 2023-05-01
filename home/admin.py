from django.contrib import admin
from .models import Attendance,StudentExtra,TeacherExtra,Notice,Group,AdminExtra
# Register your models here.

admin.site.site_header = 'FNTIC-UKMO-ADMIN'
admin.site.site_title = 'FNTIC-UKMO'



# Register your models here. (by sumit.luv)
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
    pass
admin.site.register(Attendance, AttendanceAdmin)

admin.site.register(Group)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)
