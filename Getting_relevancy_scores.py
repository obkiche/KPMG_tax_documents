import pandas as pd

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_score(s1):
# Two lists of sentences

    #s1 = ['brusselse overlijden driejarige fiscale behoud begroting belast familiale gunstregime decujus kader bedoeld gaan wetboek regering vervuld bekomen gebleven periode voorwaarden financien overdracht zoals hoofdstedelijke aanving']
    s2 = ['belasting fiscaliteit aanslagjaar inkomsten']

    #Compute embedding for both lists
    embeddings1 = model.encode(s1, convert_to_tensor=True)
    embeddings2 = model.encode(s2, convert_to_tensor=True)

    #Compute cosine-similarits
    cosine_scores = float(util.cos_sim(embeddings1, embeddings2))

    #Output the pairs with their score
    cosine_scores = ("{:.3f}".format(cosine_scores))
    return cosine_scores