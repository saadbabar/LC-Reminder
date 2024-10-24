from django.db import models
from django.contrib.auth.models import User

class SubmissionData(models.Model):
    time = models.DateTimeField()
    user_rated_difficulty = models.IntegerField()
    problem_identifier = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)  # Make notes optional

class UserProblemData(models.Model):
    problem_identifier = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority_score = models.IntegerField()
    user_sentiment = models.CharField(max_length=255)