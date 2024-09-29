from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Problem(models.Model):
    leetcode_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return f"{self.leetcode_id}: {self.title}"

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)
    user_difficulty_level = models.IntegerField()
    status = models.CharField(max_length=50)
    code = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} at {self.submission_time}"

class UserProblemData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    last_reviewed = models.DateTimeField(auto_now=True)
    next_review_date = models.DateTimeField()
    repetition_interval = models.IntegerField(default=1)
    easiness_factor = models.FloatField(default=2.5)
    repetition_count = models.IntegerField(default=1)
    user_difficulty_level = models.IntegerField()

    class Meta:
        unique_together = ('user', 'problem')

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"

    def update_review_data(self, quality):
        MIN_EF = 1.3
        MAX_EF = 2.5

        self.easiness_factor = max(
            MIN_EF,
            self.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        )

        if quality < 3:
            self.repetition_count = 1
            self.repetition_interval = 1
        else:
            if self.repetition_count == 1:
                self.repetition_interval = 1
            elif self.repetition_count == 2:
                self.repetition_interval = 6
            else:
                self.repetition_interval = int(self.repetition_interval * self.easiness_factor)
            self.repetition_count += 1

        self.next_review_date = timezone.now() + timezone.timedelta(days=self.repetition_interval)
        self.save()
