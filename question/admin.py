# admin.py
from django.contrib import admin
from .models import Question, Choice, TestResult , Response

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(TestResult)
admin.site.register(Response)

