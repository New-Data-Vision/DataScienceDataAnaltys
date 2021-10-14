from numpy.core.numeric import identity
import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from League_functions.DCWS_func import*
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_DCWS_BATCH()
    st.title('2. function DCWS_BATCH  process function')
    st.write('Welcome to metrics')
    username = return_username()
    i = (username[0])
    res = str(''.join(map(str, i)))
    return_user_idd = return_user_id(res)
    i = (return_user_idd[0])
    temp_save = int(''.join(map(str, i)))
    delite_temp_user(res)
    create_DCWS_BATCH()
    col1,col2 = st.columns(2)
    with col1:

        st.info(" For restart data you must delete data and start over !!!")
        if st.checkbox("Process data "):
            create_DCWS_BATCH_temp()
            df = pd.read_sql('SELECT * FROM League_datas', conn)
            df_new = df[["0","Nationality","Competition","Expenditures","Arrivals","Income","Departures","Balance","Year"]]
            to_append,rememmberr,flag_option = DCWS_MAIN(df_new)
            columns = ["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]    
            my_form = st.form(key = "form123")
            submit = my_form.form_submit_button(label = "Submit")
            if submit:
                                
                columns = ["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]
                st.dataframe(to_append)                                
                return_user_idd = return_user_id(res)
                i = (return_user_idd[0])
                id = str(''.join(map(str, i)))
                create_DCWS_LEAGUE_flag_option()
                flag2 = return_id_DCWS__LEAGUE_flag_option(id)
                if flag2 == []:
                    insert_DCWS_LEAGUE_flag_option(flag_option,rememmberr,id)
                    df = to_append
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = id
                    df['user_id'] = list1
                    to_append.to_sql('DCWS_BATCH_temp',con=conn,if_exists='append')
                    a = view_all_DCWS__LEAGUE_flag_record(id)
                    st.success("Processed data you selected: : ")
                    for i in a:
                        st.write(''.join(map(str, i)))
                elif flag2 != []:
                    i = (flag2[0])
                    result = str(''.join(map(str, i)))
                    if flag_option == result:
                        insert_DCWS_LEAGUE_flag_option(flag_option,rememmberr,id)
                        df = to_append
                        size = NumberOfRows(df)
                        size = len(df)
                        list1 = [0] * size
                        for i in range(0,size):
                            list1[i] = id
                        df['user_id'] = list1
                        to_append.to_sql('DCWS_BATCH_temp',con=conn,if_exists='append')
                        a = view_all_DCWS__LEAGUE_flag_record(id)
                        st.success("Processed data you selected: : ")
                        for i in a:
                            st.write(''.join(map(str, i)))
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
           
            flag_id = return_id_DCWS_BATCH(temp_save)
            if flag_id == []:
                flag2 = return_id_DCWS_BATCH_temp(temp_save)
                if flag2 != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql('SELECT * FROM DCWS_BATCH_temp', conn)
                        df_save = df[["Year_of_Season","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season","user_id"]]
                        st.dataframe(df_save)
                        df_save.to_sql('DCWS_BATCH_table',con=conn,if_exists='append')
                        delite_DCWS_BATCH_temp(temp_save)
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
                flag = return_id_DCWS_BATCH(temp_save)
                if flag != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql_query('SELECT * FROM DCWS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                        df_new = df[["Year_of_Season","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
                        st.markdown(get_table_download_link_csv(df_new), unsafe_allow_html=True)
                        st.success("Export Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !")

       # Delite datas 
        my_form_delite = st.form(key = "form_Delite")
        submit = my_form_delite.form_submit_button(label = "Delite datas")
        if submit:
            flag = return_id_DCWS_BATCH(temp_save)                             
            if flag != []:
                if int(temp_save) > 0 :
                    delite_DCWS_BATCH(temp_save)
                    delite_DCWS_LEAGUE_flag_option(temp_save)
                    #delite_DCWS_BATCH_temp(temp_save)
                    st.success("Delite Datas")
                    st.info("Please procces data")
            else:
                st.warning("file not found")
                st.info("Please procces data again !") 

        try:
            if st.checkbox("Viusalise data !!!"):
                flag = return_id_DCWS_BATCH(temp_save)
                if flag != []:
    # 
                    if int(temp_save) > 0:
                        flag_option = return_id_DCWS__LEAGUE_flag_option(temp_save)
                        temp_filter = ''.join(flag_option[0])
                        if flag_option !=[]:
                            if temp_filter == 'Year_of_Season':
                                st.write(temp_filter)

                                df = pd.read_sql_query('SELECT * FROM DCWS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Year_of_Season","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
                                df_new['Year_of_Season']= pd.to_datetime(df_new['Year_of_Season'],format='%Y')                           
                                base = alt.Chart(df_new).encode(
                                    alt.X('Year_of_Season', axis=alt.Axis(title=None))
                                )                          
                                area = base.mark_point(size=200,filled=True, color='#57A44C').encode(
                                    alt.Y('Expend',
                                          axis=alt.Axis(title='profit', titleColor='#57A44C')),
                                    #alt.Y2('Income')
                                    #size=alt.Size('count', scale=alt.Scale(range=[100, 500]))
                                )
                                line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
                                    alt.Y('sum_of_Arrivlas',
                                          axis=alt.Axis(title='number of arrivals', titleColor='#5276A7'))
                                )
                                b = alt.layer(area, line).resolve_scale(
                                    y = 'independent'
                                ).properties(
                                    width=700,
                                    height=400
                                ).configure_point(
                                    size=500
                                ).interactive()   
                                st.write(b)
                                st.success("Viusalise  Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !!")
        except Exception as e:
          st.write("Error, please resart Visaulsation checkboc !! ") 

