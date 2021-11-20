import os
folder = "biology/"
for chapter in os.listdir(folder):
    ctr = 1
    for filename in os.listdir(folder + chapter + "/"):
        fpath = folder + chapter + "/" + filename
        os.system("pdftotext " + fpath + " " + str(ctr) + ".txt")
        ctr += 1