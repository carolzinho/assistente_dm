import os
from dotenv import load_dotenv
from google import genai
from prompts import SYSTEM_PROMPT_CLINICA

load_dotenv()


def get_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY não encontrada no .env")

    return genai.Client(api_key=api_key)


def call_llm(user_prompt: str) -> str:
    try:
        client = get_client()

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                {"role": "user", "parts": [SYSTEM_PROMPT_CLINICA]},
                {"role": "user", "parts": [user_prompt]},
            ],
        )

        return response.text.strip()

    except Exception as e:
        print("ERRO NO LLM:", e)
        return "Erro ao gerar resposta"
