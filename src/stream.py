import streamlit as st
import requests

# 🔹 Configuración de página con fondo oscuro y texto claro
st.set_page_config(page_title="🚀 Echo: Futuro Tecnológico", layout="centered", page_icon="🤖")

# 🔹 Aplicar fondo oscuro correctamente
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
    }
    .respuesta {
        border-radius: 10px;
        padding: 15px;
        background-color: #262626;
        color: white;
        font-size: 18px;
    }
    div.stButton > button {
        display: block;
        margin: auto;
        background-color: #00C6FF;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px;
        border: none;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Logo futurista (Asegúrate de tener `logo.png` en tu carpeta)
st.image("logo.png", width=150)

st.markdown("<h1 style='text-align:center; color:#00C6FF;'>🤖 Echo: Chatbot de Tecnologías Futuras</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Explora los avances en IA, robótica, computación cuántica y más.</p>", unsafe_allow_html=True)

# 🔹 Entrada de texto mejorada
prompt = st.text_input("✍️ Escribe tu consulta sobre tecnología:", placeholder="Ejemplo: ¿Cómo será la IA en 2050?")

# 🔹 Botón centrado y mejorado
if st.button("🚀 Obtener información"):
    response = requests.get("http://127.0.0.1:8000/chat", params={"usuario": "Cristian", "prompt": prompt})


    # 🔹 Respuesta estilizada con fondo oscuro y texto visible
    st.markdown("<div class='respuesta'><strong>" + response.json()['response'] + "</strong></div>", unsafe_allow_html=True)

    st.divider()
