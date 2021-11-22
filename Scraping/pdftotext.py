# Run from python file location
import os
folder = "Ps12/"
ctr = 1
for filename in os.listdir(folder):
    fpath = folder + filename
    os.system("pdftotext " + fpath + " " + folder + str(ctr) + ".txt")
    ctr += 1