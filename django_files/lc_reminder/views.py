import json
from django.http import HttpResponse


# Create
def add_problem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        problem_name = data.get('problem_name')
        difficulty = data.get('difficulty')
        accepted: bool  = data.get('accepted')


# Read
def get_problems(request):
    pass

# Update
def modify_problem(request):
    pass

# Delete
def delete_problem(request):
    pass
