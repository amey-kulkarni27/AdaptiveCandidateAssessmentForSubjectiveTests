import re

qtypes = ["Very Short", "Short", "Long"]
searchphrases = [qt +  "Answer Type Questions\nQ." for qt in qtypes]
textfile = open('SS_10.txt', 'r')
text = textfile.read()
textfile.close()
for i in range(len(searchphrases)-1):
    phr = searchphrases[i]
    pattern = re.compile(phr)
    for m in pattern.finditer(text):
        start_pos = m.start()
print(len("Very Short Answer Type Questions\nQ."))