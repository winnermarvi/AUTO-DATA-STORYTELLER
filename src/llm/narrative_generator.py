from groq import Groq
from src.config import GROQ_API_KEY


def generate_narrative(prompt):

    try:

        client = Groq(
            api_key=GROQ_API_KEY
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return {
            "narrative": response.choices[0].message.content,
            "model": "llama-3.3-70b-versatile"
        }

    except Exception as e:

        return {
            "narrative": f"LLM generation failed: {str(e)}",
            "model": "llama-3.3-70b-versatile"
        }