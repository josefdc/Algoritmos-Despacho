from openai import OpenAI
import os
from dotenv import load_dotenv

# Carga variables de entorno desde el archivo .env
load_dotenv()

# Obtén la API key desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

print(f"API Key: {api_key}")

if not api_key:
    raise ValueError("Falta la API key de OpenAI. Asegúrate de que está definida en el archivo .env.")

# Crear una instancia del cliente OpenAI
client = OpenAI(api_key=api_key)

def ask_openai(context, question):
    """Function to handle interaction with OpenAI GPT using the gpt-4 model."""
    messages = [
        {"role": "system", "content": "Eres un asistente que ayuda con preguntas sobre el contexto de la aplicación."},
        {"role": "user", "content": f"Contexto de la aplicación:\n{context}\n\nPregunta del usuario:\n{question}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f'Error al contactar con OpenAI: {str(e)}'
