import streamlit as st
import pandas as pd
import numpy as np
from functions import *
from League_functions.DCWS_func import DCWS_base
from database import *
import altair as alt
from html_temp import *
import os
import time

def app():
    create_DCWS()
    st.title('1. function DCWS  process function')
    st.write('Welcome to metrics')
    username = return_username()

    i = (username[0])
    res = str(''.join(map(str, i)))

    delite_temp_user(res)
    create_DCWS()
    col1,col2 = st.columns(2)
    with col1:
                            
        st.info(" For restart data you must delete data and start over !!!")
        # Processd data
        if st.checkbox("Process data"):
            df = pd.read_sql('SELECT * FROM League_datas', conn)
            df_new = df[["0","Nationality","Competition","Expenditures","Arrivals","Income","Departures","Balance","Year"]]
            st.dataframe(df_new)
            a_leuge_DF = DCWS_base(df_new)
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
                flag = return_id_DCWS_table(te)
                if flag == []:
                    df = a_leuge_DF
                    size = NumberOfRows(df)
                    size = len(df)
                    list1 = [0] * size
                    for i in range(0,size):
                        list1[i] = te
                    df['user_id'] = list1
                    create_DCWS()
                    df.to_sql('DCWS_table',con=conn,if_exists='append')
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
                flag = return_id_DCWS_table(te)
                if flag != []:
                    if int(te) > 0:
                        df = pd.read_sql_query('SELECT * FROM DCWS_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Year_of_Season","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
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
            flag = (return_id_DCWS_table(te))                               
            if flag != []:
                if int(te) > 0 :
                    delite_DCWS(te)
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
                flag = return_id_DCWS_table(te)
                if flag != []:
                    if int(te) > 0:
                        df = pd.read_sql_query('SELECT * FROM DCWS_table WHERE user_id = "{}"'.format(te),conn)
                        df_new = df[["Year_of_Season","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]]
                        df_new['Year_of_Season']= pd.to_datetime(df_new['Year_of_Season'],format='%Y')
                        st.subheader("Expend ")
                        st.error("Expend by leagues with the inflation coefficient throw number of players come to the leauges")
                        c = alt.Chart(df_new).mark_circle().encode(
                        alt.X('Year_of_Season', scale=alt.Scale(zero=True)),
                        alt.Y('Expend', scale=alt.Scale(zero=True, padding=5)),
                        # alt.Color('sum_of_Arrivlas', scale=alt.Scale(scheme='category20b')),
                        # opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
                        size='sum_of_Arrivlas'
                        ).properties(
                            width = 600,
                            height = 600
                        ).interactive()
                        st.write(c)

                        st.error("Expend by leagues with the inflation coefficient throw number of players come to the leauges")
                        base = alt.Chart(df_new).mark_area(
                            color='goldenrod',
                            opacity=0.3
                        ).encode(
                            x='Year_of_Season',
                            y='Expend',
                        ).properties(
                            width = 600,
                            height = 400
                        )
                    
                        brush = alt.selection_interval(encodings=['x'],empty='all')
                        background = base.add_selection(brush)
                        selected = base.transform_filter(brush).mark_area(color='goldenrod')
                        st.write(background + selected)


                        st.error("Expend by leagues with the inflation coefficient throw number of players come to the leauges")
                        base = alt.Chart(df_new).encode(
                            alt.X('Year_of_Season', axis=alt.Axis(title=None))
                        )

                        area = base.mark_line(strokeWidth=5, color='#57A44C').encode(
                            alt.Y('Expend',
                                  axis=alt.Axis(title='profit', titleColor='#57A44C')),
                            #alt.Y2('Income')
                        )

                        line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
                            alt.Y('sum_of_Arrivlas',
                                  axis=alt.Axis(title='number of players arrivals', titleColor='#5276A7'))
                        )

                        b = alt.layer(area, line).resolve_scale(
                            y = 'independent'
                        ).properties(
                            width=700,
                            height=400
                        ).interactive()   
                        st.write(b)

                        st.subheader("Revenues")

                        st.success("Revenues by leagues with inflation rates throw the number of players who leave the leagues")
                        b = alt.Chart(df_new).mark_circle().encode(
                        alt.X('Year_of_Season', scale=alt.Scale(zero=True)),
                        alt.Y('Income', scale=alt.Scale(zero=True, padding=5)),
                        # alt.Color('sum_of_Arrivlas', scale=alt.Scale(scheme='category20b')),
                        # opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
                        size='sum_of_Arrivlas'
                        ).properties(
                            width = 600,
                            height = 600
                        ).interactive()
                        st.write(b)

                        st.success("Revenues by leagues with inflation rates throw the number of players who leave the leagues")
                        base1 = alt.Chart(df_new).mark_area(
                            color='goldenrod',
                            opacity=0.3
                        ).encode(
                            x='Year_of_Season',
                            y='Income',
                        ).properties(
                            width = 600,
                            height = 400
                        )
                    
                        brush1 = alt.selection_interval(encodings=['x'],empty='all')
                        background1 = base1.add_selection(brush1)
                        selected1 = base1.transform_filter(brush1).mark_area(color='goldenrod')
                        st.write(background1 + selected1)


                        st.success("Revenues by leagues with the inflation coefficient throw number of players come to the leauges")
                        base = alt.Chart(df_new).encode(
                            alt.X('Year_of_Season', axis=alt.Axis(title=None))
                        )

                        area = base.mark_line(strokeWidth=5, color='#57A44C').encode(
                            alt.Y('Income',
                                  axis=alt.Axis(title='profit', titleColor='#57A44C')),
                            #alt.Y2('Income')
                        )

                        line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
                            alt.Y('sum_of_Arrivlas',
                                  axis=alt.Axis(title='number of players arrivals', titleColor='#5276A7'))
                        )

                        c = alt.layer(area, line).resolve_scale(
                            y = 'independent'
                        ).properties(
                            width=700,
                            height=400
                        ).interactive()   
                        st.write(c)

                        st.subheader("Profit")
                        st.warning("Profit by leagues with inflation rates throw the number of players who come in the leagues")
                        a = alt.Chart(df_new).mark_circle().encode(
                        alt.X('Year_of_Season', scale=alt.Scale(zero=True)),
                        alt.Y('Balance', scale=alt.Scale(zero=True, padding=5)),
                        # alt.Color('sum_of_Arrivlas', scale=alt.Scale(scheme='category20b')),
                        # opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
                        size='sum_of_Arrivlas'
                        ).properties(
                            width = 600,
                            height = 600
                        ).interactive()
                        st.write(a)  

                        st.warning("Profit by leagues with inflation rates throw the number of players who come in the leagues")
                        base2 = alt.Chart(df_new).mark_area(
                            color='goldenrod',
                            opacity=0.3
                        ).encode(
                            x='Year_of_Season',
                            y='Balance',
                        ).properties(
                            width = 600,
                            height = 400
                        )
                    
                        brush2 = alt.selection_interval(encodings=['x'],empty='all')
                        background2 = base2.add_selection(brush2)
                        selected2 = base2.transform_filter(brush2).mark_area(color='goldenrod')
                        st.write(background2+ selected2) 

                        st.warning("Profit by leagues with the inflation coefficient throw number of players come to the leauges")
                        base = alt.Chart(df_new).encode(
                            alt.X('Year_of_Season', axis=alt.Axis(title=None))
                        )

                        area = base.mark_line(strokeWidth=5, color='#57A44C').encode(
                            alt.Y('Balance',
                                  axis=alt.Axis(title='profit', titleColor='#57A44C')),
                            #alt.Y2('Income')
                        )

                        line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
                            alt.Y('sum_of_Arrivlas',
                                  axis=alt.Axis(title='number of players arrivals', titleColor='#5276A7'))
                        )

                        a = alt.layer(area, line).resolve_scale(
                            y = 'independent'
                        ).properties(
                            width=700,
                            height=400
                        ).interactive()   
                        st.write(a)                     

                        st.success("Viusalise  Datas")
                else:

                    st.warning("file not found")
                    st.info("Please procces data again !!")

        except Exception as e:     
           st.write("Error, please resart Visaulsation checkboc !! ") 