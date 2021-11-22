import pandas as pd
import os
import pickle


csvs = [f for f in os.listdir() if f.endswith(".csv")]
qtype_difficulty = {'vs': 1, 's': 2, 'l': 4, 'val': 3, 'hots': 5, 'pb': 4}
swise_easiest = dict()
swise_hardest = dict()
root = dict()
# root[subject] -> root[subject][difficulty] -> list of all questions from given subject at given difficulty

for csv in csvs:
    name_list = csv.split("_")
    subject = name_list[0][:2]
    if subject[1].isdigit():
        subject = subject[0]
    cls = name_list[0][-2:]
    if cls[0].isalpha():
        cls = cls[1]
    cls = int(cls)
    qtype = name_list[-1][:-4]
    if subject not in root:
        root[subject] = dict()
        swise_easiest[subject] = 100
        swise_hardest[subject] = 0

    difficulty = cls + qtype_difficulty[qtype]
    if difficulty < swise_easiest[subject]:
        swise_easiest[subject] = difficulty
    if difficulty > swise_hardest[subject]:
        swise_hardest[subject] = difficulty

    df = pd.read_csv(csv)
    if difficulty not in root[subject]:
        root[subject][difficulty] = pd.DataFrame()
    root[subject][difficulty] = root[subject][difficulty].append(df, ignore_index=True)

data = {'tree': root, 'swise_easiest': swise_easiest, 'swise_hardest': swise_hardest}
pkl_file = open("tree.pkl", "wb")
pickle.dump(data, pkl_file)
pkl_file.close()