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

OJ's Notes 5/16:
    
    - Based on q < 3 case, we need to track rejected submissions not just accepted ones however it might not be relevant for the 
    first (or even second) time a problem is solved since I(1) = 1. This would require us to change our problems table in the
    database to additionally store a submission result. 
    -  

'''
class SM2:

    def __init__(self):
        pass



def main():
	print("Hello, World")

if __name__ == "__main__":
	main()
