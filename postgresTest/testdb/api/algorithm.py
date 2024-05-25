from math import ceil
import json
import random
import datetime
from itertools import groupby
from operator import attrgetter
from testdb.models import User, Submissions, Problems
from django.db.models import QuerySet
'''
algorithm.py
Authors: Omer Junedi, Saad Babar, Saif Siddiqui
Description: Spaced Repitition Algorithm implementation

https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert#

Notes: Based on above reading, I think we should implement the SM-2 (or a variation of)
algorithm to start off, but eventually should transition to FSRS (perhaps give the user
a choice for what algorithm they want). I've spoken to people who've used both and
apparently FSRS is much better based in practice.
'''

'''
Description of Algorithm:
    Where I(i) represents the interval employed for the i-th review.
    I(1) := 1
    I(2) := 6
    for n > 2, I(n) = I(n-1) * EF
        ° EF -- Ease Factor, with initial value of 2.5
        ° After each review, newEF = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
            ° newEF — the post-review updated value of the Ease Factor
            ° q — the quality grades of review, ranging from 0 - 5. If it's >= 3, it means the learner remembered, and if it's < 3,
            the learner forgot.

    If the learner forgets, the interval for the question-answer pair will be reset to I(1) with the same EF.
    0: "Total blackout", complete failure to recall the information.
    1: Incorrect response, but upon seeing the correct answer it felt familiar.
    2: Incorrect response, but upon seeing the correct answer it seemed easy to remember.
    3: Correct response, but required significant effort to recall.
    4: Correct response, after some hesitation.
    5: Correct response with perfect recall.

OJ's Notes 5/16:

    - Based on q < 3 case, we need to track rejected submissions not just accepted ones however it might not be relevant for the
    first (or even second) time a problem is solved since I(1) = 1. This would require us to change our problems table in the
    database to additionally store a submission result.
OJ's Notes 5/21:
    - Difficulty of {1, 2, 3, 4, 5} needs to be mapped to {3, 4, 5}, and incorrect submissions need to be mapped to {0, 1, 2}
    {1, 2} -> 5
    {3} -> 4
    {4, 5} -> 3
    Not sure how to do it for incorrect submissions because we only have information that it was not accepted, no idea how to tell
    if they were somewhat close or not (could use language models; vector embeddings for solutions then compare using something like cosine similarity?)
    For now given the difficulty of problem on leetcode we can map accordingly;
    Easy -> 2
    Medium -> 1
    Hard -> 0
    Logic being you were probabaly closer to solving the problem if its an easier problem, doensn't really make sense but we need something for now
    Can either store difficulty of problem in database or find some file online that has all LC problems with difficulties

'''

class SM2:

    def __init__(self,user, problem_name):
        '''
        '''
        self.submissions= user.submissions.all()
        self.user = user
        self.problem_name = problem_name
        self.username = user.username
        self.grouped_problems = []
        self.CONVERSIONS_CORRECT = {
            1: 3,
            2: 3,
            3: 4,
            4: 5,
            5: 5
        }
        self.CONVERSIONS_WRONG = {
            3: 0,
            2: 1,
            1: 2
        }


        print("SM2 Constructor")

    def group_problems(self):
        self.submissions= self.submissions.order_by('problem')
        grouped_problems = []
        for key, group in groupby(self.submissions, key=attrgetter('problem')):
            grouped_problems.append(list(group))
        self.grouped_problems = grouped_problems
        return grouped_problems

    def initialize_problem(self, submission: Submissions):
        problem_name = submission.problem
        try:
            Problems.objects.get(problem=problem_name)
        except:
            print(f'{problem_name} does not exist')
            Problems.objects.create(user_id=submission.user_id, problem=problem_name, interval=1, repetitions=0, EF=2.5)

    #don't need this function, but keeping it for now
    def update_problem_data(self):

        x = self.group_problems()
        submissions_for_given_problem = list(self.submissions.filter(problem__iexact=self.problem_name))
        print(self.problem_name)
        print(submissions_for_given_problem)
        for submission in submissions_for_given_problem:
            p, created = Problems.objects.get_or_create(user_id=submission.user_id, problem=submission.problem)
            print(p)

        print("update_problem_data function")
        #print(self.grouped_problems)
        for group in x:
            # only want to update the problem that just submitted
            if group[0].problem == self.problem_name:
                for submission in group:
                    p, created = Problems.objects.get_or_create(user_id=submission.user_id, problem=submission.problem)
                    # print(created)
                    if submission.accepted:

                        if p.repetitions == 0:
                            p.interval = 1
                        elif p.repetitions == 1:
                            p.interval = 2
                        else:
                            p.interval = round(p.interval * p.EF)


                        p.repetitions += 1
                        quality = self.CONVERSIONS_CORRECT.get(submission.difficulty, 4)
                        newEF = p.EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
                        newEF = max(newEF, 1.3)
                        p.EF = newEF
                    else:
                        p.repetitions = 0
                        p.interval = 1

                    p.save()
                break
    def update_priorities(self, submission):
        '''
        takes most recent submission and updates interval for given problem
        '''
        p, created = Problems.objects.get_or_create(user_id=submission.user_id, problem=submission.problem)
        # print(created)
        if submission.accepted:

            if p.repetitions == 0:
                p.interval = 1
            elif p.repetitions == 1:
                p.interval = 6
            else:
                p.interval = ceil(p.interval * p.EF)


            p.repetitions += 1
            quality = self.CONVERSIONS_CORRECT.get(submission.difficulty, 4)
        else:
            p.repetitions = 0
            p.interval = 1
            with open('problemlist.json') as f:
                d = json.load(f)
                for problem in d["stat_status_pairs"]:
                    if problem['stat']['question__title_slug'] == submission.problem:
                        quality = self.CONVERSIONS_WRONG.get(problem['difficulty'])
                        break
            quality = random.randint(1, 3)

        newEF = p.EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        newEF = max(newEF, 1.3)
        p.EF = newEF
        p.save()


    def get_recommendations(self, num_problems=5):
        '''
        returns `num_problems` most recent problems to review determined by SM-2
        should only be called after `update_priorities`
        '''

        # 1. For each problem get the most recent submission
        # 2. add the interval time to the timestamp of the most recent submission
        # 3. sort and return first x htems

        problems: QuerySet = Problems.objects.all()
        idk = []

        for problem in problems:
            submission = Submissions.objects.filter(problem=problem.problem).latest("timestamp")
            date_to_review = submission.timestamp + datetime.timedelta(days=problem.interval)
            idk.append((problem, date_to_review))

        def idk_key(t):
            return t[1]

        idk.sort(key=idk_key)
        print(f'full sorted list {idk}')
        return [p[0].problem for p in idk[:num_problems + 1]]



    def SuperMemo2(self, problem, quality):
        '''
       given history of answers for some given problem, returns the number of days until problem should be seen again
        '''
        pass

def main():
    print("Hello, World")

if __name__ == "__main__":
    main()
