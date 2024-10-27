# models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    score = models.IntegerField()  # Score to map to specific personality types

    def __str__(self):
        return f"{self.question.text} - {self.text}"

class TestResult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personality_type = models.CharField(max_length=50)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.personality_type}"

class Response(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    value = models.TextField()  # Store the answer value (e.g., "yes" or "no")

    def __str__(self):
        return f"{self.question.text} - {self.value}"
