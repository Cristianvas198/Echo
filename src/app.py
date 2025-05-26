import sqlite3  
import os
from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from fastapi.responses import JSONResponse



#--------------------Crear la base de datos y la tabla si no existen--------------------

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
    
    cursor.execute("INSERT INTO conversaciones (usuario, pregunta, respuesta, fecha) VALUES (?, ?, ?, ?)", 
                   (usuario, pregunta, respuesta, datetime.now()))
    
    conn.commit()
    conn.close()

def obtener_respuesta_previa(usuario, pregunta):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT respuesta FROM conversaciones WHERE usuario = ? AND pregunta = ? ORDER BY fecha DESC LIMIT 1", 
                   (usuario, pregunta))
    respuesta = cursor.fetchone()
    conn.close()
    
    return respuesta[0] if respuesta else None


#-------------------------------------Configuración de Google Gemini--------------------------

# Variables de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Cliente de Gemini
genai.configure(api_key=api_key)

# Inicializar el modelo de Gemini
model = genai.GenerativeModel("gemini-2.0-flash")


#-------------------------------------Configuración de FastAPI---------------------------------

app = FastAPI()

@app.get("/") # Ruta de bienvenida
def landing():
    return {"message": "Bienvenido a la API de chat con Gemini"}

@app.get("/chat") # Ruta para el chat
def chat(usuario: str, prompt: str):
    try:
        # Buscar las respuestas previas en la base de datos
        respuesta_previa = obtener_respuesta_previa(usuario, prompt) 


        if respuesta_previa:
            return JSONResponse(content={"response": respuesta_previa})  # ✅ Si hay una respuesta guardada, la usamos

        # Optimizar el prompt para el modelo
        contexto = f"""Eres Echo, un asistente experto en tecnologías futuras. Responde de forma clara y concisa.
        Cada respuesta debe estar relacionada con tecnología, innovación y avances digitales, sin excepciones.
        Limita tu respuesta a un máximo de **3 párrafos cortos** y evita información innecesaria.
        Consulta: '{prompt}'"""
        
        response = model.generate_content(contexto)

        if not response or not response.text:
            raise ValueError("⚠️ No se obtuvo respuesta del modelo")

        respuesta_final = response.text.strip()
        guardar_conversacion(usuario, prompt, respuesta_final)

        return JSONResponse(content={"response": respuesta_final})

    except Exception as e:
        return JSONResponse(content={"response": f"⚠️ Error en la API: {str(e)}"})

@app.get("/historial") # Ruta para obtener el historial de conversaciones
def obtener_historial(usuario: str):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pregunta, respuesta, fecha FROM conversaciones WHERE usuario = ? ORDER BY fecha DESC", (usuario,))
    historial = cursor.fetchall()
    conn.close()

    return JSONResponse(content={"historial": [{"pregunta": h[0], "respuesta": h[1], "fecha": h[2]} for h in historial]})
