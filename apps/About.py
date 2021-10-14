import streamlit as st
from html_temp import about_mesage

def app():
    st.markdown("About")
    a = " Who we are?"
    answer =" We are a free, independent platform interested a little deeper below the surface on financial transfers the way fluctuations and transfers are managed by either clubs or leagues, a network of players fluctuating between leagues and clubs.  Platform Football Data Revolution . We are sponsored by Data.Vision which has given us the rights to the resources for the benefits of this tool of course for free !! for any questions please contact us by email : footballdatarevolution@gmail.com"
    powerd_by_datavision = "Powerd by Data.Vision"
    st.markdown(about_mesage.format(a,answer,powerd_by_datavision),unsafe_allow_html=True)