import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import string
import re
import os
import csv

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
url_base = 'https://byjus.com/ncert-solutions-class'
classes = [str(i) for i in range(1, 4)]
subjects = ['social-science-history', 'social-science-geography', 'science', 'english', 'civics']
for cls in classes:
    rel_path = cls
    if not os.path.exists(rel_path):
        os.mkdir(rel_path)
    for subject in subjects:
        rel_path = cls + '/' + subject
        if not os.path.exists(rel_path):
            os.mkdir(rel_path)
        parent_url = url_base + '-' + cls + '-' + subject
        page = requests.get(parent_url, headers=headers)
        if page.status_code == 404:
            # print("Page " + cls + " " + subject + " Does Not Exist")
            continue
        try:
                soup = BeautifulSoup(page.content, 'html.parser')  
        except:
            # print("Page " + cls + " " + subject + " Error")
            continue

        tables = soup.findChildren('table')
        if len(tables) == 0:
            continue
        my_table = tables[0]
        rows = my_table.findChildren(['th', 'tr'])
        c_num = 0
        for row in rows:
            c_num += 1
            content = ""
            cells = row.findChildren('td')
            if len(cells) > 1:
                continue
            for cell in cells:
                row_val = cell.string
                # print(row_val)
                # row_val = (row_val.translate(str.maketrans('', '', string.punctuation))).lower()
                # row_val = row_val.translate(str.maketrans('', '', '-'))
                if row_val == 0:
                    continue
                try:
                    row_val = re.sub(r'[^\w\s]','',row_val).lower()
                except:
                    continue
                # print(row_val)
                # print('\n\n')
                row_val = row_val.split()
                print(row_val)
                try:
                    ind = row_val.index("chapter")
                except:
                    print(parent_url, chapter_suffix)
                    continue
                chapter_suffix = '-'.join(row_val[ind:])

                chapter_url = parent_url + '-' + chapter_suffix
                chapter_page = requests.get(chapter_url, headers=headers)
                if chapter_page.status_code == 404:
                    print("chapter_page " + chapter_suffix + " Does Not Exist")
                    continue
                try:
                        chapter_soup = BeautifulSoup(chapter_page.content, 'html.parser')  
                except:
                    print("chapter_page " + chapter_suffix + " Error")
                    continue

                article_content = chapter_soup.find('article',attrs={"id" : re.compile("post-[d]*")}).findAll(['p', 'h1', 'h2', 'h3', 'h4'])
                
                for row in article_content:
                    content += row.text
                    content += '\n'
                    # print(row.text)
            with open('./{}.txt'.format(rel_path + '/' + str(c_num)), mode='w', encoding='utf-8') as file:
                file.write(content)
