import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import csv
import time
import random

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
# url = 'https://byjus.com/ncert-solutions-class-9-social-science-geography-chapter-4-climate/'
# url = 'https://byjus.com/ncert-solutions-class-8-social-science-history-chapter-3-ruling-the-countryside/'
url = 'https://byjus.com/ncert-solutions-class-6-social-science-history-chapter-2-from-hunting-gathering-to-growing-food/'
page = requests.get(url, headers=headers)
if page.status_code == 404:
    print("Page Does Not Exist")
try:
        soup = BeautifulSoup(page.content, 'html.parser')  
except:
    print("Page Error")
article_content = soup.find('article',attrs={"id" : re.compile("post-[d]*")}).findAll(['p', 'h1', 'h2', 'h3', 'h4'])
for row in article_content:
    print(row.text)
    print()

# i = 0
# for header in soup.find_all('h2'):
#     nextNode = header
#     print(1)
#     while True:
#         nextNode = nextNode.nextSibling
#         if nextNode is None:
#             break
#         # To check if next sibling is a text node
#         if isinstance(nextNode, NavigableString) and i == 2:
#             print (nextNode.strip())
#             pass
#         # To check if next sibling is an element
#         if isinstance(nextNode, Tag):
#             if nextNode.name == "h2":
#                 i += 1
#                 break
#             if i == 2:
#                 print (nextNode.get_text(strip=True).strip())
#                 pass
# # print(i)