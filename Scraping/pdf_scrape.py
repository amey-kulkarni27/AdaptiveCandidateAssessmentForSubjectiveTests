import re
import os
import pandas as pd

def create_dataframe(qs, ans):
    '''
    Create a dataframe from list of questions and answers
    :param qs -> list of questions
    :param ans -> list of answers

    Return -> pandas dataframe containing qs and ans
    '''
    # print(len(qs), len(ans))
    if len(qs) != len(ans):
        print(len(qs), len(ans))
        # print(qs)
        for i, a in zip([i for i in range (31)], ans):
            print(i+1, a)
    df = pd.DataFrame(
        {'questions': qs,
         'answers': ans
        })
    return df, len(qs)

searchphrases = ["Very Short Answer Type Question", "Short Answer Type Question", "Long Answer Type Question", "Value Based Question", "High Order Thinking Skills (HOTS) Question", "Practical Based Question"]
q_search = re.compile("Q\. \d+")
pg_num1 = re.compile("\[ \d+")
pg_num2 = re.compile("\d+ \]")
textfile = open('S_10.txt', 'r')
lines = textfile.readlines()
ctr = 0

folder = "biology/"
for chapter in os.listdir(folder):
    for filename in os.listdir(folder + chapter + "/"):
        fpath = folder + chapter + "/" + filename