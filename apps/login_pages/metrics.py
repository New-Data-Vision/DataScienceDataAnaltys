import streamlit as st
from apps.login_pages import clubs,leauges
def app():
    options = "Chose option"
    st.title('Metrics for  LEAGUES')
    st.write('Welcome to LEauges options')
    PAGES = {
        "Processed Data by LEAUGES": leauges,
        "Processed Data by CLUBS": clubs

        }
    st.title('Meni')
    selection = st.selectbox("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()