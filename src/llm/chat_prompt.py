def chat_prompt_builder(context,conversation_history,question):

    """
    conversation_history = [
    {"role": "user", "content": "Summarize the dataset."},
    {"role": "assistant", "content": "The dataset contains 5000 customer records..."},
    {"role": "user", "content": "What are the main drivers of churn?"}
]
    """

    history = ""

    if len(conversation_history) > 0:
        for message in conversation_history:
            history += f"{message['role'].title()}: {message['content']}\n"
    else:
        history += f"No conversation yet"

    prompt = f"""
        You are an AI Business Analyst.

        Your responsibility is to answer questions using ONLY the analysis provided below.

        If the answer is not contained in the provided analysis, clearly state that the information is not available in the current analysis. Do not invent information or perform new analysis.

        ========================================
        DATASET ANALYSIS
        ========================================

        {context}

        ========================================
        CONVERSATION HISTORY
        ========================================

        {history}

        ========================================
        CURRENT USER QUESTION
        ========================================

        {question}
        """
    
    return prompt