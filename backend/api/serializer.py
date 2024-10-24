from rest_framework import serializers
from .models import SubmissionData, UserProblemData
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SubmissionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionData
        fields = ['id', 'time', 'user_rated_difficulty', 'problem_identifier', 'notes']

class UserProblemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProblemData
        # fields = ['problem_identifier', 'priority_score', 'user_sentiment']
        fields = '__all__'

class RecentSubmissionSerializer(serializers.Serializer):
    lang = serializers.CharField(max_length=50)
    status_display = serializers.CharField(max_length=50)
    timestamp = serializers.DateTimeField()
    title = serializers.CharField(max_length=255)
    title_slug = serializers.CharField(max_length=255)
