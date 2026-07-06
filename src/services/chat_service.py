from src.chat.context_builder import build_context
from src.llm.chat_prompt import chat_prompt_builder
from src.llm.narrative_generator import generate_narrative


def generate_chat_response(analysis,question,conversation_history):

    context = build_context(analysis)

    chat_prompt = chat_prompt_builder(context,conversation_history,question)

    chat_response = generate_narrative(chat_prompt)

    return chat_response