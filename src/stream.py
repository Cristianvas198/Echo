import streamlit as st
import requests

# 🔹 Configuración de página con título, ícono y diseño ancho
st.set_page_config(
    page_title="🚀 Echo: Futuro Tecnológico",
    layout="wide",
    page_icon="🤖"
)

# 🔹 Aplicar fondo oscuro y mejorar estilos
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
        font-size: 20px;
        text-align: left;
        margin-top: 20px;
    }
    .contenedor {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    div.stButton > button {
        display: block;
        margin: auto;
        background-color: #00C6FF;
        color: white;
        border-radius: 10px;
        font-size: 20px;
        padding: 12px;
        border: none;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Centrar el logo y mejorar tamaño con ruta absoluta dentro del contenedor

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.image("/app/docs/img/logo.png", width=400)  # ✅ Agrandamos la imagen
st.markdown("</div>", unsafe_allow_html=True)


# 🔹 Título y descripción mejorados
st.markdown("<h1 style='text-align:center; color:#00C6FF;'>🤖 Echo: Chatbot de Tecnologías Futuras</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Explora los avances en IA, robótica, computación cuántica y más.</p>", unsafe_allow_html=True)

# 🔹 Entrada de texto mejorada con placeholder descriptivo
prompt = st.text_input("✍️ Escribe tu consulta sobre tecnología:", placeholder="Ejemplo: ¿Cómo será la IA en 2050?")

# 🔹 Botón de consulta con animación de carga
if st.button("🚀 Obtener información"):
    with st.spinner("🔄 Generando respuesta..."):
        response = requests.get("http://127.0.0.1:8000/chat", params={"usuario": "Cristian", "prompt": prompt})
    
    # 🔹 Mostrar la respuesta con fondo oscuro y tamaño optimizado
    st.markdown(f"<div class='respuesta'><strong>{response.json()['response']}</strong></div>", unsafe_allow_html=True)
    st.divider()

# 🔹 Botón para mostrar historial de conversaciones
if st.button("📜 Ver historial"):
    historial_response = requests.get("http://127.0.0.1:8000/historial", params={"usuario": "Cristian"})
    historial = historial_response.json()["historial"]

    st.markdown("<h3 style='color:#00C6FF;'>📜 Historial de conversaciones</h3>", unsafe_allow_html=True)
    for item in historial:
        st.markdown(f"<div class='respuesta'><strong>{item['fecha']}</strong><br><strong>Q:</strong> {item['pregunta']}<br><strong>A:</strong> {item['respuesta']}</div>", unsafe_allow_html=True)
