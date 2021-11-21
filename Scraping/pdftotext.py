import os
folder = "SS9/"
for chapter in os.listdir(folder):
    ctr = 1
    for filename in os.listdir(folder + chapter + "/"):
        fpath = folder + chapter + "/" + filename
        os.system("pdftotext " + fpath + " " + folder + chapter + "/" + str(ctr) + ".txt")
        ctr += 1