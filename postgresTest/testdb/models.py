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
    
class Problem(models.Model):

    # creates relationship b/w User and Problem model using a one-to-many relationship
    # i.e one User can have multiple problems associated with them
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    problem_name = models.TextField()

    # could also use models.CharField for the difficulty
    # depending on how we want to represent it 
    # DIFFICULTIES = [
    #     "Very Easy",
    #     "Easy",
    #     "Medium",
    #     "Hard",
    #     "Very Hard"
    # ]
    # difficulty = models.CharField(choices=DIFFICULTIES)

    # difficulty int 1 to 5
    # changing to 1 to 100 for testing purposes
    #TODO: change back
    difficulty = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    #TODO: ADD TIMESTAMP
    # autopopulates with time that object was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.problem_name} - {self.difficulty}"

