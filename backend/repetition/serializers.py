from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Problem, Submission, UserProblemData

class ProblemSubmissionSerializer(serializers.Serializer):
    username = serializers.CharField()
    problem_name = serializers.CharField()
    difficulty = serializers.CharField()
    accepted = serializers.BooleanField()

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['leetcode_id', 'title', 'difficulty', 'url']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['user', 'problem', 'submission_time', 'user_difficulty_level', 'status', 'code']

class UserProblemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProblemData
        fields = ['user', 'problem', 'last_reviewed', 'next_review_date', 'repetition_interval', 'easiness_factor', 'repetition_count', 'user_difficulty_level']