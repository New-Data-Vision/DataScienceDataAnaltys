import streamlit as st
from html_temp import faq

def app():
    #st.markdown("")
    naslov = "Terms and Conditions: FAQ"
    
    a = " The terms and conditions of use are quite simple to use, of course, observing all legal regulations and regulations on data protection and copying, but since this is free and free software, you can share and share the copied content as you wish."

    powerd_by_datavision = "Powerd by Data.Vision"
    st.markdown(faq.format(naslov,a,powerd_by_datavision),unsafe_allow_html=True)