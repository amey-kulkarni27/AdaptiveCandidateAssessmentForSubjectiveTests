#to get this thing running "pip install -U sentence-transformerspip install -U sentence-transformers"
# reference
# https://www.sbert.net/docs/installation.html

#in this version the code will return a bridged passage based on the following criteria
# let a, b, c, d, e be the passages returned by the initial semantic search.
#cosine(a)>cosine(b)

# to make more sensible passages, if for any x and y belonging to {a,b,c,d,e}: (x-y)=p<=2, then return x+i terms where i in [0,p] as the passage, otherwise return the passage with the highest cosine similarity

import glob
import csv
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd

# returns the list of files and folders matching the pattern
def fileList(filePattern):
    # print(filePattern)
    return(glob.glob(filePattern))


#returns all the answers as a list.
def csvAnswerAsListFromCSVFile(fileName):
    answers=[]
    with open(fileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        skipHeader=1
        for row in spamreader:
            if(skipHeader == 1):
                skipHeader=0
                continue
            answers.append(row[1])
    return answers

#returns all the question as a list.
def csvQuestionAsListFromCSVFile(fileName):
    questions=[]
    with open(fileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        skipHeader=1
        for row in spamreader:
            if(skipHeader == 1):
                skipHeader=0
                continue
            questions.append(row[0])
    return questions



def getQAPassage(bookName, qType, numUnits, k=5):

    #output rows contain: Question, Answer, Top 5 matches
    outputRows=[]
    totalNumberOfUnits = numUnits
    for unit in range(totalNumberOfUnits):
        filePathRegEx="OswaalToNCERT/" + bookName + "/Unit" + str(unit+1) +"/pdftotext2/*"
        NCERTFileList =fileList(filePathRegEx)

        #holds all the paras in the unit = this will act as corpus.
        NCERTUnitText = []
        for unitChapter in NCERTFileList:
            with open(unitChapter,"r") as chapterText:
                lines=chapterText.readlines()
                #print(lines[0:2])
                NCERTUnitText.extend(lines)       
    
        filePathRegEx= "OswaalToNCERT/" + bookName + "/Unit"+ str(unit+1)+"/topics/*/"+ qType +".csv"
        OswaalCSVFileList = fileList(filePathRegEx)

        #holds all the answers in the unit = this will act as query
        OswaalUnitAnswerText = []
        OswaalUnitQuestionText = []
        for topic in OswaalCSVFileList:
            lines=csvAnswerAsListFromCSVFile(topic)
            OswaalUnitAnswerText.extend(lines)
            lines=csvQuestionAsListFromCSVFile(topic)
            OswaalUnitQuestionText.extend(lines)


        #performing unit wise semantic asymetric search
        #this is the basic model
        #embedder = SentenceTransformer('all-MiniLM-L6-v2')

        #this is the recommended model
        #embedder = SentenceTransformer('msmarco-distilbert-cos-v5')

        #another model that can be used
        if qType == "l" or qType == "val" or qType == "pb" or qType == "hots":
            embedder = SentenceTransformer('multi-qa-mpnet-base-cos-v1')
        else:
            embedder = SentenceTransformer('msmarco-distilbert-cos-v5')

        corpus_embeddings = embedder.encode(NCERTUnitText, convert_to_tensor=True)

        top_k = min(k, len(NCERTUnitText))

        questionIndex=0
        for query in OswaalUnitAnswerText:
            query_embedding = embedder.encode(query, convert_to_tensor=True)

            # We use cosine-similarity and torch.topk to find the highest 5 scores
            cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
            top_results = torch.topk(cos_scores, k=top_k)

            resultRow=[]
            #creating a new result row for holding only one passage
            newResultRow = []
            resultIDs=[]
            # print("\n\n======================\n\n")
            # print("Question: ",OswaalUnitQuestionText[questionIndex] )
            # print("Query: ", query)
            # print("\nTop 5 most similar sentences in corpus:")
            
            resultRow.append(OswaalUnitQuestionText[questionIndex])
            resultRow.append(query)

            newResultRow.append(OswaalUnitQuestionText[questionIndex])
            newResultRow.append(query)
            

            for score, idx in zip(top_results[0], top_results[1]):
                # print(NCERTUnitText[idx], "(Score: {:.4f})".format(score))
                resultRow.append(NCERTUnitText[idx])
                resultIDs.append(idx)
                #resultRow.append("{:.4f}".format(score))
            
            #logic for finding the passage from this.

            tempBucket=[]
            tempBucket.append(resultIDs[0])
            
            #print("Q" + str(questionIndex)+ ":: " + str(tempBucket[0]))
            resultIDs.sort()
            
            for indexOfID in range(0,top_k-1):
                if(resultIDs[indexOfID+1]-resultIDs[indexOfID]<2):
                    tempBucket.append(resultIDs[indexOfID])
                    tempBucket.append(resultIDs[indexOfID]+1)

                elif (resultIDs[indexOfID+1]-resultIDs[indexOfID]<3):
                    tempBucket.append(resultIDs[indexOfID])
                    tempBucket.append(resultIDs[indexOfID]+1)
                    tempBucket.append(resultIDs[indexOfID]+2)

            #now temp bucket might have duplicates. removing duplicates
            tempBucket = list(set(tempBucket))
            tempBucket.sort()
            myPassage = ""
            if tempBucket:
                #this means that our temp bucket is  not empty and has passage with proximity
                #print(tempBucket)
                for paraID in tempBucket:
                    myPassage= myPassage + NCERTUnitText[paraID] + " "
            else:
                #this is due to a change in logic and the following code should never be reached. 
                print("Most cosine val")
                myPassage = resultRow[2]

            newResultRow.append(myPassage)
            #print(myPassage)
            questionIndex=questionIndex+1
            outputRows.append(newResultRow)
            #print(newResultRow)
            #outputRows contain the the Question, Answer, relevent passage.
    print(len(outputRows))
    return outputRows


def main():
    k = 5
    cols = ['question', 'answer', 'context']

    for bookName, numUnits in zip(['B11', 'S8', 'S9', 'S10', 'SS10', 'SS10_2', 'SS10_3'], [1, 1, 1, 1, 4, 4, 4]):
        for qType in ['l', 's', 'vs', 'hots', 'val', 'pb']:
            df = pd.DataFrame(getQAPassage(bookName, qType, numUnits, k), columns=cols)
            df.to_csv(bookName + '_' + qType + '.csv', index=False)

if __name__=="__main__":
    main()