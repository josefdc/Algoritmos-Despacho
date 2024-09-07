from openai import OpenAI
import os
from dotenv import load_dotenv

# Carga variables de entorno desde el archivo .env
load_dotenv()

# Obtén la API key desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Falta la API key de OpenAI. Asegúrate de que está definida en el archivo .env.")

# Crear una instancia del cliente OpenAI
client = OpenAI(api_key=api_key)

def ask_openai(context, question):
    """Function to handle interaction with OpenAI GPT using the gpt-4 model."""
    # Mensaje del sistema que indica una respuesta concisa y precisa
    messages = [
        {"role": "system", "content": "Eres un asistente experto que ayuda con preguntas sobre el contexto de la aplicación. Responde de manera concisa y solo proporciona la información más relevante."},
        {"role": "user", "content": f"Contexto de la aplicación:\n{context}\n\nPregunta del usuario:\n{question}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",  # Modelo a usar
            messages=messages,
            max_tokens=200,  # Limita la respuesta a un máximo de 100 tokens
            temperature=0.4,  # Mantén la temperatura baja para respuestas más deterministas y concisas
            top_p=0.3,  # Reduce ligeramente top-p para limitar la diversidad de las respuestas
            frequency_penalty=0.2,  # Penaliza repeticiones de información
            presence_penalty=0.0  # No penalices la introducción de nueva información
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f'Error al contactar con OpenAI: {str(e)}'
