from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProblemData
from .serializer import RecentSubmissionSerializer, UserProblemDataSerializer

@api_view(['POST'])
def create_recent_submission(request):
    serializer = RecentSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        # For testing, let's use the first user in the database
        user = UserProblemData.objects.first().user if UserProblemData.objects.exists() else None
        if user and serializer.validated_data['status_display'] == 'Accepted':
            problem_identifier = serializer.validated_data['title_slug']
            user_problem_data, created = UserProblemData.objects.get_or_create(
                user=user,
                problem_identifier=problem_identifier,
                defaults={
                    'priority_score': 0,
                    'user_sentiment': 'Neutral'
                }
            )
            if not created:
                user_problem_data.priority_score = max(0, user_problem_data.priority_score - 1)
                user_problem_data.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_problem_data(request):
    # For testing, let's return data for all users
    user_problem_data = UserProblemData.objects.all()
    serializer = UserProblemDataSerializer(user_problem_data, many=True)
    return Response(serializer.data)