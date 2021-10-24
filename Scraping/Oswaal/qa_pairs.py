import re
import os

qtypes = ["Very Short", "Short", "Long"]
searchphrases = [qt +  "Answer Type Questions\nQ." for qt in qtypes]
textfile = open('SS_10.txt', 'r')
# text = textfile.read()
lines = textfile.readlines()
ctr = 0
'''
state denotes what we are currently doing
0 -> haven't found chapter yet (beginning of the book)
1 -> from CHAPTER till syllabus
2 -> search for "Very Short Answer Type"
3 -> short started, very short not ended
4 -> 
'''
state = 0
chp_name = ""
rel_path = ""
for line in lines:
    line = line.rstrip()
    # print(line)
    ctr += 1

    if state == 1:
        if line == "SYLLABUS":
            state = 2
            chp_name = chp_name.strip()
            chp_name = chp_name.replace(" ", "_")
            rel_path = chp_name + "/"
            if not os.path.exists(rel_path):
                os.mkdir(rel_path)
        else:
            line = re.sub(r'[^\w\s]','',line).lower()
            chp_name += " " + line
    if(line == "CHAPTER"):
        state = 1
        chp_name = ""
        
    if ctr > 10000:
        break
textfile.close()
# for i in range(len(searchphrases)-1):
#     phr = searchphrases[i]
#     pattern = re.compile(phr)
#     for m in pattern.finditer(text):
#         start_pos = m.start()