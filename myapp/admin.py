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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'term', 'date')  # Columns to display in the list
    list_filter = ('term', 'date')            # Add filters by term and date
    search_fields = ('title', 'description')  # Add search functionality
    ordering = ('-date',)      

    

@admin.register(TermReporting)
class TermReportingAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'reporting_date', 'status')
    list_filter = ('term', 'status', 'reporting_date')
    search_fields = ('student__name', 'student__admission_number', 'notes')
    date_hierarchy = 'reporting_date'
    
    # Actions for bulk updates
    actions = ['mark_as_reported', 'mark_as_absent', 'mark_as_late']
    
    def mark_as_reported(self, request, queryset):
        queryset.update(status='REPORTED')
    mark_as_reported.short_description = "Mark selected students as reported"
    
    def mark_as_absent(self, request, queryset):
        queryset.update(status='ABSENT')
    mark_as_absent.short_description = "Mark selected students as absent"
    
    def mark_as_late(self, request, queryset):
        queryset.update(status='LATE')
    mark_as_late.short_description = "Mark selected students as late"

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