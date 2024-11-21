import streamlit as st
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from pineconeService import PineconeService

GEMINI_API = os.getenv("GEMINI_API")
ELLABS_KEY = os.getenv("ELLABS_KEY")

# Cargar embeddings preexistentes
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

genai.configure(api_key=GEMINI_API)
gem_model = genai.GenerativeModel('gemini-1.5-flash')

pinecone = PineconeService()
pc = pinecone.get_pinecone()

if "news" not in pc.list_indexes().names():
    st.error("El índice 'news' no está configurado en Pinecone.")
else:
    index_info = pc.describe_index("news")
    host = index_info['host']
    index = pc.Index("news", host=host)

try:
    df = pd.read_csv("articles.csv")
except FileNotFoundError:
    st.error("El archivo 'articles.csv' no se encuentra.")
    st.stop()


def get_context(query_text, top_k):
    query_embedding = model.encode([query_text])[0]
    query_embedding = query_embedding.tolist()
    resultado = index.query(vector=query_embedding, top_k=top_k, include_values=True)
    resultados_ids = [match['id'] for match in resultado['matches']]
    similar_news = df.iloc[[int(id) for id in resultados_ids]]
    content = similar_news['article_content']
    context = " ".join(content)
    return context


def generate_reponse(query_text, context):
    try:
        prompt = f"Limitate a responder brevemente la siguiente pregunta:{query_text}\nDe acuerdo a el siguiente contexto:\n{context}"
        response = gem_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"


def response(query_text):
    context = get_context(query_text, 3)
    res = generate_reponse(
        query_text,
        context
    )
    return res


def render():
    st.title("Chat de Preguntas y Respuestas")
    st.markdown("### Haga una pregunta sobre los artículos almacenados.")
    query = st.text_input("Escriba su pregunta:")
    if st.button("Buscar Respuesta"):
        try:
            res = response(query)
            st.markdown(f"{res}")
        except Exception as e:
            st.error(f"Error: {e}")
