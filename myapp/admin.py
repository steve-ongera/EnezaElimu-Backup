from django.contrib import admin
from .models import Class_of_study, Subject, Student, Term, CAT

admin.site.register(Class_of_study)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Term)
admin.site.register(CAT)