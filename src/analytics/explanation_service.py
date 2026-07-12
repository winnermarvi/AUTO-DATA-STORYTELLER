from src.llm.narrative_generator import generate_narrative


def explain_result(intent, result):

    if hasattr(result, "to_string"):
        result_text = result.to_string()
    else:
        result_text = str(result)

    prompt = f"""
    You are an AI Business Analyst.

    The following analytical query has already been executed.

    Intent:
    {intent}

    Result:
    {result_text}

    Explain the result in clear business language.

    Rules:
    - Do not perform new calculations.
    - Do not invent values.
    - Base your explanation only on the provided result.
    """

    response = generate_narrative(prompt)

    return response