#from src.chat.context_builder import build_context
from src.llm.chat_prompt import chat_prompt_builder
from src.llm.narrative_generator import generate_narrative
from src.rag.knowledge_builder import build_knowledge
from src.rag.embedding_service import generate_embeddings
from src.rag.faiss_index import build_faiss_index
from src.rag.retriever import retrieve
from src.rag.context_injector import build_context


def generate_chat_response(analysis,question,conversation_history):

    knowledge = build_knowledge(analysis)

    knowledge_documents = generate_embeddings(knowledge)

    index = build_faiss_index(knowledge_documents)

    retrieved_documents = retrieve(question,index,knowledge_documents)
    
    context = build_context(retrieved_documents)

    chat_prompt = chat_prompt_builder(context,conversation_history,question)

    chat_response = generate_narrative(chat_prompt)

    return chat_response