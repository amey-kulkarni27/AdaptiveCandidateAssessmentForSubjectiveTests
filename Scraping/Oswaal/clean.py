import os
import pandas as pd
import re

def rem_q(s):
    if s == None:
        print("YES")
        return ""
    s = re.sub(r'Q\. \d+\. ', '', s)
    return s

def rem_a(s):
    if s == None:
        print("YES")
        return ""
    s = re.sub(r'Ans\. ', '', s)
    return s

def clean(s):
    if s == None:
        print("YES")
        return ""
    # s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'\[[^)]*\]', '', s)
    s = re.sub(r'\d marks each', '', s)
    s = re.sub(r'\d mark each', "", s)
    s = re.sub(r'\d.\d=\d', "", s)
    return s

folder = "ScrappingAndMapping/OswaalToNCERT/SS10_3/Unit2/topics/"
for topic in os.listdir(folder):
    for filename in os.listdir(folder + topic + "/"):
        if filename.endswith(".csv"):
            csvname = folder + topic + "/" + filename
            df = pd.read_csv(csvname, index_col=[0])
            df.dropna()
            print(csvname)
            df['questions'] = df['questions'].apply(lambda x: rem_q(x))
            df['answers'] = df['answers'].apply(lambda x: rem_a(x))
            df['questions'] = df['questions'].apply(lambda x: clean(x))
            df['answers'] = df['answers'].apply(lambda x: clean(x))
            df.to_csv(csvname, index=False)