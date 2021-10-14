import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from League_functions.IFPD_func import IFPD_base
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_IFPD()
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
            a_leuge_DF = IFPD_base(df_new)
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
                flag = return_id_IFPD_table(te)
                if flag == []:
                    df = a_leuge_DF
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = te
                    df['user_id'] = list1
                    create_IFPD()
                    df.to_sql('IFPD_table',con=conn,if_exists='append')
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
                flag = return_id_IFPD_table(te)
                if flag != []:
                    if int(te) > 0:
                        df = pd.read_sql_query('SELECT * FROM IFPD_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"]]
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
            flag = (return_id_IFPD_table(te))                               
            if flag != []:
                if int(te) > 0 :
                    delite_IFPD(te)
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
                flag = return_id_IFPD_table(te)
                if flag != []:
                    if int(te) > 0:
                        ##      1. Graph 
                        df = pd.read_sql_query('SELECT * FROM IFPD_table WHERE user_id = "{}"'.format(te),conn)
                        df.columns.name = None
                        #st.dataframe(df)
                        df_new = df[["Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"]]
                        df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')

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
                            start_btn = st.button('Start')
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
                            start_btn = st.button('Start',key='234sa')
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
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !!")

        except Exception as e:
          st.write("Error, please resart Visaulsation checkboc !! ") 