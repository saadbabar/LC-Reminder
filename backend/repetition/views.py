from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Problem, Submission, UserProblemData
from .serializers import ProblemSubmissionSerializer, ProblemSerializer, SubmissionSerializer, UserProblemDataSerializer
from django.utils import timezone

# Create your views here.

class AddProblemView(APIView):
    def post(self, request):
        serializer = ProblemSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            problem_name = serializer.validated_data['problem_name']
            difficulty = serializer.validated_data['difficulty']
            accepted = serializer.validated_data['accepted']

            # Get or create user
            user, _ = User.objects.get_or_create(username=username)

            # Get or create problem
            problem, _ = Problem.objects.get_or_create(
                title=problem_name,
                defaults={'difficulty': difficulty, 'url': f'https://leetcode.com/problems/{problem_name}/'}
            )

            # Create submission
            submission = Submission.objects.create(
                user=user,
                problem=problem,
                user_difficulty_level=1,  # You might want to adjust this
                status='Accepted' if accepted else 'Attempted'
            )

            # Update or create UserProblemData
            user_problem_data, created = UserProblemData.objects.get_or_create(
                user=user,
                problem=problem,
                defaults={
                    'next_review_date': timezone.now() + timezone.timedelta(days=1),
                    'user_difficulty_level': 1,  # You might want to adjust this
                }
            )

            if not created:
                # Update existing data
                user_problem_data.last_reviewed = timezone.now()
                user_problem_data.save()

            return Response({'message': 'Problem added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
