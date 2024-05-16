from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from testdb.models import User, Problem

@csrf_exempt
def add_problem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        problem_name = data.get('problem_name')
        difficulty = data.get('difficulty')

        user, created = User.objects.get_or_create(username=username)
        problem = Problem.objects.create(user=user, problem_name=problem_name, difficulty=difficulty)

        print(username)
        print(problem_name)
        print(difficulty)

        return JsonResponse({'status': 'success', "username": username, "problem_name": problem_name, "difficulty": difficulty})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)