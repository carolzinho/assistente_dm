import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


user_input = input("INPUT: ")


prompt = f"""
Você é uma atendente virtual de uma clínica médica.
Responda de forma educada, clara e segura.
Não faça diagnósticos médicos.
Em emergências, oriente a procurar atendimento imediato.

Usuário: {user_input}
"""


try:
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    print("\nOUTPUT:")
    print(response.text)
    print("-" * 50)

except Exception as e:
    print("ERRO NO LLM:", e)
