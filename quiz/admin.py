# Register your models here.

from django.contrib import admin
from .models import Question, Answer, PracticeHistory

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(PracticeHistory)
