from src.llm.narrative_generator import generate_narrative
import json

def detect_intent(question):

    prompt = f"""
        You are an intent detection system.

        Extract:

        - operation
        - target_column
        - group_by

        Return ONLY valid JSON.

        If group_by doesn't exist, return null.
        If target_column doesn't exist, return null.

        Valid operations are ONLY:

        - mean
        - sum
        - count
        - max
        - min

        Mapping rules:
        - average -> mean
        - avg -> mean
        - highest -> max
        - maximum -> max
        - lowest -> min
        - minimum -> min

        Return ONLY one of these operation names.

        Do not explain.
        Do not write markdown.
        Do not answer the user's question.

        Question:

        {question}
    """

    response = generate_narrative(prompt)

    response_text = response["narrative"].strip()

    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")

    try:

        intent = json.loads(response_text)

    except Exception as e:

        print(f"Error Occured {e}")

    return intent