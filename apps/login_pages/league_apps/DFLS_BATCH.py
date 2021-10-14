from numpy.core.numeric import identity
import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from League_functions.DFLS_func import*
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_DFLS_BATCH()
    st.title('2. function DFLS_BATCH  process function')
    st.write('Welcome to metrics')
    username = return_username()
    i = (username[0])
    res = str(''.join(map(str, i)))
    return_user_idd = return_user_id(res)
    i = (return_user_idd[0])
    temp_save = int(''.join(map(str, i)))
    delite_temp_user(res)
    create_DFLS_BATCH()
    col1,col2 = st.columns(2)
    with col1:

        st.info(" For restart data you must delete data and start over !!!")
        if st.checkbox("Process data "):
            create_DFLS_BATCH_temp()
            df = pd.read_sql('SELECT * FROM League_datas', conn)
            df_new = df[["0","Nationality","Competition","Expenditures","Arrivals","Income","Departures","Balance","Year"]]
            to_append,rememmberr,flag_option = DFLS_MAIN(df_new)
            columns = ["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]    
            my_form = st.form(key = "form123")
            submit = my_form.form_submit_button(label = "Submit")
            if submit:                      
                columns = ["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]
                st.dataframe(to_append)                                
                return_user_idd = return_user_id(res)
                i = (return_user_idd[0])
                id = str(''.join(map(str, i)))
                create_DFLS_LEAGUE_flag_option()
                flag2 = return_id_DFLS__LEAGUE_flag_option(id)
                if flag2 == []:
                    insert_DFLS_LEAGUE_flag_option(flag_option,rememmberr,id)
                    df = to_append
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = id
                    df['user_id'] = list1
                    to_append.to_sql('DFLS_BATCH_temp',con=conn,if_exists='append')
                    a = view_all_DFLS__LEAGUE_flag_record(id)
                    st.success("Processed data you selected: : ")
                    for i in a:
                        st.write(''.join(map(str, i)))
                    #st.dataframe(to_append)
                elif flag2 != []:
                    i = (flag2[0])
                    result = str(''.join(map(str, i)))
                    if flag_option == result:
                        insert_DFLS_LEAGUE_flag_option(flag_option,rememmberr,id)
                        df = to_append
                        size = NumberOfRows(df)
                        size = len(df)
                        list1 = [0] * size
                        for i in range(0,size):
                            list1[i] = id
                        df['user_id'] = list1
                        to_append.to_sql('DFLS_BATCH_temp',con=conn,if_exists='append')
                        a = view_all_DFLS__LEAGUE_flag_record(id)
                        st.success("Processed data you selected: : ")
                        for i in a:
                            st.write(''.join(map(str, i)))
                        st.dataframe(to_append)  
                        st.success("Datas processes  successfully !!")
                    else:
                        st.warning("Please reppet your choose in search filter")
                        st.info("Leagues, Years and Nationality are different datas!!!")
                        st.info("Or Delite perviuos data !")
        # Save datas
        my_form_save = st.form(key = "form1")
        st.info("For process data you must save data to database")
        submit = my_form_save.form_submit_button(label = "Save data")
        if submit: 
            flag_id = return_id_DFLS_BATCH(temp_save)
            if flag_id == []:
                flag2 = return_id_DFLS_BATCH_temp(temp_save)
                if flag2 != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql('SELECT * FROM DFLS_BATCH_temp', conn)
                        df_save = df[["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season","user_id"]]
                        st.dataframe(df_save)
                        df_save.to_sql('DFLS_BATCH_table',con=conn,if_exists='append')
                        delite_DFLS_BATCH_temp(temp_save)
                        st.success("Data successfuly saved !")
                else:
                    st.warning("Please first proces jour data") 
            else:
                st.warning("Record already exisit please first delite datas !!")

        # Export datas
        form_export_csv = st.form(key = "export_form")
        submit = form_export_csv.form_submit_button(label = "Export datas")
        if submit:                                
            if submit:
                flag = return_id_DFLS_BATCH(temp_save)
                if flag != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql_query('SELECT * FROM DFLS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                        df_new = df[["Name_of_Legue","Expend","Income","Balance","number_of_Season",
                           "sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues",
                          "avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
                        st.markdown(get_table_download_link_csv(df_new), unsafe_allow_html=True)
                        st.success("Export Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !")

       # Delite datas 
        my_form_delite = st.form(key = "form_Delite")
        submit = my_form_delite.form_submit_button(label = "Delite datas")
        if submit:
            flag = return_id_DFLS_BATCH(temp_save)                             
            if flag != []:
                if int(temp_save) > 0 :
                    delite_DFLS_BATCH(temp_save)
                    delite_DFLS_LEAGUE_flag_option(temp_save)
                    #delite_DFLS_BATCH_temp(temp_save)
                    st.success("Delite Datas")
                    st.info("Please procces data")
            else:
                st.warning("file not found")
                st.info("Please procces data again !") 

        try:
            if st.checkbox("Viusalise data !!!"):
                flag = return_id_DFLS_BATCH(temp_save)
                if flag != []:

                    if int(temp_save) > 0:
                        flag_option = return_id_DFLS__LEAGUE_flag_option(temp_save)
                        temp_filter = ''.join(flag_option[0])
                        if flag_option !=[]:
                            if temp_filter == 'LEAUGE':
                                temp_option = "Name_of_Legue"
                                # 1. Graphs
                                df = pd.read_sql_query('SELECT * FROM DFLS_BATCH_table WHERE user_id = "{}"'.format(1),conn)
                                df_new = df[["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
                                
                                st.error("Repayment expenses with inflation rate")

                                base = alt.Chart(df_new)

                                bar = base.mark_bar().encode(
                                    x=alt.X('Expend'),
                                    y='Name_of_Legue'
                                ).properties(
                                
                                    width=700,
                                    height=250    
                                ).interactive()

                                st.write(bar)
                                st.error("Expend by leagues with inflation rate the thought players arrive in league")
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

                                #####################
                                #####################
                                #####################
                                # 2. Graphs

                                st.success("Revenue expenses with inflation rate")

                                base = alt.Chart(df_new)

                                bar = base.mark_bar().encode(
                                    x=alt.X('Income'),
                                    y='Name_of_Legue'
                                ).properties(
                                
                                    width=700,
                                    height=250    
                                ).interactive()

                                st.write(bar)
                                st.error("Revenue by leagues with inflation rate the thought players leave the league")
                                selection1 = alt.selection_multi(fields=['Name_of_Legue'], bind='legend')
                                c = alt.Chart(df).mark_circle().encode(
                                alt.X('sum_of_Depatrues', scale=alt.Scale(zero=True)),
                                alt.Y('Income', scale=alt.Scale(zero=True, padding=5)),
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

                                #####################
                                #####################
                                #####################
                                # 3. Graphs

                                st.success("Profit expenses with inflation rate")

                                base = alt.Chart(df_new)

                                bar = base.mark_bar().encode(
                                    x=alt.X('Balance'),
                                    y='Name_of_Legue'
                                ).properties(
                                
                                    width=700,
                                    height=250    
                                ).interactive()

                                st.write(bar)
                                st.error("Profit by leagues with inflation rate the thought players leave the league")
                                selection1 = alt.selection_multi(fields=['Name_of_Legue'], bind='legend')
                                c = alt.Chart(df).mark_circle().encode(
                                alt.X('sum_of_Depatrues', scale=alt.Scale(zero=True)),
                                alt.Y('Balance', scale=alt.Scale(zero=True, padding=5)),
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

                            elif temp_filter == 'Year':
                                temp_option = "Nationality"
                                df = pd.read_sql_query('SELECT * FROM DFLS_BATCH_table WHERE user_id = "{}"'.format(1),conn)
                                df_new = df[["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
                                st.error("Repayment expenses with inflation rate")

                                base = alt.Chart(df_new)

                                bar = base.mark_bar().encode(
                                    x=alt.X('Expend'),
                                    y='Name_of_Legue'
                                ).properties(
                                
                                    width=700,
                                    height=300    
                                ).interactive()

                                st.write(bar)
                                st.error("Expend by leagues with inflation rate the thought players arrive in league")
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

                                #####################
                                #####################
                                #####################
                                # 2. Graphs

                                st.success("Revenue expenses with inflation rate")

                                base = alt.Chart(df_new)

                                bar = base.mark_bar().encode(
                                    x=alt.X('Income'),
                                    y='Name_of_Legue'
                                ).properties(
                                
                                    width=700,
                                    height=300    
                                ).interactive()

                                st.write(bar)
                                st.error("Revenue by leagues with inflation rate the thought players leave the league")
                                selection1 = alt.selection_multi(fields=['Name_of_Legue'], bind='legend')
                                c = alt.Chart(df).mark_circle().encode(
                                alt.X('sum_of_Depatrues', scale=alt.Scale(zero=True)),
                                alt.Y('Income', scale=alt.Scale(zero=True, padding=5)),
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

                                #####################
                                #####################
                                #####################
                                # 3. Graphs

                                st.success("Profit expenses with inflation rate")

                                base = alt.Chart(df_new)

                                bar = base.mark_bar().encode(
                                    x=alt.X('Balance'),
                                    y='Name_of_Legue'
                                ).properties(
                                
                                    width=700,
                                    height=300    
                                ).interactive()

                                st.write(bar)
                                st.error("Profit by leagues with inflation rate the thought players leave the league")
                                selection1 = alt.selection_multi(fields=['Name_of_Legue'], bind='legend')
                                c = alt.Chart(df).mark_circle().encode(
                                alt.X('sum_of_Depatrues', scale=alt.Scale(zero=True)),
                                alt.Y('Balance', scale=alt.Scale(zero=True, padding=5)),
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
                                st.success("Viusalise  Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !!")
        except Exception as e:
            st.write(e)
            st.write("Error, please resart Visaulsation checkboc !! ") 

