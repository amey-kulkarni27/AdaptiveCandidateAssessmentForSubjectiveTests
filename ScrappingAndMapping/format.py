import json
import pandas as pd
from tqdm import tqdm
import os

paths = [f for f in os.listdir() if f.endswith('.csv')]
books = [f[:-4] for f in paths]

dev_paths = ['SS10_l.csv', 'S8_val.csv', 'S8_s.csv', 'B11_hots.csv', 'S9_vs.csv']
dev_books = [f[:-4] for f in dev_paths]

data = dict()
data['data'] = []
data['version'] = '3.1'

id = 1
for book, path in tqdm(zip(dev_books, dev_paths)):
    book_dict = dict()
    book_dict['title'] = book
    book_dict['paragraphs'] = []

    csv_data = pd.read_csv(path)

    for index, row in csv_data.iterrows():
        para_dict = dict()
        para_dict['context'] = str(row['context'])
        para_dict['qas'] = []
        para_dict['qas'].append({'answers': [{'answer_start':0, 
                                            'text': str(row['answer'])
                                            }],
                                'question': str(row['question']), 
                                'id': str(id)
                                })
        id += 1
        book_dict['paragraphs'].append(para_dict)

    data['data'].append(book_dict)

with open("dev.json", "w") as outfile:
    json.dump(data, outfile)

train_paths = [f for f in paths if f not in dev_paths]
train_books = [f[:-4] for f in train_paths]

data = dict()
data['data'] = []
data['version'] = '3.1'

id = 1
for book, path in tqdm(zip(train_books, train_paths)):
    book_dict = dict()
    book_dict['title'] = book
    book_dict['paragraphs'] = []

    csv_data = pd.read_csv(path)

    for index, row in csv_data.iterrows():
        para_dict = dict()
        para_dict['context'] = str(row['context'])
        para_dict['qas'] = []
        para_dict['qas'].append({'answers': [{'answer_start':0, 
                                            'text': str(row['answer'])
                                            }],
                                'question': str(row['question']), 
                                'id': str(id)
                                })
        id += 1
        book_dict['paragraphs'].append(para_dict)

    data['data'].append(book_dict)

with open("train.json", "w") as outfile:
    json.dump(data, outfile)