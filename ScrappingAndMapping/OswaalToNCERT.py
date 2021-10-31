#to get this thing running "pip install -U sentence-transformerspip install -U sentence-transformers"
# reference
# https://www.sbert.net/docs/installation.html

import glob
import csv
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd
from tqdm import tqdm

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
            answers.append(row[2])
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
            questions.append(row[1])
    return questions



def main(bookName, qType, k=5):

    #output rows contain: Question, Answer, Top 5 matches
    outputRows=[]
    totalNumberOfUnits = 4
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
        if qType == "l":
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
            # print("\n\n======================\n\n")
            # print("Question: ",OswaalUnitQuestionText[questionIndex] )
            # print("Query: ", query)
            # print("\nTop 5 most similar sentences in corpus:")
            
            resultRow.append(OswaalUnitQuestionText[questionIndex])
            resultRow.append(query)

            

            for score, idx in zip(top_results[0], top_results[1]):
                # print(NCERTUnitText[idx], "(Score: {:.4f})".format(score))
                resultRow.append(NCERTUnitText[idx])
                #resultRow.append("{:.4f}".format(score))
            
            questionIndex=questionIndex+1
            outputRows.append(resultRow)
    print(len(outputRows), len(outputRows[0]))
    return outputRows


if __name__=="__main__":
    k = 5
    cols = ['question', 'answer'] + ['context_' + str(i+1) for i in range(k)]

    for bookName in tqdm(['SS10', 'SS10_2', 'SS10_3']):
        for qType in tqdm(['l', 's', 'vs']):
            df = pd.DataFrame(main(bookName, qType, k), columns=cols)
            df.to_csv(bookName + '_' + qType + '.csv', index=False)
