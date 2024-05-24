"""
views.py

Authors: Omer Junedi, Saad Babar, Saif Siddiqui
Created: May 15, 2024
Description: Defines django view that deals with POST requests sent from frontend to add solved 
problems by user and updates the database.

Related Files:
    content.js: sends requests to views.py
"""



# Create your views here.
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from testdb.models import User, Submissions
from testdb.api.algorithm import SM2



@csrf_exempt
def add_problem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        problem = data.get('problem')
        difficulty = data.get('difficulty')
        accepted: bool  = data.get('accepted')

        user, created = User.objects.get_or_create(username=username)
        problem = Submissions.objects.create(
            user=user, problem=problem, difficulty=difficulty, accepted=accepted)

        print(username)
        print(problem)
        print(difficulty)

        return JsonResponse({
            "status": "success this is coming from views.py",
            "username": username,
            "problem": problem,
            "difficulty": difficulty,
            "accepted": accepted
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def get_all_submissions(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        username = data.get('username')
        user = User.objects.get(username=username)
        # might have to convert problems to json friendly data type
        problems = user.problems.all()

        solver = SM2(problems, username)
        grouped_problems = solver.group_problems()
        print(grouped_problems)

        for problem in grouped_problems:
            for p in problem:
                print(p.user, p.problem, p.timestamp)


        # converts QuerySet to List by evaluating all queries
        problems = list(problems)
        #print(problems)

        problems_json = serializers.serialize('json', problems)

        #print(json.dumps(problems_json, indent=2))
        # reccomendations = run_algorithm(problems)
        return HttpResponse(
             problems_json, content_type='application/json'
        )
