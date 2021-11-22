import pickle

pkl_file = open("tree.pkl", "rb")
data_struct = pickle.load(pkl_file)
pkl_file.close()
hardest = data_struct['swise_hardest']['SS']
print(hardest)
print(data_struct['tree']['SS'][hardest].head())