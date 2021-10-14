import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from Club_functions.CDTAS_func import DCTAS_base
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_DCTAS()
    st.title('1. function DCTAS  process function')
    st.write('Welcome to metrics')
    username = return_username()

    i = (username[0])
    res = str(''.join(map(str, i)))

    delite_temp_user(res)
    create_DCTAS()
    col1,col2 = st.beta_columns(2)
    with col1:
                            
        st.info(" For restart data you must delete data and start over !!!")
        # Processd data
        if st.checkbox("Process data"):
            df = pd.read_sql('SELECT * FROM Clubs_datas', conn)
            df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season"]]
            st.dataframe(df_new)
            a_leuge_DF = DCTAS_base(df_new)
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
                flag = return_id_DCTAS_table(te)
                if flag == []:
                    df = a_leuge_DF
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = te
                    df['user_id'] = list1
                    create_DCTAS()
                    st.success("Data successfuly saved !")
                    df.to_sql('DCTAS_table',con=conn,if_exists='append')
                    

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
                flag = return_id_DCTAS_table(te)
                if flag != []:
                    if int(te) > 0:
                        df = pd.read_sql_query('SELECT * FROM DCTAS_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]]
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
            flag = (return_id_DCTAS_table(te))                               
            if flag != []:
                if int(te) > 0 :
                    delite_DCTAS(te)
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
                flag = return_id_DCTAS_table(te)
                if flag != []:
                    if int(te) > 0:
                        df = pd.read_sql_query('SELECT * FROM DCTAS_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]]
                        
                        st.error("Visualization of the top 10 club expenses from 2000 to now")
                        st.error("Without inflation rate")
                        dff = df_new.nlargest(10,'Expenditures')

                        brush = alt.selection(type='interval')

                        points = alt.Chart(dff).mark_point(size=200,filled=True).encode(
                            x='Arrivals',
                            y='Expenditures',
                            color=alt.condition(brush, 'Club', alt.value('lightgray'))
                        ).add_selection(
                            brush
                        )

                        bars = alt.Chart(dff).mark_bar().encode(
                            y='Club',
                            color='Club',
                            x='Expenditures'
                        ).transform_filter(
                            brush
                        )

                        st.write(points & bars)


                        st.error("With inflation rate")
                        dff2 = df_new.nlargest(10,'inflation_Expenditure')
                        brush1 = alt.selection(type='interval')
                        points1 = alt.Chart(dff2).mark_point(size=200,filled=True).encode(
                            x='Arrivals',
                            y='inflation_Expenditure',
                            color=alt.condition(brush1, 'Club', alt.value('lightgray'))
                        ).add_selection(
                            brush1
                        )

                        bars1 = alt.Chart(dff2).mark_bar().encode(
                            y='Club',
                            color='Club',
                            x='inflation_Expenditure'
                        ).transform_filter(
                            brush1
                        )
                        st.write(points1 & bars1)

                        ################
                        ################

                        st.success("Visualization of the top 10 club revenue from 2000 to now")
                        st.success("Without inflation rate")
                        dffR = df_new.nlargest(10,'Income')

                        brush_r1 = alt.selection(type='interval')

                        points_r1 = alt.Chart(dffR).mark_point(size=200,filled=True).encode(
                            x='Arrivals',
                            y='Income',
                            color=alt.condition(brush_r1, 'Club', alt.value('lightgray'))
                        ).add_selection(
                            brush_r1
                        )

                        bars_r1 = alt.Chart(dffR).mark_bar().encode(
                            y='Club',
                            color='Club',
                            x='Income'
                        ).transform_filter(
                            brush_r1
                        )
                        st.write(points_r1 & bars_r1)

                        st.success("With inflation rate")
                        dffR2 = df_new.nlargest(10,'inflation_Income')

                        brush_r2 = alt.selection(type='interval')

                        points_r2 = alt.Chart(dffR2).mark_point(size=200,filled=True).encode(
                            x='Arrivals',
                            y='inflation_Income',
                            color=alt.condition(brush_r2, 'Club', alt.value('lightgray'))
                        ).add_selection(
                            brush_r2
                        )

                        bars_r2 = alt.Chart(dffR2).mark_bar().encode(
                            y='Club',
                            color='Club',
                            x='inflation_Income'
                        ).transform_filter(
                            brush_r2
                        )
                        st.write(points_r2 & bars_r2)

                        ################
                        ################

                        st.success("Visualization of the top 10 club profit from 2000 to now")
                        st.success("Without inflation rate")
                        dffP = df_new.nlargest(10,'Balance')

                        brush_p1 = alt.selection(type='interval')

                        points_p1 = alt.Chart(dffP).mark_point(size=200,filled=True).encode(
                            x='Arrivals',
                            y='Balance',
                            color=alt.condition(brush_p1, 'Club', alt.value('lightgray'))
                        ).add_selection(
                            brush_p1
                        )

                        bars_p1 = alt.Chart(dffP).mark_bar().encode(
                            y='Club',
                            color='Club',
                            x='Balance'
                        ).transform_filter(
                            brush_p1
                        )
                        st.write(points_p1 & bars_p1)

                        st.success("With inflation rate")
                        dffP2 = df_new.nlargest(10,'inflation_Balance')

                        brush_p2 = alt.selection(type='interval')

                        points_p2 = alt.Chart(dffP2).mark_point(size=200,filled=True).encode(
                            x='Arrivals',
                            y='inflation_Balance',
                            color=alt.condition(brush_p2, 'Club', alt.value('lightgray'))
                        ).add_selection(
                            brush_p2
                        )

                        bars_p2 = alt.Chart(dffP2).mark_bar().encode(
                            y='Club',
                            color='Club',
                            x='inflation_Balance'
                        ).transform_filter(
                            brush_p2
                        )
                        st.write(points_p2 & bars_p2)

                        st.success("Viusalise  Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !!")

        except Exception as e:
          st.write("Error, please resart Visaulsation checkboc !! ") 