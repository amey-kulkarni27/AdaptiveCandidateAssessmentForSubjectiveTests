import os
import pandas as pd
import re

def rem_q(s):
    if ~isinstance(s, str):
        return s
    s = re.sub(r'Q\. \d+\. ', '', s)
    return s

def rem_a(s):
    if ~isinstance(s, str):
        return s
    s = re.sub(r'Ans\. ', '', s)
    return s

def clean(s):
    if ~isinstance(s, str):
        return s
    s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'\[[^)]*\]', '', s)
    s = re.sub(r'\d marks each', '', s)
    s = re.sub(r'\d mark each', "", s)
    s = re.sub(r'\d.\d=\d', "", s)
    return s

folder = "10_1/"
for topic in os.listdir(folder):
    for filename in os.listdir(folder + topic + "/"):
        if filename.endswith(".csv"):
            csvname = folder + topic + "/" + filename
            df = pd.read_csv(csvname)
            print(csvname)
            df['questions'] = df['questions'].apply(rem_q)
            df['answers'] = df['answers'].apply(rem_a)
            df['questions'] = df['questions'].apply(clean)
            df['answers'] = df['answers'].apply(clean)
            df.to_csv(csvname)