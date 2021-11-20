import pandas as pd
import os

csvs = [f for f in os.listdir() if f.endswith(".csv")]
sizes = []

for c in csvs:
    sizes.append(pd.read_csv(c).index.size)

df = pd.DataFrame()
df['csvs'] = csvs
df['sizes'] = sizes



df.to_csv("stats.csv", index=False)