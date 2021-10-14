from numpy.core.numeric import identity
import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from League_functions.BFPD_func import*
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_BFPD_BATCH()
    st.title('2. function BFPD_BATCH  process function')
    st.write('Welcome to metrics')
    username = return_username()
    i = (username[0])
    res = str(''.join(map(str, i)))
    return_user_idd = return_user_id(res)
    i = (return_user_idd[0])
    temp_save = int(''.join(map(str, i)))
    delite_temp_user(res)
    create_BFPD_BATCH()
    col1,col2 = st.columns(2)
    with col1:

        st.info(" For restart data you must delete data and start over !!!")
        if st.checkbox("Process data "):
            create_BFPD_BATCH_temp()
            #create_BFPD__LEAGUE_table()
            df = pd.read_sql('SELECT * FROM League_datas', conn)
            df_new = df[["0","Nationality","Competition","Expenditures","Arrivals","Income","Departures","Balance","Year"]]
            to_append,rememmberr,flag_option = BFPD_MAIN(df_new)
            columns = ["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]    
            my_form = st.form(key = "form123")
            submit = my_form.form_submit_button(label = "Submit")
            if submit:
                                
                columns = ["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]
                st.dataframe(to_append)                                
                return_user_idd = return_user_id(res)
                i = (return_user_idd[0])
                id = str(''.join(map(str, i)))
                create_BFPD_LEAGUE_flag_option()
                flag2 = return_id_BFPD__LEAGUE_flag_option(id)
                if flag2 == []:
                    insert_BFPD_LEAGUE_flag_option(flag_option,rememmberr,id)
                    df = to_append
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = id
                    df['user_id'] = list1
                    to_append.to_sql('BFPD_BATCH_temp',con=conn,if_exists='append')
                    a = view_all_BFPD__LEAGUE_flag_record(id)
                    st.success("Processed data you selected: : ")
                    for i in a:
                        st.write(''.join(map(str, i)))
                    st.dataframe(to_append)  
                elif flag2 != []:
                    i = (flag2[0])
                    result = str(''.join(map(str, i)))
                    if flag_option == result:
                        insert_BFPD_LEAGUE_flag_option(flag_option,rememmberr,id)
                        df = to_append
                        size = NumberOfRows(df)
                        size = len(df)
                        list1 = [0] * size
                        for i in range(0,size):
                            list1[i] = id
                        df['user_id'] = list1
                        to_append.to_sql('BFPD_BATCH_temp',con=conn,if_exists='append')
                        a = view_all_BFPD__LEAGUE_flag_record(id)
                        st.success("Processed data you selected: : ")
                        for i in a:
                            st.write(''.join(map(str, i)))
                        st.dataframe(to_append)  
                    else:
                        st.warning("Please reppet your choose in search filter")
                        st.info("Leagues, Years and Nationality are different datas!!!")
                        st.info("Or Delite perviuos data !")

        # Save datas
        my_form_save = st.form(key = "form1")
        st.info("For process data you must save data to database")
        submit = my_form_save.form_submit_button(label = "Save data")
        if submit:
           
            flag_id = return_id_BFPD_BATCH(temp_save)
            if flag_id == []:
                flag2 = return_id_BFPD_BATCH_temp(temp_save)
                if flag2 != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql('SELECT * FROM BFPD_BATCH_temp', conn)
                        df_save = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                        st.dataframe(df_save)
                        df_save.to_sql('BFPD_BATCH_table',con=conn,if_exists='append')
                        delite_BFPD_BATCH_temp(temp_save)
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
                flag = return_id_BFPD_BATCH(temp_save)
                if flag != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                        df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                        st.markdown(get_table_download_link_csv(df_new), unsafe_allow_html=True)
                        st.success("Export Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !")

       # Delite datas 
        my_form_delite = st.form(key = "form_Delite")
        submit = my_form_delite.form_submit_button(label = "Delite datas")
        if submit:
            flag = return_id_BFPD_BATCH(temp_save)                             
            if flag != []:
                if int(temp_save) > 0 :
                    delite_BFPD_BATCH(temp_save)
                    delite_BFPD_LEAGUE_flag_option(temp_save)
                    #delite_BFPD_BATCH_temp(temp_save)
                    st.success("Delite Datas")
                    st.info("Please procces data")
            else:
                st.warning("file not found")
                st.info("Please procces data again !") 

        try:
            if st.checkbox("Viusalise data !!!"):
                flag = return_id_BFPD_BATCH(temp_save)
                if flag != []:
                    if int(temp_save) > 0:
                        flag_option = return_id_BFPD__LEAGUE_flag_option(temp_save)
                        temp_filter = ''.join(flag_option[0])
                        if flag_option !=[]:
                            if temp_filter == 'LEAUGE':
                                temp_option = "Name_of_Legue"
                                st.success("Visualization of profit by the player by League")
                                ##      1. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                                brush = alt.selection(type='interval')
                                points = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    color=alt.condition(brush, 'Name_of_Legue', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                ).properties(
                                    width=500,
                                    height=400
                                )
                                bars = alt.Chart(df_new).mark_bar().encode(
                                    y=alt.Y('Name_of_Legue', axis=alt.Axis( title='Name of Legue')),

                                    color='Name_of_Legue',
                                    x=alt.Y('Balance_by_player', axis=alt.Axis( title='Income by player')),
                                ).transform_filter(
                                    brush
                                ).properties(
                                    width=500,
                                    height=100
                                )
                                st.write(points & bars)
                                st.success("Viusalise  Datas")
                                #   ---------------------------------------------------------------
                                ##      2. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                                nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                                        fields=['Balance_by_player'], empty='none')

                                line = alt.Chart(df_new).mark_line(interpolate='basis').encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    color='Name_of_Legue'
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                selectors = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                points = line.mark_point().encode(
                                    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                                )
                                text = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest, 'Balance_by_player', alt.value(' '))
                                )
                                rules = alt.Chart(df_new).mark_rule(color='gray').encode(
                                    x='Year',
                                ).transform_filter(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                a = alt.layer(
                                    line, selectors, points, rules, text
                                ).properties(
                                    width=700, height=300
                                )
                                st.write(a)
                                #   ---------------------------------------------------------------
                                ##      3. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                                highlight = alt.selection(type='single', on='mouseover',
                                                      fields=['Name_of_Legue'], nearest=True)
                                base = alt.Chart(df_new).encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    color='Name_of_Legue'
                                )
                                points = base.mark_circle().encode(
                                    opacity=alt.value(0)
                                ).add_selection(
                                    highlight
                                ).properties(
                                    width=700, height=400
                                )
                                lines = base.mark_line().encode(
                                    size=alt.condition(~highlight, alt.value(1), alt.value(3))
                                )
                                points + lines
                                st.write(points + lines)
                                #   ---------------------------------------------------------------
                                st.success("Visualization of profit by the player by League with inflation the rate")                                #   ---------------------------------------------------------------
                                ##      1. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')

                                brush = alt.selection(type='interval')
                                points = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    color=alt.condition(brush, 'Name_of_Legue', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                ).properties(
                                    width=500,
                                    height=400
                                )
                                bars = alt.Chart(df_new).mark_bar().encode(
                                    y=alt.Y('Name_of_Legue', axis=alt.Axis( title='Name of Legue')),

                                    color='Name_of_Legue',
                                    x=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                ).transform_filter(
                                    brush
                                ).properties(
                                    width=500,
                                    height=100
                                )
                                st.write(points & bars)
                                st.success("Viusalise  Datas")
                                #   ---------------------------------------------------------------
                                ##      2. Graph 
                                # Create a selection that chooses the nearest point & selects based on x-value
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                                nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                                        fields=['Balance_INFLACION'], empty='none')
                                # The basic line
                                line = alt.Chart(df_new).mark_line(interpolate='basis').encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    color='Name_of_Legue'
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                # Draw points on the line, and highlight based on selection
                                points = line.mark_point().encode(
                                    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                                )
                                # Draw text labels near the points, and highlight based on selection
                                text = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest, 'Balance_INFLACION', alt.value(' '))
                                )
                                # Draw a rule at the location of the selection
                                rules = alt.Chart(df_new).mark_rule(color='gray').encode(
                                    x='Year',
                                ).transform_filter(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                # Put the five layers into a chart and bind the data
                                a = alt.layer(
                                    line, selectors, points, rules, text
                                ).properties(
                                    width=700, height=300
                                )
                                st.write(a)
                                #   ---------------------------------------------------------------
                                ##      3. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                                highlight = alt.selection(type='single', on='mouseover',
                                                      fields=['Name_of_Legue'], nearest=True)
                                base = alt.Chart(df_new).encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    color='Name_of_Legue'
                                )
                                points = base.mark_circle().encode(
                                    opacity=alt.value(0)
                                ).add_selection(
                                    highlight
                                ).properties(
                                    width=700, height=400
                                )
                                lines = base.mark_line().encode(
                                    size=alt.condition(~highlight, alt.value(1), alt.value(3))
                                )
                                points + lines
                                st.write(points + lines)
                                #   ---------------------------------------------------------------
                                st.success("Viusalise  Datas")
                            elif temp_filter == 'Year_of_Season':
                                temp_option = "Year"
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]] 
                                st.warning("Without the inflation rate")          
                                st.success("Visualization of profit per the player according to the selected season")
                                error_bars = alt.Chart(df_new).mark_errorbar(extent='ci').encode(
                                  x=alt.X('Balance_by_player', scale=alt.Scale(zero=False)),
                                  y=alt.Y('Year'),
                                  color =  'Year'
                                ).properties(
                                    width=600,
                                    height=500
                                ).interactive()
                                points = alt.Chart(df_new).mark_point(filled=True, color='black',size=90).encode(
                                  x=alt.X('Balance_by_player', aggregate='mean'),
                                  y=alt.Y('Year'),
                                  color =  'Year'
                                ).properties(
                                    width=600,
                                    height=500
                                ).interactive()
                                error_bars + points
                                st.write(error_bars + points)
                                st.success("Visualization of profit per the player according to the selected season")
                                test = alt.Chart(df_new).mark_circle(size=60).encode(
                                    y=alt.Y('Balance_by_player', axis=alt.Axis(title=None)),
                                    x=alt.X('Nationality', axis=alt.Axis(labels=False,title=None)),
                                    color='Year'
                                ).properties(
                                    width=600,
                                    height=500
                                ).interactive()
                                st.write(test)
                                st.success("Visualization of profit per the player according to the selected season")
                                brush = alt.selection(type='interval')
                                points = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Name_of_Legue', axis=alt.Axis(labels=False,title=None)),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    color=alt.condition(brush, 'Year', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                ).properties(
                                    width=500,
                                    height=400)
                                bars = alt.Chart(df_new).mark_bar().encode(
                                    y=alt.Y('Year', axis=alt.Axis( title='Year')),
                                    color='Balance_by_player',
                                    x=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                ).transform_filter(
                                    brush
                                ).properties(
                                    width=500,
                                    height=100)
                                st.write(points & bars)
                                ###########################
                                ###########################
                                ###########################
                                st.error("With the inflation rate")          
                                st.success("Visualization of profit per the player according to the selected season")
                                error_bars = alt.Chart(df_new).mark_errorbar(extent='ci').encode(
                                  x=alt.X('Balance_INFLACION', scale=alt.Scale(zero=False)),
                                  y=alt.Y('Year'),
                                  color =  'Year'
                                ).properties(
                                    width=600,
                                    height=500
                                ).interactive()
                                points = alt.Chart(df_new).mark_point(filled=True, color='black',size=90).encode(
                                  x=alt.X('Balance_INFLACION', aggregate='mean'),
                                  y=alt.Y('Year'),
                                  color =  'Year'
                                ).properties(
                                    width=600,
                                    height=500
                                ).interactive()
                                error_bars + points
                                st.write(error_bars + points)
                                st.success("Visualization of profit per the player according to the selected season")
                                test = alt.Chart(df_new).mark_circle(size=60).encode(
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis(title=None)),
                                    x=alt.X('Nationality', axis=alt.Axis(labels=False,title=None)),
                                    color='Year'
                                ).properties(
                                    width=600,
                                    height=500
                                ).interactive()
                                st.write(test)
                                st.success("Visualization of profit per the player according to the selected season")
                                brush = alt.selection(type='interval')
                                points = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Name_of_Legue', axis=alt.Axis(labels=False,title=None)),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player')),
                                    color=alt.condition(brush, 'Year', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                ).properties(
                                    width=500,
                                    height=400)
                                bars = alt.Chart(df_new).mark_bar().encode(
                                    y=alt.Y('Year', axis=alt.Axis( title='Year')),
                                    color='Balance_INFLACION',
                                    x=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player')),
                                ).transform_filter(
                                    brush
                                ).properties(
                                    width=500,
                                    height=100)
                                st.write(points & bars)
                                st.success("Viusalise  Datas")                                                         
                            elif temp_filter == 'Nationality':
                                temp_option = "Nationality"
                                st.success("Visualization of profit by the player by Nationality")
                                #   ---------------------------------------------------------------
                                ##      1. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')

                                brush = alt.selection(type='interval')
                                points = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    color=alt.condition(brush, 'Nationality', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                ).properties(
                                    width=500,
                                    height=400
                                )
                                bars = alt.Chart(df_new).mark_bar().encode(
                                    y=alt.Y('Nationality', axis=alt.Axis( title='Nationality')),

                                    color='Nationality',
                                    x=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                ).transform_filter(
                                    brush
                                ).properties(
                                    width=500,
                                    height=100
                                )
                                st.write(points & bars)
                                st.success("Viusalise  Datas")
                                #   ---------------------------------------------------------------
                                ##      2. Graph 
                                # Create a selection that chooses the nearest point & selects based on x-value
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                                nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                                        fields=['Balance_by_player'], empty='none')
                                line = alt.Chart(df_new).mark_line(interpolate='basis').encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    color='Nationality'
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                selectors = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                points = line.mark_point().encode(
                                    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                                )
                                text = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest, 'Balance_by_player', alt.value(' '))
                                )
                                rules = alt.Chart(df_new).mark_rule(color='gray').encode(
                                    x='Year',
                                ).transform_filter(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                a = alt.layer(
                                    line, selectors, points, rules, text
                                ).properties(
                                    width=700, height=300
                                )
                                st.write(a)
                                #   ---------------------------------------------------------------
                                ##      3. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')

                                highlight = alt.selection(type='single', on='mouseover',
                                                      fields=['Nationality'], nearest=True)
                                base = alt.Chart(df_new).encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_by_player', axis=alt.Axis( title='Balance by player')),
                                    color='Nationality'
                                )
                                points = base.mark_circle().encode(
                                    opacity=alt.value(0)
                                ).add_selection(
                                    highlight
                                ).properties(
                                    width=700, height=400
                                )
                                lines = base.mark_line().encode(
                                    size=alt.condition(~highlight, alt.value(1), alt.value(3))
                                )

                                points + lines
                                st.write(points + lines)
                                #   ---------------------------------------------------------------
                                st.success("Visualization of profit by the player by Nationality with inflation the rate") 
                                #   ---------------------------------------------------------------
                                ##      1. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')

                                brush = alt.selection(type='interval')
                                points = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    color=alt.condition(brush, 'Nationality', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                ).properties(
                                    width=500,
                                    height=400
                                )
                                bars = alt.Chart(df_new).mark_bar().encode(
                                    y=alt.Y('Nationality', axis=alt.Axis( title='Name of Legue')),

                                    color='Nationality',
                                    x=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                ).transform_filter(
                                    brush
                                ).properties(
                                    width=500,
                                    height=100
                                )
                                st.write(points & bars)
                                st.success("Viusalise  Datas")
                                #   ---------------------------------------------------------------
                                ##      2. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')
                                nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                                        fields=['Balance_INFLACION'], empty='none')

                                line = alt.Chart(df_new).mark_line(interpolate='basis').encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    color='Nationality'
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                selectors = alt.Chart(df_new).mark_point().encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                points = line.mark_point().encode(
                                    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                                )
                                text = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest, 'Balance_INFLACION', alt.value(' '))
                                )
                                rules = alt.Chart(df_new).mark_rule(color='gray').encode(
                                    x='Year',
                                ).transform_filter(
                                    nearest
                                ).properties(
                                    width=700,
                                    height=600
                                )
                                a = alt.layer(
                                    line, selectors, points, rules, text
                                ).properties(
                                    width=700, height=300
                                )
                                st.write(a)
                                #   ---------------------------------------------------------------
                                ##      3. Graph 
                                df = pd.read_sql_query('SELECT * FROM BFPD_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_new = df[["Name_of_Legue","Year","Nationality","Balance_by_player","Balance_INFLACION"]]
                                df_new['Year']= pd.to_datetime(df_new['Year'],format='%Y')

                                highlight = alt.selection(type='single', on='mouseover',
                                                      fields=['Nationality'], nearest=True)

                                base = alt.Chart(df_new).encode(
                                    x=alt.X('Year', axis=alt.Axis(title='Date')),
                                    y=alt.Y('Balance_INFLACION', axis=alt.Axis( title='Balance by player + INFLACION')),
                                    color='Nationality'
                                )
                                points = base.mark_circle().encode(
                                    opacity=alt.value(0)
                                ).add_selection(
                                    highlight
                                ).properties(
                                    width=700, height=400
                                )
                                lines = base.mark_line().encode(
                                    size=alt.condition(~highlight, alt.value(1), alt.value(3))
                                )
                                points + lines
                                st.write(points + lines)
                                #   ---------------------------------------------------------------
                                st.success("Viusalise  Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !!")
        except Exception as e:
          st.write("Error, please resart Visaulsation checkboc !! ") 

