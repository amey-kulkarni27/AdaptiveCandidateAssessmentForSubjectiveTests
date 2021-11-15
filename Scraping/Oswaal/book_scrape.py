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

searchphrases = ["Very Short Answer Type Question", "Short Answer Type Question", "Long Answer Type Question", "Value Based Question", "High Order Thinking Skills (HOTS) Question"]
q_search = re.compile("Q\. \d+")
pg_num1 = re.compile("\[ \d+")
pg_num2 = re.compile("\d+ \]")
textfile = open('S_08.txt', 'r')
lines = textfile.readlines()
ctr = 0
'''
mode denotes what we are currently doing
0 -> haven't found topic yet (beginning of the book)
1 -> search for "Very Short Answer Type", get topic name
2 -> very short question
4 -> 
'''
mode = 0
top_name = ""
top_cnt = 0
rel_path = ""
q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
qctr = 0
for line in lines:
    line = line.rstrip()
    ctr += 1

    # Remove Form Feed character
    line = line.replace('\x0c', '')
    if line == "FORMATIVE":
        break

    if line == "" or any(x.isalpha() for x in line) == False or (line.isdigit() and len(line) == 1) or pg_num1.match(line) or pg_num2.match(line) or line.startswith("Oswaal"):
        if line != "CHAPTER" and line != "MAP WORK" and line != "QUICK REVIEW":  
            continue
    line = re.sub(r'\([^)]*\)', '', line)
    line = re.sub(r'\[[^)]*\]', '', line)

    if mode == 0 and line.startswith("CHAPTER"):
        mode = 1
        top_name = ""

    elif mode == 1:
        if line == "Quick Review":  
            top_name = top_name.strip()
            top_name = top_name.replace(" ", "_")
            rel_path = "8/" + top_name + "/"
            if not os.path.exists(rel_path):
                os.mkdir(rel_path)
            # print(top_name)
            top_name = ""
        elif line.startswith(searchphrases[0]):
            mode = 2
            q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
        elif line.startswith(searchphrases[1]):
            mode = 3
            q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
        elif line.startswith(searchphrases[2]):
            mode = 4
            q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
        elif line.startswith(searchphrases[3]):
            mode = 5
            q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
        elif line.startswith(searchphrases[4]):
            mode = 6
            q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
        else:
            line = re.sub(r'[^\w\s]','',line).lower()
            top_name += " " + line       
    
    elif mode >= 2:
        if q_search.match(line):
            if(len(q_list)) and a:
                a_list.append(ans)
            q = True
            a = False
            qs = line
        elif line.startswith("Ans."):
            if q:
                q_list.append(qs)
            q = False
            a = True
            ans = line
        elif "Question" in line or line.startswith("TOPIC-") or line == "CHAPTER" or line == "MAP WORK" or line == "Formative Assessment":
            if a:
                a_list.append(ans)
            if mode == 2:
                # if not os.path.exists(rel_path+"vs.csv"):
                df, n_q = create_dataframe(q_list, a_list)
                qctr += n_q
                df.to_csv(rel_path+"vs.csv")
            elif mode == 3:
                # if not os.path.exists(rel_path+"s.csv"):
                df, n_q = create_dataframe(q_list, a_list)
                qctr += n_q
                df.to_csv(rel_path+"s.csv")
            elif mode == 4:
                # if not os.path.exists(rel_path+"l.csv"):
                df, n_q = create_dataframe(q_list, a_list)
                qctr += n_q
                df.to_csv(rel_path+"l.csv")
            elif mode == 5:
                # if not os.path.exists(rel_path+"val.csv"):
                df, n_q = create_dataframe(q_list, a_list)
                qctr += n_q
                df.to_csv(rel_path+"val.csv")
            elif mode == 6:
                # if not os.path.exists(rel_path+"hots.csv"):
                df, n_q = create_dataframe(q_list, a_list)
                qctr += n_q
                df.to_csv(rel_path+"hots.csv")
            prev_mode = mode

            if line.startswith("TOPIC-"):
                mode = 1
                top_name = ""
            elif line == "CHAPTER" or line == "":
                mode = 0
                top_name = ""
            elif line == "MAP WORK" or line == "Formative Assessment":
                mode = 0
                top_name = ""
            elif line.startswith(searchphrases[0]):
                mode = 2
            elif line.startswith(searchphrases[1]):
                mode = 3
            elif line.startswith(searchphrases[2]):
                mode = 4
            elif line.startswith(searchphrases[3]): # Value Based
                mode = 5
            elif line.startswith(searchphrases[4]): # HOTS
                mode = 6
            if mode != prev_mode:
                q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
            else:
                qs, ans, q, a = "", "", False, False


        elif q:
            if (line.isupper() and all(x.isalpha() or x.isspace() or x==":" for x in line)):
                continue
            qs += " " + line
        elif a:
            if (line.isupper() and all(x.isalpha() or x.isspace() or x==":" for x in line)):
                continue
            ans += " " + line

textfile.close()
print(qctr)