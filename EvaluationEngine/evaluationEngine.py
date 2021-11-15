from sentence_transformers import SentenceTransformer, util
import torch


def getEvaluation(question, answer, passage, givenAnswer, questionWeight, answerWeight, passageWeight):

    #embedder for mapping  question and given answer
    embedderQ = SentenceTransformer('msmarco-distilbert-cos-v5')

    #embedder for mapping to given answer to answer and passage
    embedderLong = SentenceTransformer('multi-qa-mpnet-base-cos-v1')

    #
    #
    # might also be a good idea to use the newly trained model for this long embedder
    #
    #

    #looking for only the top match
    top_k = 1
    cosScores=[]

    #first set of embeddings (Q to given A)
    questionShortEmbedding = embedderQ.encode(question, convert_to_tensor=True)
    answerShortEmbedding = embedderQ.encode(givenAnswer, convert_to_tensor=True)

    

    shortCosScores = util.pytorch_cos_sim(questionShortEmbedding, answerShortEmbedding)[0]
    topResultShort = torch.topk(shortCosScores, k=top_k)


    for score, idx in zip(topResultShort[0], topResultShort[1]):
        cosScores.append(score)
        #print(score)


    #second set of embeddings (givenA to Ans and passage)

    answerLongEmbedding=embedderLong.encode(answer, convert_to_tensor=True)
    passageLongEmbedding=embedderLong.encode(passage, convert_to_tensor=True)
    givenAnswerLongEmbedding=embedderLong.encode(givenAnswer, convert_to_tensor=True)

    #givenA - > Ans
    ansCosScores = util.pytorch_cos_sim(givenAnswerLongEmbedding, answerLongEmbedding)[0]
    topResultAns = torch.topk(ansCosScores, k=top_k)

    for score, idx in zip(topResultAns[0], topResultAns[1]):
        cosScores.append(score)
        #print(score)

    #givenA - > passage
    passageCosScores = util.pytorch_cos_sim(givenAnswerLongEmbedding, passageLongEmbedding)[0]
    topResultPassage = torch.topk(passageCosScores, k=top_k)

    for score, idx in zip(topResultPassage[0], topResultPassage[1]):
        cosScores.append(score)
        #print(score)
    #calculating weighted score
    finalScoreOfAns=(cosScores[0] * questionWeight + cosScores[1] * answerWeight + cosScores[2] * passageWeight)/ (questionWeight+ answerWeight+ passageWeight)
    return finalScoreOfAns






def main():

    questionWeight= 1
    answerWeight= 10
    passageWeight = 10
    
    question = "What is the instructor's name?"
    answer= "Instructor's name is Glint"
    passage= "Glint was the instructor of the sports accademy. He was specialising in basketball"
    givenAnswer= "The name of the instructor is Glint"
    wrongAnswer= "The name of the instructor is Sasi"
    print("Right>>>>>")
    #getEvaluation(question, answer,passage,givenAnswer, questionWeight,answerWeight,passageWeight)
    print (getEvaluation(question, answer,passage,givenAnswer, questionWeight,answerWeight,passageWeight))
    
    print("Wrong1>>>>>")
    print (getEvaluation(question, answer,passage,wrongAnswer, questionWeight,answerWeight,passageWeight))


    wrongAnswer= "The name of the instructor is Bhaskar"
    print("Wrong2>>>>>")
    print (getEvaluation(question, answer,passage,wrongAnswer, questionWeight,answerWeight,passageWeight))
  
  


if __name__=="__main__":
    main()