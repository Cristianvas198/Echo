import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="🚀 Chatbot de Productividad", layout="centered", page_icon="💼")

# Estilo con colores y estructura
st.title("💼 Asistente de Productividad con Gemini")
st.write("Optimiza tu trabajo con IA. Escribe una consulta y obtén respuestas estructuradas.")

# Entrada de texto con icono
prompt = st.text_input("✍️ Escribe tu consulta:", placeholder="Ejemplo: Redacta un email profesional...")

# Botón con animación
if st.button("🚀 Generar respuesta"):
    response = requests.get("http://127.0.0.1:8000/chat", params={"prompt": prompt})
    
    # Respuesta con mejor formato
    st.markdown("### 💡 Respuesta:")
    st.markdown(f"📌 **{response.json()['response']}**", unsafe_allow_html=True)
    
    # Línea divisoria
    st.divider()
    
    # Sección adicional para mejorar presentación
    st.write("⚡ _¿Quieres más opciones de automatización? Escribe una tarea y prueba._")


