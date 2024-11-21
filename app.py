import streamlit as st
from streamlit_option_menu import option_menu
from pages import scraping
from pages import summary
from pages import chat
from pages import display_news

st.set_page_config(page_title="Noticias y Comparaciones", layout="wide", initial_sidebar_state="collapsed")


selected = option_menu(
    menu_title="Menú Principal",
    options=["Scraping", "Comparador", "Chat", "Mostrar Noticias"],
    icons=["search", "bar-chart", "chat", "list-task"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Scraping":
    scraping.render()
elif selected == "Comparador":
    summary.render()
elif selected == "Chat":
    chat.render()
elif selected == "Mostrar Noticias":
    display_news.render()
