import pandas as pd

df = pd.read_csv("stats.csv")
swise = dict()

for row in range(df.index.size):
    name = (df.iloc[row, 0])
    nlist = name.split("_")
    stype = nlist[0][:2]
    if stype not in swise:
        swise[stype] = 0
    swise[stype] += df.iloc[row, 1]

dfs = pd.DataFrame(list(swise.items()))
dfs.to_csv("swise.csv", index=False)