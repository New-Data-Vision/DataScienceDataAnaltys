import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from League_functions.DFLS_func import DFLS_base
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_DFLS()
    st.title('1. function IFPA  process function')
    st.write('Welcome to metrics')
    username = return_username()

    i = (username[0])
    res = str(''.join(map(str, i)))

    delite_temp_user(res)
    col1,col2 = st.columns(2)
    with col1:
                            
        st.info(" For restart data you must delete data and start over !!!")
        # Processd data
        if st.checkbox("Process data"):
            df = pd.read_sql('SELECT * FROM League_datas', conn)
            df_new = df[["0","Nationality","Competition","Expenditures","Arrivals","Income","Departures","Balance","Year"]]
            st.dataframe(df_new)
            a_leuge_DF = DFLS_base(df_new)
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
                flag = return_id_DFLS_table(te)
                if flag == []:
                    df = a_leuge_DF
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = te
                    df['user_id'] = list1
                    create_DFLS()
                    df.to_sql('DFLS_table',con=conn,if_exists='append')
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
                flag = return_id_DFLS_table(te)
                if flag != []:
                    if int(te) > 0:
                        df = pd.read_sql_query('SELECT * FROM DFLS_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
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
            flag = (return_id_DFLS_table(te))                               
            if flag != []:
                if int(te) > 0 :
                    delite_DFLS(te)
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
                flag = return_id_DFLS_table(te)
                if flag != []:
                    if int(te) > 0:
                        st.info("Interactive visaulsation !!")
                        df = pd.read_sql_query('SELECT * FROM DFLS_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
                        df = df_new.nlargest(10, 'Expend')

                        # Graph 1.
                        st.success("Expend by leagues with the inflation coefficient throw number of players come to the leauge")
                        st.info("Top 10 leauges by the Expend")
                        selection1 = alt.selection_multi(fields=['Name_of_Legue'], bind='legend')

                        c = alt.Chart(df).mark_circle().encode(
                        alt.X('sum_of_Arrivlas', scale=alt.Scale(zero=True)),
                        alt.Y('Expend', scale=alt.Scale(zero=True, padding=5)),
                        alt.Color('Name_of_Legue', scale=alt.Scale(scheme='category20b')),
                        opacity=alt.condition(selection1, alt.value(1), alt.value(0.2)),
                        size='number_of_Season'
                        ).add_selection(
                            selection1
                        ).properties(
                            width = 700,
                            height = 600
                        ).interactive()
                        st.altair_chart(c)

                        # Graph 2.
                        st.success("Revenues by leagues with inflation rates throw the number of players who leave the league")
                        st.info("Top 10 leauges by the Revenues")
                        selection2 = alt.selection_multi(fields=['Name_of_Legue'], bind='legend')

                        df2 = df_new.nlargest(10, 'Income')
                        b = alt.Chart(df2).mark_circle().encode(
                        alt.X('sum_of_Depatrues', scale=alt.Scale(zero=True)),
                        alt.Y('Income', scale=alt.Scale(zero=True, padding=5)),
                        alt.Color('Name_of_Legue', scale=alt.Scale(scheme='category20b')),
                        opacity=alt.condition(selection2, alt.value(1), alt.value(0.2)),
                        size='number_of_Season'
                        ).add_selection(
                            selection2
                        ).properties(
                            width = 700,
                            height = 600
                        ).interactive()
                        st.write(b)

                        # Graph 3.
                        st.success("Profit by leagues with inflation rates throw the number of players who come in the league")
                        st.info("Top 10 leauges by the profit")
                        selection3 = alt.selection_multi(fields=['Name_of_Legue'], bind='legend')

                        df3 = df_new.nlargest(10, 'Balance')
                        a = alt.Chart(df3).mark_circle().encode(
                        alt.X('sum_of_Arrivlas', scale=alt.Scale(zero=True)),
                        alt.Y('Balance', scale=alt.Scale(zero=True, padding=5)),
                        alt.Color('Name_of_Legue', scale=alt.Scale(scheme='category20b')),
                        opacity=alt.condition(selection3, alt.value(1), alt.value(0.2)),
                        size='number_of_Season'
                        ).add_selection(
                            selection3
                        ).properties(
                            width = 700,
                            height = 600
                        ).interactive()
                        st.write(a)
                        
                else:

                    st.warning("file not found")
                    st.info("Please procces data again !!")

        except Exception as e:

            st.write(e)
            st.write("Error, please resart Visaulsation checkboc !! ") 