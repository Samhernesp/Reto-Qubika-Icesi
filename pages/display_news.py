import streamlit as st
import pandas as pd

def render():
    """Renderiza la página de visualización de noticias."""
    st.title("Noticias en la Base de Datos")
    st.markdown("### Aquí puedes visualizar todas las noticias guardadas en la base de datos.")

    # Cargar el archivo CSV
    try:
        df = pd.read_csv("articles.csv")
        st.write(f"Total de noticias guardadas: {len(df)}")
    except FileNotFoundError:
        st.error("No se encontró el archivo 'articles.csv'. Asegúrate de haber agregado noticias a la base de datos.")
        return

    # Mostrar las noticias en una tabla
    st.table(df)

    # Filtro por título o autor
    st.markdown("#### Filtro por Título o Autor")
    search_query = st.text_input("Buscar:", "")
    if search_query:
        filtered_df = df[
            df["title"].str.contains(search_query, case=False, na=False) |
            df["author"].str.contains(search_query, case=False, na=False)
        ]
        st.write(f"Se encontraron {len(filtered_df)} resultados:")
        st.table(filtered_df)
