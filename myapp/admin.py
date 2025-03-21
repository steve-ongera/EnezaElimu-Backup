from django.contrib import admin
from .models import *

@admin.register(EnrolledSubject)
class EnrolledSubjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'date_enrolled')
    list_filter = ('term__year', 'term__name', 'subject')
    search_fields = ('student__name', 'student__admission_number', 'subject__name', 'term__name')

    # Optional: For ordering
    ordering = ('student', 'term__year', 'term__name', 'subject')

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('term', 'amount_required')
    search_fields = ('term__name', 'term__year')
    list_filter = ('term__year',)

# Fee Payment Admin
@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'amount_paid', 'payment_date', 'receipt_number', 'get_balance')
    search_fields = ('student__name', 'term__name', 'receipt_number')
    list_filter = ('term__year', 'payment_date')

    def get_balance(self, obj):
        return obj.balance
    get_balance.short_description = 'Balance'

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

admin.site.register(Profile)
admin.site.register(Activity)
admin.site.register(Message)
admin.site.register(NewsUpdate)