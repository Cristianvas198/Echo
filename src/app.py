from fastapi import FastAPI
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configurar el cliente de Gemini
genai.configure(api_key=api_key)

# Inicializar el modelo de Gemini
model = genai.GenerativeModel("gemini-2.0-flash")

# Crear la aplicación FastAPI
app = FastAPI()

@app.get("/")
def landing():
    return {"message": "Bienvenido a la API de chat con Gemini"}

@app.get("/chat")
def chat(prompt: str):
    response = model.generate_content(prompt)
    return {"response": f"**Respuesta:**\n\n{response.text}"}


@app.get("/email")
def generate_email(subject: str, details: str):
    prompt = f"""Genera un email profesional sobre '{subject}', incluyendo estos detalles: {details}. 
    Usa un tono formal y estructurado."""
    
    response = model.generate_content(prompt)
    return {"email": response.text}

@app.get("/resumen")
def generate_summary(text: str):
    prompt = f"""Resume el siguiente texto en 3 párrafos clave: {text}"""
    
    response = model.generate_content(prompt)
    return {"summary": response.text}
