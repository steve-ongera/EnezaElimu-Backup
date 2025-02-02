from django.contrib import admin
from .models import *

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'teacher_code', 'email', 'phone', 'assigned_class')
    search_fields = ('first_name', 'last_name', 'teacher_code', 'email', 'phone')
    list_filter = ('assigned_class', 'gender', 'department')


admin.site.register(Class_of_study)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Term)
admin.site.register(CAT)


admin.site.register(Staff)
admin.site.register(NonStaff)
admin.site.register(Intern)
admin.site.register(Department)