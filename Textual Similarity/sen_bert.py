import torch
import transformers

# Medium Article: https://towardsdatascience.com/bert-for-measuring-text-similarity-eec91c6bf9e1

sentences = [
    "This is a sentence is a truth.",
    "This, too is a sentence.",
    "Is this supposed to be a question?",
]

tokeniser = transformers.AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
bert_model = transformers.AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

token_ids = []

# token_masks will be set only where the words are defined
token_masks = []

encode_len = 128
for sentence in sentences:
    tokens = tokeniser.encode_plus(sentence, max_length=encode_len,
    truncation=True, padding='max_length', return_tensors='pt')
    # Padding of max length adds zeroes to the end in each embedding, so they have the same length
    token_ids.append(tokens['input_ids'][0])
    token_masks.append(tokens['attention_mask'][0])

# Convert list of tensors to a 2-D tensor
token_ids = torch.stack(token_ids)
token_masks = torch.stack(token_masks)
# print(token_ids.shape) # -> (N, encode_len)

# Create a dictionary as required by BERT
tokens['input_ids'] = token_ids
tokens['attention_mask'] = token_masks

# Run the given tokens through the BERT model
output_dict = bert_model(**tokens)
print(output_dict.keys())