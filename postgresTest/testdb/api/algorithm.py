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
from itertools import groupby
from operator import attrgetter
from testdb.models import User, Submissions, Problems

class SM2:

    def __init__(self, problems, username):
        self.problems = problems
        self.username = username


    def group_problems(self):
        self.problems = self.problems.order_by('problem')
        grouped_problems = []
        for key, group in groupby(self.problems, key=attrgetter('problem')):
            grouped_problems.append(list(group))
        return grouped_problems

    def initialize_problem(self, problem):

        if problem not in self.problem_data:
            self.problem_data[problem] = {
                'interval': 1,
                'EF': 2.5,
                'repetitions': 0
            }
    def update_problem_data(self, problem, quality):
        data = self.problem_data[problem]
        if quality >= 3:

            data['repetitions'] += 1
            if data['repetitions'] == 1:
                data['interval'] = 1
            elif data['repetitions'] == 2:
                data['interval'] = 6
            else:
                data['interval'] = round(data['interval'] * data['EF'])


            data['EF'] = data['EF'] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            if data['EF'] < 1.3:
                data['EF'] = 1.3

        else:
            data['repetitions'] = 0
            data['interval'] = 1

        self.problem_data[problem] = data

    def SuperMemo2(self, problem, quality):
        '''
       given history of answers for some given problem, returns the number of days until problem should be seen again
        '''
        self.initialize_problem(problem)
        self.update_problem_data(problem, quality)
        return self.problem_data[problem]['interval']


def main():
    print("Hello, World")

if __name__ == "__main__":
    main()
