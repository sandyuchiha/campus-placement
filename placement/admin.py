from django.contrib import admin
from .models import Student, Company, InterviewQuestion, InterviewResult

admin.site.register(Student)
admin.site.register(Company)
admin.site.register(InterviewQuestion)
admin.site.register(InterviewResult)