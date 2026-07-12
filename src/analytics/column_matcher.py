from src.llm.narrative_generator import generate_narrative
import json


def match_columns(intent, columns):

    prompt = f"""
    You are a column matching system.

    Your task is to match the requested column names to the closest matching
    column names from the available dataset columns.

    Available Columns:
    {columns}

    Requested Intent:
    {json.dumps(intent, indent=2)}

    Rules:
    - Match ONLY from the available columns.
    - Keep the operation unchanged.
    - If target_column is null, return null.
    - If group_by is null, return null.
    - Return ONLY valid JSON.
    - Do not explain.
    - Do not use markdown.

    Expected Output:
    {{
        "operation": "...",
        "target_column": "...",
        "group_by": "..."
    }}
    """

    response = generate_narrative(prompt)

    response_text = response["narrative"].strip()
    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")

    matched_intent = json.loads(response_text)

    return matched_intent