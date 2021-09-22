import json
import queue
import random
from re import sub
import numpy as np

def js_r(filename: str):
    '''
    filename -> name of the json file that contains the questions

    Returns: dictionary containing the questions, subjectwise and difficulty-wise
    '''
    with open(filename) as f_in:
        return json.load(f_in)

def get_q(questions, subject, level, visited):
    '''
    Given a subject and difficulty level, pick a question from the specified category
    Updates visited
    questions -> Python dictionary containing all questions
    subject -> sunject/topic of question
    level -> difficulty of question
    visited -> boolean numpy array denoting which questions have been used so far

    Returns: Question to be asked 
    '''
    q_num = random.choices(np.arange(start=0, stop=len(questions[subject][level])), weights=(1 ^ visited[subject][level]), k=1)[0]
    visited[subject][level][q_num] = 1
    return questions[subject][level][q_num]

def correct(answer):
    '''
    Evaluating answer.
    This will be done using Sentence Bert
    '''
    if answer == 'y' or answer == 'Y':
        return True
    return False

def simulate_exam(n=5):
    '''
    Adaptively generate n questions
    
    n -> Number of questions to be adaptively generated

    Returns: Interactive Exam that chooses the next question according to given response
    '''
    questions = js_r('questions.json')
    visited = dict()
    subjects = list(questions.keys())
    total_questions = 0
    for subject in subjects:
        visited[subject] = dict()
        levels = list(questions[subject].keys())
        for level in levels:
            num_q = len(questions[subject][level])
            visited[subject][level] = np.array([0 for i in range(num_q)])
            total_questions += num_q

    if total_questions < n:
        print("Not enough questions")
        return

    q = queue.Queue(maxsize=len(subjects))
    for subject in random.sample(subjects, len(subjects)):
        q.put(subject)

    # Generate questions
    jump = 0
    level_num = 0
    while(True):
        cur_subject = q.get()
        levels = list(questions[cur_subject].keys())
        while(n > 0):
            cur_level = levels[level_num]
            # If no questions left in this section, change topic but maintain level
            if(sum(visited[cur_subject][cur_level]) == len(questions[cur_subject][cur_level])):
                q.put(cur_subject)
                jump += 1
                # If all questions of this difficulty level have been exhausted, change difficulty level
                if jump == len(subjects):
                    level_num += 1
                    level_num %= len(subjects)
                break
            
            jump = 0
            question = get_q(questions, cur_subject, cur_level, visited)
            n -= 1
            print(question)
            answer = input()
            if correct(answer):
                level_num += 1
                print(level_num)
                if(level_num == len(subjects)):
                    # Change subject and set difficulty to 0
                    q.put(cur_subject)
                    level_num = 0
            else:
                if(sum(visited[cur_subject][cur_level]) == len(questions[cur_subject][cur_level])):
                    q.put(cur_subject)
                    level_num = 0
                    break
        if n <= 0:
            break
    
    

simulate_exam(7)