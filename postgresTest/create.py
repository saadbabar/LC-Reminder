import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postgresTest.settings')
django.setup()

from testdb.models import User, Problem
# ^^
# imperative to follow this order of import and setup statements otherwise it won't work

def create_user(username):
	user = User.objects.create(username=username)
	return user


def add_problem(user: User, problem_name, difficulty):
	problem = Problem.objects.create(user=user, problem_name=problem_name, difficulty=difficulty)
	return problem




def main():
	oj = create_user("ojunedi")
	add_problem(oj, 'Two Sum', 1)


if __name__ == "__main__":
	main()
