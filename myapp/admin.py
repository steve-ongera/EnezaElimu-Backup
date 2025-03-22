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

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at', 'views', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('views', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ExaminationSession)
class ExaminationSessionAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date')
    list_filter = ('year',)
    search_fields = ('year',)

@admin.register(ExamTimeTable)
class ExamTimeTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'session', 'start_date', 'end_date')
    list_filter = ('session__year',)
    search_fields = ('name', 'session__year')


class TermReporting(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='term_reports')
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    reporting_date = models.DateField()
    
    # Simple reporting status
    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late Reporting'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REPORTED')
    
    # Optional notes field
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'term']
        ordering = ['-term__year', 'term__name', 'reporting_date']
    
    def __str__(self):
        return f"{self.student.name} - {self.term} ({self.get_status_display()})"
    
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