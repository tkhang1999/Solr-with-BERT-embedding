import pysolr
from sentence_transformers import SentenceTransformer
import constants


embedder = SentenceTransformer(constants.PRE_TRAINED_MODEL)
solr = pysolr.Solr(constants.SOLR_URL)

def semantic_search(query):
    # Encode query to BERT embedding
    query_embedding = [str(emb) for emb in embedder.encode(query)[0]]
    # Convert embedding to query vector
    query_vector = ','.join(query_embedding)
    # Make a search query with the query vector to
    # obtain results with similarity scores of all sentences in the database
    query_search = "{!vp f=vector vector=\"%s\"}" % (query_vector)
    fl_search = "id,content,score"

    search_results = solr.search(query_search, **{
        'fl': fl_search
    }, rows=600)
    # Format search results
    results = [{'id': result['id'], 'content': result['content'], \
        'score': result['score']} for result in search_results]

    return results

if __name__ == '__main__':
    query = 'delicious food'
    results = semantic_search(query)

    # Display top results with their similarity score
    print('\nQuery: ', query)
    print('\nTop %d semantic search results:' % constants.TOP_RESULTS)

    for result in results[:constants.TOP_RESULTS]:
        print(result['content'][0], '(Score: %.4f)' % result['score'])
