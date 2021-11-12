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
        # for i, a in zip([i for i in range (31)], ans):
        #     print(i+1, a)
    df = pd.DataFrame(
        {'questions': qs,
         'answers': ans
        })
    return df

subject = "History"
year = "2018"
path = "./" + subject + "/" + year + "/"
textfile = open(path + 'merged.txt', 'r')
lines = textfile.readlines()
ctr = 0
q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
start = False
qnum = 1
for line in lines:
    line = line.rstrip()
    ctr += 1
    line = line.replace('\x0c', '')
    line = re.sub(r'\([^)]*\)', '', line)
    line = re.sub(r'\[[^)]*\]', '', line)
    if line.startswith("www."):
        continue

    if start == False:
        if line.startswith("1."):
            qs = line
            q = True
            start = True
    else:
        if q:
            if line.startswith("Answer"):
                # print(qnum)
                q_list.append(qs)
                qs = ""
                ans = line
                q = False
                a = True
                qnum += 1
            else:
                qs += " " + line
        else:
            if line.startswith(str(qnum) + "."):
                a_list.append(ans)
                ans = ""
                qs = line
                q = True
                a = False
            else:
                ans += " " + line
if ans != "":
    a_list.append(ans)
df = create_dataframe(q_list, a_list)
df.to_csv(path + "qa.csv")

textfile.close()
print(qnum-1)