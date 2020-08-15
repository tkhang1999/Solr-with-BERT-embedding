import pandas as pd
import pysolr
from sentence_transformers import SentenceTransformer

PRE_TRAINED_MODEL = 'bert-base-nli-stsb-mean-tokens'

# Read reviews data
reviews = pd.read_csv("configs/foodhunter_reviews.csv")

# Encode reviews to BERT embeddings
corpus = reviews['content']
embedder = SentenceTransformer(PRE_TRAINED_MODEL)
corpus_embeddings = embedder.encode(corpus)

# Convert embedding to vector
vectors = []
for embedding in corpus_embeddings:
    vector = []
    for i in range(len(embedding)):
        vector.append(str(i) + "|" + str(embedding[i]))
    vectors.append(vector)

vectors = [' '.join(vector) for vector in vectors]

# Data to be added to Solr
data = [{"id": rid, "content": rev, "vector": vec} for rid, rev, vec in zip(reviews['id'], reviews['content'], vectors)]

# Add data to Solr with core 'bert'
solr = pysolr.Solr('http://localhost:8983/solr/bert', always_commit=True)
print(solr.add(data))
