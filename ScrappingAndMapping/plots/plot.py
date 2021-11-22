import pandas as pd

df = pd.read_csv("stats.csv")
cwise = dict()

for row in range(df.index.size):
    name = (df.iloc[row, 0])
    nlist = name.split("_")
    ctype = nlist[0][-2:]
    if ctype not in cwise:
        cwise[ctype] = 0
    cwise[ctype] += df.iloc[row, 1]

dfc = pd.DataFrame(list(cwise.items()))
dfc.to_csv("cwise.csv", index=False)