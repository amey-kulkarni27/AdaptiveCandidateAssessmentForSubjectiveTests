import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import random

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
url = 'https://byjus.com/ncert-solutions-class-8-social-science-history-chapter-3-ruling-the-countryside/'
page = requests.get(url, headers=headers)
if page.status_code == 404:
    print("Page Does Not Exist")
try:
        soup = BeautifulSoup(page.content, 'html.parser')  
except:
    print("Page Error")
for row in soup.find('article',attrs={"id" : re.compile("post-[d]*")}).findAll('p'):
    print(row.text)