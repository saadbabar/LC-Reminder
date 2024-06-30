"""
Author: Omer Junedi
Created: May 15, 2024
Description: Sample script for how to use django models to add data to postgres database
"""


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postgresTest.settings')
django.setup()

from testdb.models import User, Submissions
# ^^
# imperative to follow this order of import and setup statements otherwise it won't work

def create_user(username):
	user = User.objects.create(username=username)
	return user


def add_problem(user: User, problem, difficulty):
	problem = Submissions.objects.create(user=user, problem=problem, difficulty=difficulty)
	return problem




def main():
	oj = create_user("ojunedi")
	add_problem(oj, 'Two Sum', 1)


if __name__ == "__main__":
	main()
