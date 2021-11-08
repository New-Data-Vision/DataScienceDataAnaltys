from numpy.core.numeric import NaN
from numpy.core.numerictypes import _typedict
import streamlit as st 
import marshal
import time
import pandas as pd
import numpy as np
from sqlite3.dbapi2 import paramstyle
from functions import check_email,make_password,check_hashes,GETCoefficients,remove_duplicates
from database import create_usertable,add_user_data,check_double_email,check_double_username,login_user,check_userdatatable
import matplotlib
matplotlib.use('Agg')
#from League_functions.avg_Income_for_player_Departures import  BATCH_for_GetAVGExpendFORplayerArrivals
from functions import DataFrameFunc,NumberOfRows
from League_functions.EFPA_func import*
from Club_functions.CDWS_func import*
from Club_functions.CDTAS_func import*
import matplotlib.pyplot as plt
from database import*
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import altair as alt
from datetime import datetime
from html_temp import *
import PIL.Image as Image
from pathlib import Path
from PIL import UnidentifiedImageError
from streamlit import caching
from html_temp import*
from functions import*
import pandas as pd
import base64
from PIL import Image
import textwrap
from io import StringIO,BytesIO
from PIL import Image
from database import*
import os
import streamlit.components.v1 as components
import sqlite3
import os
rem_niz_CLUB_SEASON = []
rem_niz_CLUB_TROUGHT_SEASON = []
coef = 'file.txt'
fp_league = 'Ligaska_KONACAN_STAS.csv'
fp_clubs = 'datas/sportska_kubska_statsitika_OBRDENO.csv'
save_csv_Expend = "sportska_kubska_statsitika_OBRDENO.csv"
save_csv_Expend_BATCH = 'datas/BATCH_sportska_kubska_statsitika_OBRDENO.csv'
#-----------------------------------------
f_datas = 'datas/exported/GetAVGExpendFORplayerArrivals.csv'
#------------------------------------






