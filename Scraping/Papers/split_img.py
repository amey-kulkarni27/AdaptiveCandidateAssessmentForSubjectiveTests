import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

subject = "History"
year = "2018"
path = "./" + subject + "/" + year + "/"
num_files = len(os.listdir(path + "Full/"))

for i in range(num_files):
    img = cv2.imread(path + "Full/" + '-' + str(i + 1) + '.png') 
    h, w = img.shape[:2]
    imga = img[0:h, 0:w//2]
    imgb = img[0:h, w//2:w]
    cv2.imwrite(path + "Split/" + str(i + 1) + "_a.png", imga)
    cv2.imwrite(path + "Split/" + str(i + 1) + "_b.png", imgb)
