# Usar Python 3.9 como imagen base
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app/src

# Copiar los archivos del proyecto al contenedor
COPY src/ /app/src/
COPY docs /app/docs



# Instalar las dependencias
RUN pip install --no-cache-dir -r /app/src/requirements.txt

# Exponer los puertos para FastAPI (8000) y Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Ejecutar FastAPI y Streamlit al mismo tiempo
CMD uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run /app/src/stream.py --server.port 8501 --server.address 0.0.0.0


