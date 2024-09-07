from openai import OpenAI
import os

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(context, question):
    """Function to handle interaction with OpenAI GPT using the gpt-4o-mini model."""
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
