import re
import os

searchphrases = ["Very Short Answer Type Questions", "Short Answer Type Questions", "Long Answer Type Questions"]
q_search = re.compile("Q\. \d+\. ")
textfile = open('SS_10.txt', 'r')
lines = textfile.readlines()
ctr = 0
'''
mode denotes what we are currently doing
0 -> haven't found chapter yet (beginning of the book)
1 -> from CHAPTER till syllabus
2 -> search for "Very Short Answer Type"
3 -> very short question
4 -> 
'''
mode = 0
chp_name = ""
rel_path = ""
q_list = []
a_list = []
qs, ans = "", ""
ch_cnt = 0
for line in lines:
    line = line.rstrip()
    ctr += 1

    if mode == 0 and line == "CHAPTER":
        mode = 1
        chp_name = ""
        nlctr = 0
        ch_cnt += 1
        if ch_cnt == 2:
            break

    if mode == 1:
        if line == "" and nlctr == 0:
            nlctr = 1
        elif line == "" and nlctr == 1:  
            mode = 2
            chp_name = chp_name.strip()
            chp_name = chp_name.replace(" ", "_")
            rel_path = chp_name + "/"
            if not os.path.exists(rel_path):
                os.mkdir(rel_path)
        else:
            line = re.sub(r'[^\w\s]','',line).lower()
            chp_name += " " + line
    
    elif mode == 2:
        if line.startswith(searchphrases[0]):
            mode = 3 # Detected "Very Short Answer Type Questions"
            qs, ans = "", ""
            q, a = False, False
    
    elif mode == 3:
        if q_search.match(line):
            if(len(q_list)):
                a_list.append(ans)
            q = True
            a = False
            qs = line
        elif line.startswith("Ans. "):
            q_list.append(qs)
            q = True
            a = False
            ans = line
        elif line.startswith(searchphrases[1]):
            a_list.append(ans)
            break
        elif q:
            qs += " " + line
        elif a:
            ans += " " + line
        

    if ctr > 10000:
        break

print(q_list)
print(a_list)
textfile.close()
# for i in range(len(searchphrases)-1):
#     phr = searchphrases[i]
#     pattern = re.compile(phr)
#     for m in pattern.finditer(text):
#         start_pos = m.start()