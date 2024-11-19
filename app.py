import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import os
import google.generativeai as genai
from pinecone import Pinecone


GEMINI_API = os.getenv("GEMINI_API")
PINECONE_KEY = os.getenv("PINECONE_KEY")
ELLABS_KEY = os.getenv("ELLABS_KEY")


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
genai.configure(api_key=GEMINI_API)
gem_model = genai.GenerativeModel('gemini-1.5-flash')


#Pinecone Config
pc = Pinecone(api_key=PINECONE_KEY)
if "news" not in pc.list_indexes().names():
    st.error("El índice 'news' no está configurado en Pinecone.")
else:
    index_info = pc.describe_index("news")
    host = index_info['host']
    index = pc.Index("news", host=host)


# Carga de datos iniciales
try:
    df = pd.read_csv("articles.csv")
except FileNotFoundError:
    st.error("El archivo 'articles.csv' no se encuentra.")
    st.stop()


# Función para obtener noticias relacionadas
def get_news(query_text, top_k):
    try:
        query_embedding = model.encode([query_text])[0]
        resultado = index.query(vector=query_embedding.tolist(), top_k=top_k, include_metadata=True)
        resultados_ids = [int(match['id']) for match in resultado['matches']]
        return df.iloc[resultados_ids]
    except Exception as e:
        st.error(f"Error al obtener noticias relacionadas: {e}")
        return pd.DataFrame()

def summarize(news_df):
    try:
        summaries = []
        for _, row in news_df.iterrows():
            prompt = f"Limitate a resumir la siguiente noticia: {row['article_content']}"
            response = gem_model.generate_content(prompt)
            summaries.append(response.text.strip())
        news_df.loc[:, 'article_content'] = summaries
        return news_df
    except Exception as e:
        st.error(f"Error al generar resúmenes: {e}")
        return []

def response(query_text):
    context = get_news(query_text, 2)
    response = summarize(context)
    return response

# Función para generar audio con ElevenLabs
def generate_audio(text):

    url = "https://api.elevenlabs.io/v1/text-to-speech/nPczCjzI2devNBz1zQrb"
    headers = {
        "xi-api-key": ELLABS_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        audio_file = "comparison_audio.mp3"
        with open(audio_file, "wb") as file:
            file.write(response.content)
        return audio_file
    else:
        st.error(f"Error al generar el audio: {response.content}")
        return None

st.title("Comparador de Noticias con Narración")
st.markdown("### Busca, compara y escucha resúmenes de noticias relacionadas.")

query = st.text_input("Escribe tu consulta")

# Botón para procesar consulta
if st.button("Buscar noticias relacionadas"):
    related_news = response(query)

    if related_news.empty or len(related_news) < 2:
        st.warning("No se encontraron suficientes noticias relacionadas para comparar.")
    else:

        st.write("Noticias relacionadas:")
        for index, row in related_news.iterrows():
            st.markdown(f"**{row['title']}** - {row['date']}")
            st.write(row['article_content'])

        comparison_text = f"Comparación entre noticias: {related_news['article_content'].iloc[0]} {related_news['article_content'].iloc[1]}"

        audio_file = generate_audio(comparison_text)
        if audio_file:
            st.audio(audio_file, format="audio/mp3")

# Visualización de similitudes
st.markdown("### Visualización de Similitudes entre Noticias")
embeddings = model.encode(df['article_content'].tolist())
similarity_matrix = np.dot(embeddings, embeddings.T)

plt.figure(figsize=(8, 6))
sns.heatmap(similarity_matrix, annot=False, cmap="coolwarm")
st.pyplot(plt)
