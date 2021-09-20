import torch
import transformers

sentences = [
    "This is a sentence.",
    "This, too is a sentence.",
    "Is this supposed to be a question?",
]

tokeniser = transformers.AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
model = transformers.AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

token_ids = []
# token_wts will be multiplied during the mean pooling step
token_wts = []

# for sentence in sentences:
