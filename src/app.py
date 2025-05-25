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
    Cada respuesta debe estar relacionada con tecnología, innovación y avances digitales, sin excepciones.
    Limita tu respuesta a un máximo de **3 párrafos cortos** y evita información innecesaria.
    Consulta: '{prompt}'"""
    
    response = model.generate_content(contexto)

    # Guardamos la nueva respuesta en la base de datos
    guardar_conversacion(usuario, prompt, response.text)

    return {"response": response.text}

@app.get("/historial")
def obtener_historial(usuario: str):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pregunta, respuesta, fecha FROM conversaciones WHERE usuario = ? ORDER BY fecha DESC", (usuario,))
    historial = cursor.fetchall()
    conn.close()
    
    return {"historial": historial}