def app():





    #st.title('View all posts !!!')
    a = " Welcome to the Football data revolution !!"
    b = " Here you are chance to investigate and explore football financial data about leagues and clubs across Europe and the World"
    c = " Data are collected by Transfmarket.com and data records by the Expenditures of top 100 clubs every season and top 25/26 Leagues by Expenditures"
    d = " With expending by club or league are recorded how many players come or leave club and league, also recorded Profit and revenue or income"
    e = " We take the coefficient of inflation and calculate for every cash transfer and thus have the opportunity to see the role we call the ‘inflation rate’ and see the monetary amount and the real value of a monetary transaction that took place 15 or more years ago."
    p = " We hope you enjoy and indulge your research imagination, also here you can explore, prove and argue your theses. We’ve provided you with interactive graos, data processing tools that handle a bunch and a bunch of different data, and allowed you to create your own post and share your thoughts with us. To use our software you need to register and log in, and the fun begins"
    
    powerd_by_datavision = "Powerd by Data.Vision"
    st.markdown(home_message.format(a,b,c,d,e,p,powerd_by_datavision),unsafe_allow_html=True)

    if st.checkbox(" Read some post !! "):
        blog_option = st.selectbox("Chose a option ",["Search post by Author","Search post by Title"], key='post_options' )
    
        df_user = pd.read_sql_query('SELECT DISTINCT user_id FROM blog_table_temp_MAIN',conn)
        temp_user = df_user['user_id'].unique() 
        df_post = pd.read_sql_query('SELECT DISTINCT id_post FROM blog_table_temp_MAIN',conn)
        temp_post = df_post['id_post'].unique() 
        # st.success("temp_post")
        # st.dataframe(temp_post)
        post_lista =[]
        for i in temp_post:
            post_lista.append(i)
        user_lista =[]
        for i in temp_user:
            user_lista.append(i)
        d = {}
        for i in user_lista:
            #st.write(" i :: ",i)
            for j in post_lista:
                #st.write(" j :: ",j)
                df = pd.read_sql_query('SELECT author,read_time FROM blog_table_temp_MAIN WHERE id_post = "{}"'.format(int(j)),conn)
                #st.dataframe(df)
                Total = df['read_time'].sum()
                add_if_key_not_exist(d,j,Total)
        if blog_option == "Search post by Title":
            st.success("Search posts by the Title name")
            df_title = pd.read_sql_query('SELECT title FROM blog_table_temp_MAIN',conn)
            temp_title = df_title['title'].unique() 
            title_lista =[]
            for i in temp_title:
                title_lista.append(i)
            remeber = st.selectbox("Select title post", options= list(title_lista))
            if st.button("Submit"):
                df_title_temp = pd.read_sql_query('SELECT id_post,user_id FROM blog_table_temp_MAIN WHERE title = "{}"'.format(remeber),conn)
                #st.dataframe(df_title_temp)
                j = df_title_temp['user_id'][0]
                i = df_title_temp['id_post'][0]
                df_title = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
                df_a_d_t = pd.read_sql_query('SELECT DISTINCT title,author,postdate FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
                if df_a_d_t.empty != True :
                    temp_reading_time = d.get(i)
                    st.markdown(head_message_temp.format(df_a_d_t['title'][0],df_a_d_t['author'][0],df_a_d_t['postdate'][0],temp_reading_time),unsafe_allow_html=True)
                    for i in range(0,len(df_title)):
                        if df_title['img'][i] != None:
                            data = df_title['img'][i]
                            h = int(df_title['h'][i])
                            w = int(df_title['w'][i])
                            nova_lista = marshal.loads(data)  
                            arr = np.array(nova_lista)                            
                            oimg = convert_bytes_to_img(w,h,arr)
                            st.image(oimg)
                        elif type(df_title['article'][i]) == str and df_title['article'][i] != None:
                            st.markdown(full_message_temp.format(df_title['article'][i]),unsafe_allow_html=True)
        elif blog_option == "Search post by Author":
            st.success("Search posts by the Author name")
            df_autor = pd.read_sql_query('SELECT author FROM blog_table_temp_MAIN',conn)
            temp_autor = df_autor['author'].unique() 
            title_autor =[]
            for i in temp_autor:
                title_autor.append(i)
            autor_temp = st.selectbox("Select title post", options= list(title_autor))
            if st.button("Submit author"):
                df_title_temp = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE author = "{}"'.format(autor_temp),conn)
                temp_user = df_title_temp['user_id'].unique() 
                user_lista =[]
                for i in temp_user:
                    user_lista.append(i)
                df = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN',conn)
                df_new = df[['id_post','author','user_id','title','article','img','postdate']]
                a = df_new['id_post'].unique() 
                lista =[]
                for i in a:
                    lista.append(i)
                for j in user_lista:
                    df = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE user_id = "{}"'.format(int(j)),conn)
                    for i in lista:
                        df_print = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
                        df_a_d_t = pd.read_sql_query('SELECT DISTINCT title,author,postdate FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
                        if df_a_d_t.empty != True :
                            temp_reading_time = d.get(i)
                            st.markdown(head_message_temp.format(df_a_d_t['title'][0],df_a_d_t['author'][0],df_a_d_t['postdate'][0],temp_reading_time),unsafe_allow_html=True)
                            for i in range(0,len(df_print)):
                                if  df_print['img'][i] != None:
                                    data = df_print['img'][i]
                                    h = int(df_print['h'][i])
                                    w = int(df_print['w'][i])
                                    nova_lista = marshal.loads(data)  
                                    arr = np.array(nova_lista)                            
                                    oimg = convert_bytes_to_img(w,h,arr)
                                    st.image(oimg)
                                elif type(df_print['article'][i]) == str and df_print['article'][i] != None:
                                    st.markdown(full_message_temp.format(df_print['article'][i]),unsafe_allow_html=True)
                            st.success("end of post")

    if st.checkbox(" Take look and see some awesome interactive dashboard !! "):

        
        if st.checkbox(" League Expenditures  "):
            st.success("Potrošnja liga") 
            te = int(2)
            flag = return_id_EFPA_table(te)
            if flag != []:
                if int(te) > 0:
                    ##      1. Graph 
                    df = pd.read_sql_query('SELECT * FROM EFPA_table WHERE user_id = "{}"'.format(te),conn)
                    df_new = df[["Name_of_Legue","Year","Nationality","Expend_by_player","Expend_INFLACION"]]
                    df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                    st.markdown(html_vizaulazacija1,unsafe_allow_html=True)
                    chartline1 = alt.Chart(df_new).mark_line(size=5,color='#297F87').encode(
                         x=alt.X('Year', axis=alt.Axis(title='date')),
                         y=alt.Y('sum(Expend_by_player)',axis=alt.Axis( title='Inflation rate'), stack=None),
                         ).properties(
                             width=700, 
                             height=500
                         ).interactive()
                    
                    chartline2 = alt.Chart(df_new).mark_line(size=5,color='#DF2E2E').encode(
                         x=alt.X('Year', axis=alt.Axis(title='date')),
                         y=alt.Y('sum(Expend_INFLACION)', axis=alt.Axis( title='Inflation rate'),stack=None)
                         ).properties(
                             width=700, 
                             height=500
                         ).interactive()
                    st.altair_chart(chartline1 + chartline2)
                    ##########################################################################################################
                    ##      2. Graph 
                    st.markdown(html_vizaulazacija2,unsafe_allow_html=True)
                    st.subheader("Expend by year ")
                    
                    df2 = pd.read_sql_query('SELECT * FROM EFPA_table WHERE user_id = "{}"'.format(te),conn)
                    df_new2 = df2[["Name_of_Legue","Year","Nationality","Expend_by_player","Expend_INFLACION"]]
                    #df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                    df_new2["date2"] = pd.to_datetime(df["Year"],format='%Y')
                    data_start = df_new2["Year"].min()
                    data_end = df_new2["Year"].max()
                    def timestamp(t):
                      return pd.to_datetime(t).timestamp() * 1000
                    slider2 = alt.binding_range(name='cutoff:', min=timestamp(data_start), max=timestamp(data_end))
                    selector2 = alt.selection_single(name="SelectorName",fields=['cutoff'],bind=slider2,init={"cutoff": timestamp("2011-01-01")})
                    abssa = alt.Chart(df_new2).mark_bar(size=17).encode(
                        x='Year',
                        y=alt.Y('Expend_by_player',title =None),
                        color=alt.condition(
                            'toDate(datum.Year) < SelectorName.cutoff[0]',
                          alt.value('red'), alt.value('blue')
                        )
                    ).properties(
                        width=700,
                    ).add_selection(
                        selector2
                    )
                    st.altair_chart(abssa)
                    st.subheader("Expend by year + INFLACION")
                    df2 = pd.read_sql_query('SELECT * FROM EFPA_table WHERE user_id = "{}"'.format(te),conn)
                    df_new2 = df2[["Name_of_Legue","Year","Nationality","Expend_by_player","Expend_INFLACION"]]
                    df_new2["date2"] = pd.to_datetime(df["Year"],format='%Y')
                    data_start = df_new2["Year"].min()
                    data_end = df_new2["Year"].max()
                    #st.write("data_start",data_start,"data_end",data_end)
                    def timestamp(t):
                      return pd.to_datetime(t).timestamp() * 1000
                    slider2 = alt.binding_range(name='cutoff:', min=timestamp(data_start), max=timestamp(data_end))
                    selector2 = alt.selection_single(name="SelectorName",fields=['cutoff'],bind=slider2,init={"cutoff": timestamp("2011-01-01")})
                    abssa = alt.Chart(df_new2).mark_bar(size=17).encode(
                        x='Year',
                        y=alt.Y('Expend_INFLACION',title =None),
                        color=alt.condition(
                            'toDate(datum.Year) < SelectorName.cutoff[0]',
                          alt.value('red'), alt.value('blue')
                        )
                    ).properties(
                        width=700,
                    ).add_selection(
                        selector2
                    )
                    st.write(abssa)
                    ##########################################################################################################
                    ##      3. Graph 
                    st.markdown(html_vizaulazacija3,unsafe_allow_html=True)
                    while True:
                        lines = alt.Chart(df_new).mark_bar(size=25).encode(
                          x=alt.X('Year',axis=alt.Axis(title='date')),
                          y=alt.Y('Expend_by_player',axis=alt.Axis(title='value'))
                          ).properties(
                              width=600,
                              height=300
                          )
                        def plot_animation(df_new):
                            lines = alt.Chart(df_new).mark_bar(size=25).encode(
                            x=alt.X('Year', axis=alt.Axis(title='date')),
                            y=alt.Y('Expend_by_player',axis=alt.Axis(title='value')),
                            ).properties(
                                width=600, 
                                height=300
                            )
                            return lines
                        N = df_new.shape[0] # number of elements in the dataframe
                        burst = 6       # number of elements (months) to add to the plot
                        size = burst    # size of the current dataset
                        line_plot = st.altair_chart(lines)
                        line_plot
                        start_btn1 = st.button('Start')
                        if start_btn1:
                            for i in range(1,N):
                                step_df = df_new.iloc[0:size]       
                                lines = plot_animation(step_df)
                                line_plot = line_plot.altair_chart(lines)
                                size = i + burst
                                if size >= N:
                                    size = N - 1  
                                time.sleep(0.1)
                        break
                    ##########################################################################################################
                    ##      4. Graph 
                    st.markdown(html_vizaulazacija4,unsafe_allow_html=True)
                    while True:
                        lines = alt.Chart(df_new).mark_bar(size=25).encode(
                          x=alt.X('Year',axis=alt.Axis(title='date')),
                          y=alt.Y('Expend_INFLACION',axis=alt.Axis(title='value'))
                          ).properties(
                              width=600,
                              height=300
                          )
                        def plot_animation(df_new):
                            lines = alt.Chart(df_new).mark_bar(size=25).encode(
                            x=alt.X('Year', axis=alt.Axis(title='date')),
                            y=alt.Y('Expend_INFLACION',axis=alt.Axis(title='value')),
                            ).properties(
                                width=600, 
                                height=300
                            )
                            return lines
                        N = df_new.shape[0] # number of elements in the dataframe
                        burst = 6       # number of elements (months) to add to the plot
                        size = burst    # size of the current dataset
                        line_plot = st.altair_chart(lines)
                        line_plot
                        start_btn2 = st.button('Start',key='2021')
                        if start_btn2:
                            for i in range(1,N):
                                step_df = df_new.iloc[0:size]       
                                lines = plot_animation(step_df)
                                line_plot = line_plot.altair_chart(lines)
                                size = i + burst
                                if size >= N:
                                    size = N - 1  
                                time.sleep(0.1)
                        break                   
                    st.success("Viusalise  Datas")

        if st.checkbox(" Leagues Incomes  "):
            st.warning("Prihodi liga ")
            te = int(2)
            flag = return_id_IFPD_table(te)
            if flag != []:
                if int(te) > 0:
                    ##      1. Graph 
                    df = pd.read_sql_query('SELECT * FROM IFPD_table WHERE user_id = "{}"'.format(te),conn)
                    df.columns.name = None
                    #st.dataframe(df)
                    df_new = df[["Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"]]
                    #df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                    df_new["Year"] = pd.to_datetime(df_new["Year"]).dt.strftime("%Y")
                    st.markdown(html_IFPD_vizaulazacija1,unsafe_allow_html=True)
                    chartline1 = alt.Chart(df_new).mark_line(size=5,color='#297F87').encode(
                         x=alt.X('Year', axis=alt.Axis(title='date')),
                         y=alt.Y('sum(Income_by_player)',axis=alt.Axis( title='Inflation rate'), stack=None),
                         ).properties(
                             width=700, 
                             height=500
                         ).interactive()
                    
                    chartline2 = alt.Chart(df_new).mark_line(size=5,color='#DF2E2E').encode(
                         x=alt.X('Year', axis=alt.Axis(title='date')),
                         y=alt.Y('sum(Income_INFLACION)', axis=alt.Axis( title='Inflation rate'),stack=None)
                         ).properties(
                             width=700, 
                             height=500
                         ).interactive()
                    st.altair_chart(chartline1 + chartline2)
                    ##########################################################################################################
                    ##      2. Graph 
                    st.markdown(html_IFPD_vizaulazacija2,unsafe_allow_html=True)
                    st.subheader("Income by year ")
                    
                    df2 = pd.read_sql_query('SELECT * FROM IFPD_table WHERE user_id = "{}"'.format(te),conn)
                    df_new2 = df2[["Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"]]
                    df_new2["date2"] = pd.to_datetime(df["Year"]).dt.strftime("%Y-%m-%d")
                    data_start = df_new2["Year"].min()
                    data_end = df_new2["Year"].max()
                    def timestamp(t):
                      return pd.to_datetime(t).timestamp() * 1000
                    slider2 = alt.binding_range(name='cutoff:', min=timestamp(data_start), max=timestamp(data_end))
                    selector2 = alt.selection_single(name="SelectorName",fields=['cutoff'],bind=slider2,init={"cutoff": timestamp("2011-01-01")})
                    abssa = alt.Chart(df_new2).mark_bar(size=17).encode(
                        x='Year',
                        y=alt.Y('Income_by_player',title =None),
                        color=alt.condition(
                            'toDate(datum.Year) < SelectorName.cutoff[0]',
                          alt.value('red'), alt.value('blue')
                        )
                    ).properties(
                        width=700,
                    ).add_selection(
                        selector2
                    )
                    st.altair_chart(abssa)
                    st.subheader("Income by year + INFLACION")
                    df2 = pd.read_sql_query('SELECT * FROM IFPD_table WHERE user_id = "{}"'.format(te),conn)
                    df_new2 = df2[["Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"]]
                    df_new2["date2"] = pd.to_datetime(df2["Year"]).dt.strftime("%Y-%m-%d")
                    data_start = df_new2["Year"].min()
                    data_end = df_new2["Year"].max()
                    #st.write("data_start",data_start,"data_end",data_end)
                    def timestamp(t):
                      return pd.to_datetime(t).timestamp() * 1000
                    slider2 = alt.binding_range(name='cutoff:', min=timestamp(data_start), max=timestamp(data_end))
                    selector2 = alt.selection_single(name="SelectorName",fields=['cutoff'],bind=slider2,init={"cutoff": timestamp("2011-01-01")})
                    abssa = alt.Chart(df_new2).mark_bar(size=17).encode(
                        x='Year',
                        y=alt.Y('Income_INFLACION',title =None),
                        color=alt.condition(
                            'toDate(datum.Year) < SelectorName.cutoff[0]',
                          alt.value('red'), alt.value('blue')
                        )
                    ).properties(
                        width=700,
                    ).add_selection(
                        selector2
                    )
                    st.write(abssa)
                    ##########################################################################################################
                    ##      3. Graph 
                    st.markdown(html_IFPD_vizaulazacija3,unsafe_allow_html=True)
                    while True:
                        lines = alt.Chart(df_new).mark_bar(size=25).encode(
                          x=alt.X('Year',axis=alt.Axis(title='date')),
                          y=alt.Y('Income_by_player',axis=alt.Axis(title='value'))
                          ).properties(
                              width=600,
                              height=300
                          )
                        def plot_animation(df_new):
                            lines = alt.Chart(df_new).mark_bar(size=25).encode(
                            x=alt.X('Year', axis=alt.Axis(title='date')),
                            y=alt.Y('Income_by_player',axis=alt.Axis(title='value')),
                            ).properties(
                                width=600, 
                                height=300
                            )
                            return lines
                        N = df_new.shape[0] # number of elements in the dataframe
                        burst = 6       # number of elements (months) to add to the plot
                        size = burst    # size of the current dataset
                        line_plot = st.altair_chart(lines)
                        line_plot
                        start_btn3 = st.button('Start Income',key='sdsdadsda')
                        if start_btn3:
                            for i in range(1,N):
                                step_df = df_new.iloc[0:size]       
                                lines = plot_animation(step_df)
                                line_plot = line_plot.altair_chart(lines)
                                size = i + burst
                                if size >= N:
                                    size = N - 1  
                                time.sleep(0.1)
                        break
                    ##########################################################################################################
                    ##      4. Graph 
                    st.markdown(html_IFPD_vizaulazacija4,unsafe_allow_html=True)
                    while True:
                        lines = alt.Chart(df_new).mark_bar(size=25).encode(
                          x=alt.X('Year',axis=alt.Axis(title='date')),
                          y=alt.Y('Income_INFLACION',axis=alt.Axis(title='value'))
                          ).properties(
                              width=600,
                              height=300
                          )
                        def plot_animation(df_new):
                            lines = alt.Chart(df_new).mark_bar(size=25).encode(
                            x=alt.X('Year', axis=alt.Axis(title='date')),
                            y=alt.Y('Income_INFLACION',axis=alt.Axis(title='value')),
                            ).properties(
                                width=600, 
                                height=300
                            )
                            return lines
                        N = df_new.shape[0] # number of elements in the dataframe
                        burst = 6       # number of elements (months) to add to the plot
                        size = burst    # size of the current dataset
                        line_plot = st.altair_chart(lines)
                        line_plot
                        start_btn = st.button('Start Income',key='inflation')
                        if start_btn:
                            for i in range(1,N):
                                step_df = df_new.iloc[0:size]       
                                lines = plot_animation(step_df)
                                line_plot = line_plot.altair_chart(lines)
                                size = i + burst
                                if size >= N:
                                    size = N - 1  
                                time.sleep(0.1)
                        break
                    st.success("Viusalise  Datas")


        if st.checkbox(" Clubs Expenditures  "):
            st.info("club")   
            te = int(2)
            flag = return_id_CDWS_table(te)
            if flag != []:
                if int(te) > 0:
                    st.success("Visualization of top 22 Club Expenditures with year of expend")
                    st.success("Without inflation rate")
                    df = pd.read_sql_query('SELECT * FROM CDWS_table WHERE user_id = "{}"'.format(te),conn)
                    df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season","Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]]
                    df_new['Season']= pd.to_datetime(df_new['Season'],format='%Y')
                    df = df_new.nlargest(22,'Expenditures')
                    brush = alt.selection(type='interval')
                    points = alt.Chart(df).mark_point(size=200,filled=True).encode(
                        x='Season',
                        y='Expenditures',
                        color=alt.condition(brush, 'Club', alt.value('lightgray'))
                    ).add_selection(
                        brush
                    )
                    bars = alt.Chart(df).mark_bar().encode(
                        y='Club',
                        color='Club',
                        x='sum(Expenditures)'
                    ).transform_filter(
                        brush
                    )
                    st.write(points & bars)
                    st.success("Visualization of top 22 Club Expenditures with year of expend")
                    st.success("With inflation rate")
                    df2 = df_new.nlargest(22,'Inflacion_Expenditures')
                    brush1 = alt.selection(type='interval')
                    points1 = alt.Chart(df2).mark_point(size=200,filled=True).encode(
                        x='Season',
                        y='Inflacion_Expenditures',
                        color=alt.condition(brush1, 'Club', alt.value('lightgray'))
                    ).add_selection(
                        brush1
                    )
                    bars1 = alt.Chart(df2).mark_bar().encode(
                        y='Club',
                        color='Club',
                        x='sum(Inflacion_Expenditures)'
                    ).transform_filter(
                        brush1
                    )
                    st.write(points1 & bars1)           
                        











   