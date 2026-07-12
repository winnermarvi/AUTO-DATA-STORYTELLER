from sentence_transformers import SentenceTransformer
import copy
from huggingface_hub import login
from src.config import HF_TOKEN

login(token=HF_TOKEN)

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(knowledge):

    texts = [document["content"] for document in knowledge]

    embeddings = model.encode(texts)

    knowledge_with_embeddings = []

    for document, embedding in zip(knowledge, embeddings):

        new_document = copy.deepcopy(document)
        new_document["embedding"] = embedding

        knowledge_with_embeddings.append(new_document)

    return knowledge_with_embeddings




def generate_query_embedding(question):

    embedding_question = model.encode(question)

    return embedding_question