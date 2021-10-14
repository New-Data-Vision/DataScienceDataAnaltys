from numpy.core.numeric import True_
import streamlit as st 
import pandas as pd
import numpy as np
from sqlite3.dbapi2 import paramstyle
#import bcrypt
from functions import *
from database import *
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
#from League_functions.avg_Income_for_player_Departures import  BATCH_for_GetAVGExpendFORplayerArrivals
from functions import DataFrameFunc,NumberOfRows
from League_functions.EFPA_func import*
from League_functions.IFPD_func import*
from League_functions.BFPD_func import*
from League_functions.DFLS_func import*
from League_functions.DCWS_func import*
from Club_functions.CDWS_func import*
from Club_functions.CDTAS_func import*
import matplotlib.pyplot as plt
import altair as alt
#rom bokeh.plotting import figure
#mport duckdb
#import subprocess
from html_temp import *
import os
import time

#################
from apps.login_pages import metrics, post
######################
import sqlite3
save_df = DataFrameFunc('datas/Ligaska_KONACAN_STAS.csv')
conn = sqlite3.connect('data_new.db', check_same_thread=False)
c = conn.cursor()

fp_clubs = 'datas/sportska_kubska_statsitika_OBRDENO.csv'
coef = 'file.txt'
fp_league = 'datas/Ligaska_KONACAN_STAS.csv'
save_csv_Expend = 'datas/sportska_kubska_statsitika_OBRDENO.csv'
save_csv_Expend_BATCH = 'datas/BATCH_sportska_kubska_statsitika_OBRDENO.csv'

rem_niz_INCOME = []
rem_niz_BALANCE = []
rem_niz_SEASON = []
rem_niz_CLUB_SEASON = []
rem_niz_CLUB_TROUGHT_SEASON = []
df_empt = pd.DataFrame()
flag = 0
rem_niz_nizz = []



def app():

    

    st.subheader("LogIn")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):

        st.write("Log in as ::: ",username)
        create_usertable()
        temp_user()
        temp_add_user_data(username)
        hashed_pswd = make_password(password)
        result = login_user(username,check_hashes(password,hashed_pswd))

        c.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name="EFPA_table"')

        if c.fetchone()[0]==1 : 
        	st.success('Successfully log  in!!')
        else :
        	st.error('The user does not exist !!')

        if result:
            PAGES = {
                "Metrics": metrics,
                "Post": post
            }
            st.title('Meni')
            selection = st.radio("Go to", list(PAGES.keys()))
            page = PAGES[selection]
            page.app()
