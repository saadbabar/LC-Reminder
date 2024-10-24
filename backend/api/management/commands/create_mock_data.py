from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import UserProblemData
import random

class Command(BaseCommand):
    help = 'Creates mock data for testing the API'

    def handle(self, *args, **kwargs):
        # Create test users
        users = []
        for i in range(3):
            username = f'testuser{i+1}'
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('testpassword')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created test user: {username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Using existing test user: {username}'))
            users.append(user)

        # Create mock UserProblemData entries
        problem_titles = ['two-sum', 'reverse-integer', 'palindrome-number', 'roman-to-integer', 'longest-common-prefix']
        sentiments = ['Positive', 'Neutral', 'Negative']

        for user in users:
            for title in problem_titles:
                UserProblemData.objects.create(
                    user=user,
                    problem_identifier=title,
                    priority_score=random.randint(0, 10),
                    user_sentiment=random.choice(sentiments)
                )
                self.stdout.write(self.style.SUCCESS(f'Created UserProblemData for {user.username}: {title}'))

        self.stdout.write(self.style.SUCCESS('Mock data creation completed'))