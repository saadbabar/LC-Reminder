"""
views.py

Authors: Omer Junedi, Saad Babar, Saif Siddiqui
Created: May 15, 2024
Description: Defines django view that deals with POST requests sent from frontend to add solved 
problems by user and updates the database.

Related Files:
    content.js: sends requests to views.py
"""


from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from testdb.models import User, Problem

@csrf_exempt
def add_problem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        problem_name = data.get('problem_name')
        difficulty = data.get('difficulty')
        accepted: bool  = data.get('accepted') 

        user, created = User.objects.get_or_create(username=username)
        problem = Problem.objects.create(
            user=user, problem_name=problem_name, difficulty=difficulty, accepted=accepted)

        print(username)
        print(problem_name)
        print(difficulty)

        return JsonResponse({
            "status": "success this is coming from views.py",
            "username": username,
            "problem_name": problem_name,
            "difficulty": difficulty,
            "accepted": accepted
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def get_all_problems(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        username = data.get('username')
        user = User.objects.get(username=username)
        # might have to convert problems to json friendly data type
        problems = user.problems.all()
        problems_json = serializers.serialize('json', problems)

        print(problems_json)
        # reccomendations = run_algorithm(problems)
        
        return HttpResponse(
             problems_json, content_type='application/json'
        )




