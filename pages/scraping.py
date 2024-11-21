import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from pineconeService import PineconeService

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

pinecone = PineconeService()

pc = pinecone.get_pinecone()
if "news" not in pc.list_indexes().names():
    st.error("El índice 'news' no está configurado en Pinecone.")
else:
    index_info = pc.describe_index("news")
    host = index_info['host']
    index = pc.Index("news", host=host)

def scrape_semanayelespectador(url):
    try:
        if "semana.com" in url:
            response = requests.get(url)

            if response.status_code == 200:
                content = response.text
                soup = BeautifulSoup(content, 'lxml')
                header_box = soup.find('div', class_="mx-auto max-w-[968px]")
                title = header_box.find('h1').get_text()
                author = header_box.find('span', class_="mb-1 border-l border-primary pl-2 text-sm font-medium").get_text()
                date = header_box.find('div', class_="pl-2 text-xs leading-none").get_text()
                body = soup.find('div', class_="paywall mx-auto mb-4")
                content = body.find_all('p')
                article_content = ""
                for p in content:
                    article_content += p.get_text() + " "
            else:
                    raise Exception("Error al acceder al sitio web de Semana.")

        elif "elespectador.com" in url:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                soup = BeautifulSoup(content, 'lxml')
                header_box = soup.find('div', class_='ArticleHeader')
                title = header_box.find('h1', class_='Title').get_text()
                author = header_box.find('div', class_='ArticleHeader-Author').get_text()
                header_info = soup.find('div', class_='ArticleHeader-ContainerInfo')
                datetime = header_info.find('div', class_='Datetime ArticleHeader-Date').get_text()
                date = datetime.split('-')[0].strip()
                content_box = soup.find('div', class_='Article-Content')
                content = content_box.find_all('p', class_='font--secondary')
                article_content = ""
                for p in content:
                    article_content += p.get_text() + " "
            else:
                raise Exception("Error al acceder al sitio web de El Espectador.")
        else:
            st.error("URL no válido. Solo se soportan 'Semana' y 'El Espectador'.")
            return None


        return {'title' : title, 'author' : author, 'date' : date, 'article_content' : article_content}
    except Exception as e:
        st.error(f"Error al realizar scraping: {e}")
        return None

def render():
    st.title("Scraping de Noticias")
    st.markdown("### Ingrese una URL de Semana o El Espectador para agregar un artículo.")

    url = st.text_input("Ingrese la URL del artículo")

    if st.button("Extraer Artículo"):
        if url:
            article = scrape_semanayelespectador(url)
            if article:
                st.write("Artículo extraído exitosamente:")
                new_row = pd.DataFrame([article])
                st.table(new_row)

                try:
                    df = pd.read_csv("articles.csv")
                except FileNotFoundError:
                    df = pd.DataFrame(columns=["title", "author", "date", "article_content"])

                df = pd.concat([df, new_row])
                df.reset_index(drop=True, inplace=True)

                df.to_csv("articles.csv", index=False)

                print(len(df.index))

                try:
                    embedding = model.encode(article['article_content'])
                    index.upsert([(str(len(df.index)-1), embedding)])
                except Exception as e:
                    st.error(f"No fue posible guardar el artículo en Pinecone: {e}")

                st.success("Artículo añadido a la base de datos.")
        else:
            st.warning("Por favor, ingrese una URL válida.")
