from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "models/gemini-2.5-flash"


def safe_json_extract(text: str) -> dict | None:
    """
    Extrai o primeiro JSON válido encontrado no texto.
    """
    if not text:
        return None

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def classify_intent(text: str) -> dict:
    prompt = f"""
Você é um classificador de intenção.

RESPONDA SOMENTE COM JSON VÁLIDO.
NÃO escreva texto fora do JSON.
NÃO use markdown.

Formato EXATO:
{{"intent":"<intencao>","urgency":"<normal|alta>"}}

Intenções permitidas:
- saudacao
- marcar_consulta
- perguntar_preco
- perguntar_convenio
- emergencia
- corrigir_dado
- outro

Mensagem do usuário:
"{text}"
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        parsed = safe_json_extract(response.text)

        if not parsed:
            raise ValueError("Resposta não contém JSON válido")

        # Validação defensiva
        if "intent" not in parsed or "urgency" not in parsed:
            raise ValueError("JSON incompleto")

        return parsed

    except Exception as e:
        print("ERRO AO CLASSIFICAR INTENÇÃO:", e)
        return {
            "intent": "outro",
            "urgency": "normal"
        }


if __name__ == "__main__":
    while True:
        user_input = input("INPUT: ")
        print("INTENT:", classify_intent(user_input))
