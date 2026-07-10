import numpy as np
from src.rag.embedding_service import generate_query_embedding

def retrieve(question, index, knowledge_documents, k=3):

    retrieved_documents = []

    query_embedding = generate_query_embedding(question)

    query_embedding = np.array(query_embedding, dtype=np.float32)

    query_embedding = query_embedding.reshape(1, -1)

    distances, indices = index.search(query_embedding, k)

    for i in indices[0]:

        retrieved_documents.append(knowledge_documents[i])

    return retrieved_documents