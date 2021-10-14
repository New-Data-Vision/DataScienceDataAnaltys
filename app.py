
import streamlit as st


from multiapp import MultiApp
from apps import home, SingUp, LogIn, LogIn, Search , About , TandC_FAQ# import your app modules here


app = MultiApp()


st.markdown("""
# Multi-Page App Football Data app
""")


# Add all your application here
app.add_app("Home", home.app)
app.add_app("SingUp", SingUp.app)
#app.add_app("Model", model.app)
app.add_app("LogIn",LogIn.app)
app.add_app("Search",Search.app)
app.add_app("About",About.app)
app.add_app("Terms and Conditions: FAQ",TandC_FAQ.app)
# The main app
app.run()