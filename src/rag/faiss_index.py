import faiss
import numpy as np

def build_faiss_index(knowledge_document):

    embeddings = []

    embeddings = [document["embedding"] for document in knowledge_document]
    
    embeddings = np.array(embeddings,dtype=np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index