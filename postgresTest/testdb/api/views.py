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
from testdb.models import User, Submissions, Problems
from testdb.api.algorithm import SM2



@csrf_exempt
def add_problem(request):
    '''
    adds submission to Submissions Table and problem to Problems if doesn't exist already
    and then updates next interval for given problem
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        problem_name = data.get('problem_name')
        difficulty = data.get('difficulty')
        accepted: bool  = data.get('accepted')

        user, created = User.objects.get_or_create(username=username)
        submission = Submissions.objects.create(
            user=user, problem=problem_name, difficulty=difficulty, accepted=accepted)

        solver = SM2(user, problem_name)
        solver.update_priorities(submission)
        print(f'recommendations are {solver.get_recommendations()}')
        #print(username)
        #print(problem_name)
        #print(difficulty)

        return JsonResponse({
            "status": "success this is coming from views.py",
            "username": username,
            "problem_name": problem_name,
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
        problem_name = data.get('problem_name')
        # might have to convert problems to json friendly data type
        problems = user.submissions.all()
        print(data)
        print("views.py get_all_submissions")
        print(user)
        print(problem_name)

        solver = SM2(user, problem_name)
        solver.update_problem_data()
        # grouped_problems = solver.group_problems()

        # print(grouped_problems)

        # for problem in grouped_problems:
        #     for p in problem:
        #         print(p.user, p.problem_name, p.timestamp)


        # converts QuerySet to List by evaluating all queries
        problems = list(problems)
        problems_json = serializers.serialize('json', problems)

        #print(json.dumps(problems_json, indent=2))
        # reccomendations = run_algorithm(problems)
        return HttpResponse(
             problems_json, content_type='application/json'
        )
