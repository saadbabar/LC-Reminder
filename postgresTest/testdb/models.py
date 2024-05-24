'''
models.py
Author: Omer Junedi, Saad Babar, Saif Siddiqui
Created: May 15, 2024
Description: Defines the database models
'''

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=80)

    def __str__(self):
        return self.username
    
class Submissions(models.Model):
    '''
     creates relationship b/w User and Submission model using a one-to-many relationship
     i.e one User can have multiple submissions associated with them
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    problem = models.TextField()
    # changing to 1 to 100 for testing purposes
    #TODO: change back
    difficulty = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    # autopopulates with time that object was created
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField()

    def __str__(self):
        return f"{self.problem} - {self.difficulty}"

class Problems(models.Model):
    '''
    Stores all problems and data relevant for spaced repetition algorithm
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    problem = models.TextField()
    interval = models.IntegerField()
    repetitions = models.IntegerField()
    EF = models.FloatField()

    def __str__(self) -> str:
        return f'{self.problem} {self.interval} {self.repetitions} {self.EF}'