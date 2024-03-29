import torch
import transformers
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go

# Medium Article: https://towardsdatascience.com/bert-for-measuring-text-similarity-eec91c6bf9e1

sentences = [
    "This sentence is the truth.",
    "This, too is a sentence.",
    "Is this supposed to be a question?",
    "Apples are cuter than strawberries.",
    "Oranges are more beautiful than mangoes."
]
n = len(sentences)

tokeniser = transformers.AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
bert_model = transformers.AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

token_ids = []

# token_masks will be set only where the words are defined
token_masks = []

encode_len = 128
for sentence in sentences:
    tokens = tokeniser.encode_plus(sentence, max_length=encode_len,
    truncation=True, padding='max_length', return_tensors='pt')
    # Padding of max_length adds zeroes to the end in each sequence of token_ids, so they have the same length
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
# print(output_dict.keys())
# 1: last_hidden_state -> returns the sequence of hidden states at the last layer of the output
# 2: pooler_output -> the last layer after being passed through, for e.g an activation function such as tanh

# BERT has multiple layers, each of which can give some representation, however we want the embeddings from the last layer
embeddings = output_dict['last_hidden_state'] # n x encode_len x 768

# Convert token_masks to have the same dimension as the embeddings
token_masks = token_masks.unsqueeze(-1) # Adds a singleton dimension
token_masks = token_masks.expand(embeddings.shape).float()
# token_masks is now also of dimension n x encode_len x 768

masked_embeddings = embeddings * token_masks

# Now we perform the pooling step

'''
First sum all the masked_embedding values along the 2nd dimension
This will give us a vector of dimension 768 per sentence
After this we have to normalise by the mask weights
'''

# Sum of masked_embeddings
embeddings_sum = torch.sum(masked_embeddings, axis=1)
# Sum of masks, to normalise
mask_sums = torch.sum(token_masks, axis=1)
# Avoid divide by zero
mask_sums = torch.clamp(mask_sums, min=1e-9)
# Finally, pooling step to get the dense similarity matrices
pooled = embeddings_sum / mask_sums

# Finding similarity of two sentences using cosine similarity

# Convert Pytorch Tensor to numpy array
similarity_matrix = pooled.detach().numpy()

# Finiding the cosine similarity between any two sentences is the same as taking the normalised dot product between any two rows of similarity_matrix
i = 0
j = 1
print(cosine_similarity([similarity_matrix[i]], [similarity_matrix[j]]))

# Entire similarity matrix, for each pair of sentences
print(cosine_similarity(similarity_matrix, similarity_matrix))

fig = go.Figure(data=go.Heatmap(
          x=['s[0]', 's[1]', 's[2]', 's[3]', 's[4]'],
          y=['s[0]', 's[1]', 's[2]', 's[3]', 's[4]'],
          z = cosine_similarity(similarity_matrix, similarity_matrix),
          type = 'heatmap',
          colorscale = 'Agsunset'))

fig.update_layout(font_size=14)
fig.show()
