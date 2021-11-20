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

searchphrases = ["Very Short Answer", "Short Answer", "DONTUSEShort Answers – II", "Long Answer", "Value Based", "High Order Thinking", "Practical Based"]
q_search = re.compile("Q\. \d+")


folder = "biology/"
qctr = 0
ctr = 1
for chapter in os.listdir(folder):
    csv_folder = folder + chapter + "/CSVs/"
    if not os.path.exists(csv_folder):
        os.mkdir(csv_folder)
    filenum = 1
    while True:
        txt = folder + chapter + "/" + str(filenum) + ".txt"
        # print(txt)
        if os.path.exists(txt) == False:
            break
        filenum += 1
        textfile = open(txt, 'r')
        lines = textfile.readlines()
        line_num = 0
        first_line = ""
        q_list, a_list, qs, ans, q, a = [], [], "", "", False, False
        for line in lines:
            line = line.rstrip()
            # Remove Form Feed character
            line = line.replace('\x0c', '')
            line = re.sub(r'\[[^)]*\]', '', line)
            if line_num == 0:
                first_line = line
                line_num += 1
                continue
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
            elif q:
                if (line.isupper() and all(x.isalpha() or x.isspace() or x==":" for x in line)):
                    continue
                qs += " " + line
            elif a:
                if (line.isupper() and all(x.isalpha() or x.isspace() or x==":" for x in line)):
                    continue
                ans += " " + line
        if ans != "":
            a_list.append(ans)
        df, n_q = create_dataframe(q_list, a_list)
        qctr += n_q

        if first_line.startswith(searchphrases[0]):
            df.to_csv(csv_folder + "vs-" + str(ctr) + ".csv")
        elif first_line.startswith(searchphrases[1]):
            df.to_csv(csv_folder + "s-" + str(ctr) + ".csv")
        elif first_line.startswith(searchphrases[3]):
            df.to_csv(csv_folder + "l-" + str(ctr) + ".csv")
        elif first_line.startswith(searchphrases[4]):
            df.to_csv(csv_folder + "val-" + str(ctr) + ".csv")
        elif first_line.startswith(searchphrases[5]):
            df.to_csv(csv_folder + "hots-" + str(ctr) + ".csv")
        elif first_line.startswith(searchphrases[6]):
            df.to_csv(csv_folder + "pb-" + str(ctr) + ".csv")
        else:
            print(first_line)
        ctr += 1
print(qctr)