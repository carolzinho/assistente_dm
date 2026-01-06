from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "models/gemini-2.5-flash"


def extract_entities(user_input: str) -> dict:
    prompt = f"""
Você é um sistema de extração de informações.

⚠️ Responda SOMENTE com um JSON válido.
⚠️ Não escreva explicações, comentários ou texto fora do JSON.

Formato obrigatório:
{{
  "especialidade": string ou null,
  "medico": string ou null,
  "data": string ou null,
  "horario": string ou null
}}

Mensagem do usuário:
"{user_input}"
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw_text = response.text.strip()

        # 🔎 Extrai o primeiro bloco JSON da resposta
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)

        if not match:
            raise ValueError("Nenhum JSON encontrado na resposta")

        json_text = match.group()
        return json.loads(json_text)

    except Exception as e:
        print("ERRO NA EXTRAÇÃO DE ENTIDADES:", e)
        return {
            "especialidade": None,
            "medico": None,
            "data": None,
            "horario": None
        }



if __name__ == "__main__":
    while True:
        msg = input("INPUT: ")
        if msg.lower() in ["sair", "exit"]:
            break

        entities = extract_entities(msg)
        print("ENTITIES:", entities)
        print("-" * 40)
