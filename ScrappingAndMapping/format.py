import json
import pandas as pd
from tqdm import tqdm

books = ['SS10_l', 'SS10_vs', 'SS10_2_vs', 'SS10_2_l', 'SS10_3_s', 'SS10_s', 'SS10_3_vs', 'SS10_3_l', 'SS10_2_s']
paths = ['SS10_l.csv', 'SS10_vs.csv', 'SS10_2_vs.csv', 'SS10_2_l.csv', 'SS10_3_s.csv', 'SS10_s.csv', 'SS10_3_vs.csv', 'SS10_3_l.csv', 'SS10_2_s.csv']

books = books[2:]
paths = paths[2:]

data = dict()
data['data'] = []
data['version'] = '3.1'

id = 1
for book, path in tqdm(zip(books, paths)):
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