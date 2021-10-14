import streamlit as st
from apps.login_pages.league_apps import EFPA,EFPA_BATCH,IFPD,IFPD_BATCH,BFPD,BFPD_BATCH,DFLS,DFLS_BATCH,DCWS,DCWS_BATCH
def app():
    st.title('Metrics for  LEAGUES')
    st.write('Welcome to app1')
    PAGES = {
        " 1. Processed Data by average league EXPEND for player ARRIVALS": EFPA,
        " 2. Custom options for previous function ": EFPA_BATCH,
        " 3. Processed Data by average league INCOME for player DEPARTURES":IFPD,
        " 4. Custom options for previous function":IFPD_BATCH,
        " 5. Processed Data by average league BALANCE for player DEPARTURES":BFPD, 
        " 6. Custom options for previous function":BFPD_BATCH,
        " 7. Processed Data by average LEAGUE by AVG SESONS statistic":DFLS,
        " 8. Custom options for previous function":DFLS_BATCH,
        " 9. Processed Data by average -> LEAGUE by YEAR statistic":DCWS,
        " 10. Custom options for previous function":DCWS_BATCH    
        }
    st.title('Meni')
    selection = st.selectbox("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

    # Custom options for previous function
    # Data by average league EXPEND for player ARRIVALS

    # Data by average league INCOME for player DEPARTURES

    # BATCH Data by average league BALANCE for player DEPARTURES

    # BATCH Data by average LEAGUE by AVG SESONS statistic

    # BATCH Data by average -> LEAGUE by YEAR statistic