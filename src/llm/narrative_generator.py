from google import genai
from src.config import GEMINI_API_KEY

def generate_narrative(prompt):

    try:

        client = genai.Client(api_key= GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= prompt
        )
        
        return {
            'narrative' : response.text,
            'model' : 'gemini-2.5-flash'
        }
    
    except Exception as e:

        return {
            "narrative": f"LLM generation failed: {str(e)}",
            "model": "gemini-2.5-flash"
        }