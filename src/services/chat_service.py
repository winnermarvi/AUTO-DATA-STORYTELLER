#from src.chat.context_builder import build_context
from src.llm.chat_prompt import chat_prompt_builder
from src.llm.narrative_generator import generate_narrative
from src.rag.knowledge_builder import build_knowledge
from src.rag.embedding_service import generate_embeddings
from src.rag.faiss_index import build_faiss_index
from src.rag.retriever import retrieve
from src.rag.context_injector import build_context
from src.analytics.query_classifier import is_analytics_question
from src.analytics.intent_detector import detect_intent
from src.analytics.column_matcher import match_columns
from src.analytics.pandas_executor import execute_query
from src.analytics.explanation_service import explain_result
from src.analytics.validation import validate_intent


def generate_chat_response(df,analysis,question,conversation_history):

    if is_analytics_question(question):

        intent_raw = detect_intent(question)

        intent = match_columns(intent_raw,df.columns.tolist())

        validation = validate_intent(intent, df)

        if not validation["valid"]:
            return {
                "narrative": validation["message"]
            }

        result = execute_query(df,intent)

        chat_response = explain_result(intent,result)

    else:

        knowledge = build_knowledge(analysis)

        knowledge_documents = generate_embeddings(knowledge)

        index = build_faiss_index(knowledge_documents)

        retrieved_documents = retrieve(question,index,knowledge_documents)
        
        context = build_context(retrieved_documents)

        chat_prompt = chat_prompt_builder(context,conversation_history,question)

        chat_response = generate_narrative(chat_prompt)

    return chat_response