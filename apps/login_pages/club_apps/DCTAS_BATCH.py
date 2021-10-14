from numpy.core.numeric import identity
import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from Club_functions.CDTAS_func import *
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_DCTAS_BATCH()
    st.title('2. function DCTAS_BATCH  process function')
    st.write('Welcome to metrics')
    username = return_username()
    i = (username[0])
    res = str(''.join(map(str, i)))
    return_user_idd = return_user_id(res)
    i = (return_user_idd[0])
    temp_save = int(''.join(map(str, i)))
    delite_temp_user(res)
    create_DCTAS_BATCH()
    col1,col2 = st.columns(2)
    with col1:

        st.info(" For restart data you must delete data and start over !!!")
        if st.checkbox("Process data "):
            create_DCTAS_BATCH_temp()
            create_DCTAS_LEAGUE_flag_option()
            df = pd.read_sql('SELECT * FROM Clubs_datas', conn)
            df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season"]]
            to_append,rememmberr,flag_option = DCTAS_MAIN(df_new)
            columns = ["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]    
            my_form = st.form(key = "form123")
            submit = my_form.form_submit_button(label = "Submit")
            if submit:
                                
                columns = ["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]
                st.dataframe(to_append)                                
                return_user_idd = return_user_id(res)
                i = (return_user_idd[0])
                id = str(''.join(map(str, i)))
                return_id_DCTAS__LEAGUE_flag_option(temp_save)
                flag2 = return_id_DCTAS__LEAGUE_flag_option(id)
                if flag2 == []:
                    insert_DCTAS_LEAGUE_flag_option(flag_option,rememmberr,id)
                    df = to_append
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = id
                    df['user_id'] = list1
                    to_append.to_sql('DCTAS_BATCH_temp',con=conn,if_exists='append')
                    a = view_all_DCTAS__LEAGUE_flag_record(id)
                    st.success("Processed data you selected: : ")
                    for i in a:
                        st.write(''.join(map(str, i)))
                elif flag2 != []:
                    i = (flag2[0])
                    result = str(''.join(map(str, i)))
                    if flag_option == result:
                        insert_DCTAS_LEAGUE_flag_option(flag_option,rememmberr,id)
                        df = to_append
                        size = NumberOfRows(df)
                        size = len(df)
                        list1 = [0] * size
                        for i in range(0,size):
                            list1[i] = id
                        df['user_id'] = list1
                        to_append.to_sql('DCTAS_BATCH_temp',con=conn,if_exists='append')
                        a = view_all_DCTAS__LEAGUE_flag_record(id)
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
           
            flag_id = return_id_DCTAS_BATCH(temp_save)
            if flag_id == []:
                flag2 = return_id_DCTAS_BATCH_temp(temp_save)
                if flag2 != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql('SELECT * FROM DCTAS_BATCH_temp', conn)
                        df_save = df[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance","user_id"]]
                        st.dataframe(df_save)
                        df_save.to_sql('DCTAS_BATCH_table',con=conn,if_exists='append')
                        delite_DCTAS_BATCH_temp(temp_save)
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
                flag = return_id_DCTAS_BATCH(temp_save)
                if flag != []:
                    if int(temp_save) > 0:
                        df = pd.read_sql_query('SELECT * FROM DCTAS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                        df_new = df[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]]
                        st.markdown(get_table_download_link_csv(df_new), unsafe_allow_html=True)
                        st.success("Export Datas")
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !")

       # Delite datas 
        my_form_delite = st.form(key = "form_Delite")
        submit = my_form_delite.form_submit_button(label = "Delite datas")
        if submit:
            flag = return_id_DCTAS_BATCH(temp_save)                             
            if flag != []:
                if int(temp_save) > 0 :
                    delite_DCTAS_BATCH(temp_save)
                    delite_DCTAS_LEAGUE_flag_option(temp_save)
                    st.success("Delite Datas")
                    st.info("Please procces data")
            else:
                st.warning("file not found")
                st.info("Please procces data again !") 

        try:
            if st.checkbox("Viusalise data !!!"):
                flag = return_id_DCTAS_BATCH(temp_save)
                if flag != []:
    # 
                    if int(temp_save) > 0:
                        flag_option = return_id_DCTAS__LEAGUE_flag_option(temp_save)
                        st.write("i(flag_option[0])",flag_option[0])
                        temp_filter = ''.join(flag_option[0])
                        st.write("temp_filter",temp_filter,"type(temp_filter)",type(temp_filter))

                        if flag_option !=[]:
                            if temp_filter == 'State':
                                df = pd.read_sql_query('SELECT * FROM DCTAS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_save = df[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]]
                                # Graph 1.  Expend
                                st.error("Visualization the State expenses from 2000 to now")
                                st.error("Without inflation rate")
                                brush = alt.selection(type='interval')
                            
                                points = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='Expenditures',
                                    color=alt.condition(brush, 'State', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                )
                            
                                bars = alt.Chart(df_save).mark_bar().encode(
                                    y='State',
                                    color='State',
                                    x='sum(Expenditures)'
                                ).transform_filter(
                                    brush
                                )
                            
                                st.write(points & bars)
                                ###########################################################################
                                # Graph 2. Expend
                                nearest = alt.selection(type='single', nearest=True, on='mouseover',fields=['Expenditures'], empty='none')

                                # The basic line
                                line = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='Expenditures',
                                    color='State'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors = alt.Chart(df_save).mark_point().encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest
                                )

                                # Draw points on the line, and highlight based on selection
                                points = line.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest, 'Expenditures', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                ).transform_filter(
                                    nearest
                                )

                                # Put the five layers into a chart and bind the data
                                aa = alt.layer(
                                    line, selectors, points, rules, text
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(aa)
                                ##############
                                ##############
                                ##############
                                # Graph 3.  Expend inflaction

                                st.error("Visualization the State expenses from 2000 to now")
                                st.error("With inflation rate")
                                brush1 = alt.selection(type='interval')
                            
                                points1 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='inflation_Expenditure',
                                    color=alt.condition(brush1, 'State', alt.value('lightgray'))
                                ).add_selection(
                                    brush1
                                )
                            
                                bars1 = alt.Chart(df_save).mark_bar().encode(
                                    y='State',
                                    color='State',
                                    x='sum(inflation_Expenditure)'
                                ).transform_filter(
                                    brush1
                                )
                            
                                st.write(points1 & bars1)
                                ###########################################################################

                                # Graph 4.  Expend inflaction
                                nearest1 = alt.selection(type='single', nearest=True, on='mouseover',fields=['inflation_Expenditure'], empty='none')

                                # The basic line
                                line1 = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='inflation_Expenditure',
                                    color='State'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors1 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest1
                                )

                                # Draw points on the line, and highlight based on selection
                                points1 = line.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest1, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text1 = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest1, 'inflation_Expenditure', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules1 = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                ).transform_filter(
                                    nearest1
                                )

                                # Put the five layers into a chart and bind the data
                                a1 = alt.layer(
                                    line1, selectors1, points1, rules1, text1
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(a1)
                                ################################    Income / Revenue
                                #   ["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season","Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
                                st.success("Visualization the State Revenue from 2000 to now")
                                st.success("Without inflation rate")
                                brushR = alt.selection(type='interval')
                                # Graph 5.  Income
                            
                                pointsR = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Income',
                                    color=alt.condition(brushR, 'State', alt.value('lightgray'))
                                ).add_selection(
                                    brushR
                                )
                            
                                barsR = alt.Chart(df_save).mark_bar().encode(
                                    y='State',
                                    color='State',
                                    x='sum(Income)'
                                ).transform_filter(
                                    brushR
                                )
                            
                                st.write(pointsR & barsR)
                                ###########################################################################

                                nearestR = alt.selection(type='single', nearest=True, on='mouseover',fields=['Income'], empty='none')
                                
                                # Graph 6.  Income
                                # The basic line
                                lineR = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Income',
                                    color='State'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectorsR = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearestR
                                )

                                # Draw points on the line, and highlight based on selection
                                pointsR = lineR.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearestR, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                textR = lineR.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearestR, 'Income', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rulesR = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                ).transform_filter(
                                    nearestR
                                )

                                # Put the five layers into a chart and bind the data
                                aR = alt.layer(
                                    lineR, selectorsR, pointsR, rulesR, textR
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(aR)
                                ##############
                                ##############
                                ##############
                                # Graph 7.  Income Inflacions 

                                st.success("Visualization the State Revenue from 2000 to now")
                                st.success("With inflation rate")
                                brush11 = alt.selection(type='interval')
                            
                                points11 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Income',
                                    color=alt.condition(brush11, 'State', alt.value('lightgray'))
                                ).add_selection(
                                    brush11
                                )
                            
                                bars11 = alt.Chart(df_save).mark_bar().encode(
                                    y='State',
                                    color='State',
                                    x='sum(inflation_Income)'
                                ).transform_filter(
                                    brush11
                                )
                            
                                st.write(points11 & bars11)
                                ###########################################################################

                                nearest11 = alt.selection(type='single', nearest=True, on='mouseover',fields=['inflation_Income'], empty='none')

                                # Graph 8.  Income Inflacions 
                                # The basic line
                                line11 = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Income',
                                    color='State'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors11 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest1
                                )

                                # Draw points on the line, and highlight based on selection
                                points11 = line11.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest1, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text11 = line11.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest11, 'inflation_Expenditure', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules11 = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                ).transform_filter(
                                    nearest11
                                )

                                # Put the five layers into a chart and bind the data
                                a11 = alt.layer(
                                    line1, selectors1, points1, rules1, text1
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(a11)

                                ################################    Profit
                                #   ["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season","Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
                                st.info("Visualization the State profit from 2000 to now")
                                st.info("Without inflation rate")
                                brushP = alt.selection(type='interval')
                                # Graph 9.  Profit 
                                pointsP = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Balance',
                                    color=alt.condition(brushP, 'State', alt.value('lightgray'))
                                ).add_selection(
                                    brushP
                                )
                            
                                barsP = alt.Chart(df_save).mark_bar().encode(
                                    y='State',
                                    color='State',
                                    x='sum(Balance)'
                                ).transform_filter(
                                    brushP
                                )
                            
                                st.write(pointsP & barsP)
                                ###########################################################################

                                nearestP = alt.selection(type='single', nearest=True, on='mouseover',fields=['Balance'], empty='none')

                                # Graph 10.  Profit 
                                # The basic line
                                lineP = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Balance',
                                    color='State'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectorsP = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearestP
                                )

                                # Draw points on the line, and highlight based on selection
                                pointsP = lineP.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearestP, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                textP = lineP.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearestP, 'Balance', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rulesP = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                ).transform_filter(
                                    nearestP
                                )

                                # Put the five layers into a chart and bind the data
                                aP = alt.layer(
                                    lineP, selectorsP, pointsP, rulesP, textP
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(aP)
                                ##############
                                ##############
                                ############## 

                                st.info("Visualization the State profit from 2000 to now")
                                st.info("With inflation rate")
                                brushPI = alt.selection(type='interval')
                                # Graph 11.  Profit  Inflacion
                                pointsPI = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Balance',
                                    color=alt.condition(brushPI, 'State', alt.value('lightgray'))
                                ).add_selection(
                                    brushPI
                                )
                            
                                barsPI = alt.Chart(df_save).mark_bar().encode(
                                    y='State',
                                    color='State',
                                    x='sum(inflation_Balance)'
                                ).transform_filter(
                                    brushPI
                                )
                            
                                st.write(pointsPI & barsPI)
                                ###########################################################################
                                dff = pd.read_sql_query('SELECT * FROM DCTAS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                dff_save = dff[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]]

                                nearest0 = alt.selection(type='single', nearest=True, on='mouseover',fields=['inflation_Balance'], empty='none')

                                # Graph 12.  Profit  Inflacion
                                # The basic line
                                line0 = alt.Chart(dff_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Balance',
                                    color='State'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors0 = alt.Chart(dff_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest0
                                )

                                # Draw points on the line, and highlight based on selection
                                points0 = line0.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest0, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text0 = line0.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest0, 'inflation_Expenditure', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules0 = alt.Chart(dff_save).mark_rule(color='gray').encode(
                                    x='Departures',
                                ).transform_filter(
                                    nearest0
                                )

                                # Put the five layers into a chart and bind the data
                                a0 = alt.layer(
                                    line0, selectors0, points0, rules0, text0
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(a0)


                                st.success("Viusalise  Datas")
    # 
                            elif temp_filter == 'Competition':
                                temp_option = "Competition"
                                df = pd.read_sql_query('SELECT * FROM DCTAS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                df_save = df[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]]
                                # Graph 1.  Expend
                                st.error("Visualization the Competition expenses from 2000 to now")
                                st.error("Without inflation rate")
                                brush = alt.selection(type='interval')
                            
                                points = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='Expenditures',
                                    color=alt.condition(brush, 'Competition', alt.value('lightgray'))
                                ).add_selection(
                                    brush
                                )
                            
                                bars = alt.Chart(df_save).mark_bar().encode(
                                    y='Competition',
                                    color='Competition',
                                    x='sum(Expenditures)'
                                ).transform_filter(
                                    brush
                                )
                            
                                st.write(points & bars)
                                ###########################################################################
                                # Graph 2. Expend
                                nearest = alt.selection(type='single', nearest=True, on='mouseover',fields=['Expenditures'], empty='none')

                                # The basic line
                                line = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='Expenditures',
                                    color='Competition'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors = alt.Chart(df_save).mark_point().encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest
                                )

                                # Draw points on the line, and highlight based on selection
                                points = line.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest, 'Expenditures', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                ).transform_filter(
                                    nearest
                                )

                                # Put the five layers into a chart and bind the data
                                aa = alt.layer(
                                    line, selectors, points, rules, text
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(aa)
                                ##############
                                ##############
                                ##############
                                # Graph 3.  Expend inflaction

                                st.error("Visualization the Competition expenses from 2000 to now")
                                st.error("With inflation rate")
                                brush1 = alt.selection(type='interval')
                            
                                points1 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='inflation_Expenditure',
                                    color=alt.condition(brush1, 'Competition', alt.value('lightgray'))
                                ).add_selection(
                                    brush1
                                )
                            
                                bars1 = alt.Chart(df_save).mark_bar().encode(
                                    y='Competition',
                                    color='Competition',
                                    x='sum(inflation_Expenditure)'
                                ).transform_filter(
                                    brush1
                                )
                            
                                st.write(points1 & bars1)
                                ###########################################################################

                                # Graph 4.  Expend inflaction
                                nearest1 = alt.selection(type='single', nearest=True, on='mouseover',fields=['inflation_Expenditure'], empty='none')

                                # The basic line
                                line1 = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    y='inflation_Expenditure',
                                    color='Competition'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors1 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest1
                                )

                                # Draw points on the line, and highlight based on selection
                                points1 = line.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest1, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text1 = line.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest1, 'inflation_Expenditure', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules1 = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Arrivals',
                                    x=alt.X('Arrivals', axis=alt.Axis(title='the number of players who come to the league')),
                                ).transform_filter(
                                    nearest1
                                )

                                # Put the five layers into a chart and bind the data
                                a1 = alt.layer(
                                    line1, selectors1, points1, rules1, text1
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(a1)
                                ################################    Income / Revenue
                                #   ["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season","Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
                                st.success("Visualization the Competition Revenue from 2000 to now")
                                st.success("Without inflation rate")
                                brushR = alt.selection(type='interval')
                                # Graph 5.  Income
                            
                                pointsR = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Income',
                                    color=alt.condition(brushR, 'Competition', alt.value('lightgray'))
                                ).add_selection(
                                    brushR
                                )
                            
                                barsR = alt.Chart(df_save).mark_bar().encode(
                                    y='Competition',
                                    color='Competition',
                                    x='sum(Income)'
                                ).transform_filter(
                                    brushR
                                )
                            
                                st.write(pointsR & barsR)
                                ###########################################################################

                                nearestR = alt.selection(type='single', nearest=True, on='mouseover',fields=['Income'], empty='none')
                                
                                # Graph 6.  Income
                                # The basic line
                                lineR = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Income',
                                    color='Competition'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectorsR = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearestR
                                )

                                # Draw points on the line, and highlight based on selection
                                pointsR = lineR.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearestR, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                textR = lineR.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearestR, 'Income', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rulesR = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                ).transform_filter(
                                    nearestR
                                )

                                # Put the five layers into a chart and bind the data
                                aR = alt.layer(
                                    lineR, selectorsR, pointsR, rulesR, textR
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(aR)
                                ##############
                                ##############
                                ##############
                                # Graph 7.  Income Inflacions 

                                st.success("Visualization the Competition Revenue from 2000 to now")
                                st.success("With inflation rate")
                                brush11 = alt.selection(type='interval')
                            
                                points11 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Income',
                                    color=alt.condition(brush11, 'Competition', alt.value('lightgray'))
                                ).add_selection(
                                    brush11
                                )
                            
                                bars11 = alt.Chart(df_save).mark_bar().encode(
                                    y='Competition',
                                    color='Competition',
                                    x='sum(inflation_Income)'
                                ).transform_filter(
                                    brush11
                                )
                            
                                st.write(points11 & bars11)
                                ###########################################################################

                                nearest11 = alt.selection(type='single', nearest=True, on='mouseover',fields=['inflation_Income'], empty='none')

                                # Graph 8.  Income Inflacions 
                                # The basic line
                                line11 = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Income',
                                    color='Competition'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors11 = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest1
                                )

                                # Draw points on the line, and highlight based on selection
                                points11 = line11.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest1, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text11 = line11.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest11, 'inflation_Expenditure', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules11 = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                ).transform_filter(
                                    nearest11
                                )

                                # Put the five layers into a chart and bind the data
                                a11 = alt.layer(
                                    line1, selectors1, points1, rules1, text1
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(a11)

                                ################################    Profit
                                #   ["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season","Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
                                st.info("Visualization the Competition profit from 2000 to now")
                                st.info("Without inflation rate")
                                brushP = alt.selection(type='interval')
                                # Graph 9.  Profit 
                                pointsP = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Balance',
                                    color=alt.condition(brushP, 'Competition', alt.value('lightgray'))
                                ).add_selection(
                                    brushP
                                )
                            
                                barsP = alt.Chart(df_save).mark_bar().encode(
                                    y='Competition',
                                    color='Competition',
                                    x='sum(Balance)'
                                ).transform_filter(
                                    brushP
                                )
                            
                                st.write(pointsP & barsP)
                                ###########################################################################

                                nearestP = alt.selection(type='single', nearest=True, on='mouseover',fields=['Balance'], empty='none')

                                # Graph 10.  Profit 
                                # The basic line
                                lineP = alt.Chart(df_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='Balance',
                                    color='Competition'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectorsP = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearestP
                                )

                                # Draw points on the line, and highlight based on selection
                                pointsP = lineP.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearestP, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                textP = lineP.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearestP, 'Balance', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rulesP = alt.Chart(df_save).mark_rule(color='gray').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                ).transform_filter(
                                    nearestP
                                )

                                # Put the five layers into a chart and bind the data
                                aP = alt.layer(
                                    lineP, selectorsP, pointsP, rulesP, textP
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(aP)
                                ##############
                                ##############
                                ############## 

                                st.info("Visualization the Competition profit from 2000 to now")
                                st.info("With inflation rate")
                                brushPI = alt.selection(type='interval')
                                # Graph 11.  Profit  Inflacion
                                pointsPI = alt.Chart(df_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Balance',
                                    color=alt.condition(brushPI, 'Competition', alt.value('lightgray'))
                                ).add_selection(
                                    brushPI
                                )
                            
                                barsPI = alt.Chart(df_save).mark_bar().encode(
                                    y='Competition',
                                    color='Competition',
                                    x='sum(inflation_Balance)'
                                ).transform_filter(
                                    brushPI
                                )
                            
                                st.write(pointsPI & barsPI)
                                ###########################################################################
                                dff = pd.read_sql_query('SELECT * FROM DCTAS_BATCH_table WHERE user_id = "{}"'.format(temp_save),conn)
                                dff_save = dff[["Order_of_Expend","Club","State","Competition","Expenditures","Income","Arrivals","Departures","Balance","inflation_Expenditure","inflation_Income","inflation_Balance"]]

                                nearest0 = alt.selection(type='single', nearest=True, on='mouseover',fields=['inflation_Balance'], empty='none')

                                # Graph 12.  Profit  Inflacion
                                # The basic line
                                line0 = alt.Chart(dff_save).mark_line(interpolate='basis').encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    y='inflation_Balance',
                                    color='Competition'
                                )

                                # Transparent selectors across the chart. This is what tells us
                                # the x-value of the cursor
                                selectors0 = alt.Chart(dff_save).mark_point(size=200,filled=True).encode(
                                    #x='Departures',
                                    x=alt.X('Departures', axis=alt.Axis(title='the number of players who left the league')),
                                    opacity=alt.value(0),
                                ).add_selection(
                                    nearest0
                                )

                                # Draw points on the line, and highlight based on selection
                                points0 = line0.mark_point(size=200,filled=True).encode(
                                    opacity=alt.condition(nearest0, alt.value(1), alt.value(0))
                                )

                                # Draw text labels near the points, and highlight based on selection
                                text0 = line0.mark_text(align='left', dx=5, dy=-5).encode(
                                    text=alt.condition(nearest0, 'inflation_Expenditure', alt.value(' '))
                                )

                                # Draw a rule at the location of the selection
                                rules0 = alt.Chart(dff_save).mark_rule(color='gray').encode(
                                    x='Departures',
                                ).transform_filter(
                                    nearest0
                                )

                                # Put the five layers into a chart and bind the data
                                a0 = alt.layer(
                                    line0, selectors0, points0, rules0, text0
                                ).properties(
                                    width=600, height=300
                                )
                                st.write(a0)



                                st.success("Viusalise  Datas")
    
                
                else:
                    st.warning("file not found")
                    st.info("Please procces data again !!")
        except Exception as e:
            st.write(e)
            st.write("Error, please resart Visaulsation checkboc !! ") 

