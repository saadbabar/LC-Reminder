from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    username = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return self.username
    
class Problem(models.Model):
    problem_name = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return self.problem_name
    
class Submissions(models.Model):
    id = models.AutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.problem.problem_name + " - " + self.username.username
    

