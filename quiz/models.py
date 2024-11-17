from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    options = models.JSONField()  # Store multiple-choice options
    correct_option = models.CharField(max_length=1, default='A')  # Provide a default value
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Add this line to link Answer to Question
    is_correct = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user} for {self.question}"

class PracticeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    last_practiced = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"History of {self.user}"