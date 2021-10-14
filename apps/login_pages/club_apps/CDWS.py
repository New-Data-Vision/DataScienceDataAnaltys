import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from Club_functions.CDWS_func import CDWS_base
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_CDWS()
    st.title('1. function CDWS  process function')
    st.write('Welcome to metrics')
    username = return_username()

    i = (username[0])
    res = str(''.join(map(str, i)))

    delite_temp_user(res)
    create_CDWS()
    col1,col2 = st.columns(2)
    with col1:
                            
        st.info(" For restart data you must delete data and start over !!!")
        # Processd data
        if st.checkbox("Process data"):
            df = pd.read_sql('SELECT * FROM Clubs_datas', conn)
            df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season"]]
            st.dataframe(df_new)
            a_leuge_DF = CDWS_base(df_new)
            my_form = st.form(key = "form123")
            submit = my_form.form_submit_button(label = "Submit")
            if submit:
                st.success("Datas processes  :")
            my_form_save = st.form(key = "form1")
            st.info("For process data you must save data to database")
            submit = my_form_save.form_submit_button(label = "Save data")
            if submit:
                return_user_idd = return_user_id(res)
                i = (return_user_idd[0])
                res = int(''.join(map(str, i)))
                te = int(res)
                flag = return_id_CDWS_table(te)
                if flag == []:
                    df = a_leuge_DF
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = te
                    df['user_id'] = list1
                    create_CDWS()
                    df.to_sql('CDWS_table',con=conn,if_exists='append')
                    st.success("Data successfuly saved !")

                else:
                    st.warning("Please first delite your records from database !!")
        # Export datas
        form_export_csv = st.form(key = "export_form")
        submit = form_export_csv.form_submit_button(label = "Export datas")
        if submit:                                
            if submit:
                return_user_idd = return_user_id(res)
                i = (return_user_idd[0])
                res = int(''.join(map(str, i)))
                te = int(res)
                flag = return_id_CDWS_table(te)
                if flag != []:
                    if int(te) > 0:
                        df = pd.read_sql_query('SELECT * FROM CDWS_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season","Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]]
                        st.markdown(get_table_download_link_csv(df_new), unsafe_allow_html=True)
                        st.success("Export Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !")
        # Delite datas 
        my_form_delite = st.form(key = "form12")
        submit = my_form_delite.form_submit_button(label = "Delite datas")
        if submit:
            return_user_idd = return_user_id(res)
            i = (return_user_idd[0])
            res = int(''.join(map(str, i)))
            te = int(res)
            flag = (return_id_CDWS_table(te))                               
            if flag != []:
                if int(te) > 0 :
                    delite_CDWS(te)
                    st.success("Delite Datas")
                    st.info("Please procces data")
            else:
                st.warning("file not found")
                st.info("Please procces data again !")
        try:
            if st.checkbox("Viusalise data !!!"):
                # Viusalise datas
                #st.write("Viusalise datas",res)
                return_user_idd = return_user_id(res)
                st.write("")
                i = (return_user_idd[0])
                res = int(''.join(map(str, i)))
                te = int(res)
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

                        
                        st.success("Viusalise  Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !!")

        except Exception as e:
          st.write("Error, please resart Visaulsation checkboc !! ") 