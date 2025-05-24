import sqlite3  
import os
from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv

# 🔹 1. Crear la base de datos y la tabla si no existen
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    pregunta TEXT,
    respuesta TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()

def guardar_conversacion(usuario, pregunta, respuesta):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO conversaciones (usuario, pregunta, respuesta) VALUES (?, ?, ?)", 
                   (usuario, pregunta, respuesta))
    
    conn.commit()
    conn.close()

def obtener_respuesta_previa(pregunta):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT respuesta FROM conversaciones WHERE pregunta = ? ORDER BY fecha DESC LIMIT 1", (pregunta,))
    respuesta = cursor.fetchone()
    conn.close()
    
    return respuesta[0] if respuesta else None


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
def chat(usuario: str, prompt: str):
    # Buscar respuesta previa en la base de datos
    respuesta_previa = obtener_respuesta_previa(prompt)

    if respuesta_previa:
        return {"response": respuesta_previa}  # Si hay una respuesta guardada, la usamos

    # 🔹 Optimización del Prompt
    contexto = f"""Eres Echo, un asistente experto en tecnologías futuras. Responde de forma clara y concisa.
    Limita tu respuesta a un máximo de **3 párrafos cortos** y evita información innecesaria.
    Consulta: '{prompt}'"""
    
    response = model.generate_content(contexto)

    # Guardamos la nueva respuesta en la base de datos
    guardar_conversacion(usuario, prompt, response.text)

    return {"response": response.text}





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
