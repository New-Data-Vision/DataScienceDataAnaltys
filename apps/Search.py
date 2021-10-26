import streamlit as st
from html_temp import *
from functions import *
from database import *
from streamlit import caching
from datetime import datetime
from PIL import Image
import pandas as pd
import numpy as np
import marshal



def app():


    st.header("Search")
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














    # sc = st.selectbox("chose",["Title","Author"])
    # df_user = pd.read_sql_query('SELECT DISTINCT user_id FROM blog_table_temp_MAIN ',conn)
    # temp_user = df_user['user_id'].unique() 
    # df_post = pd.read_sql_query('SELECT DISTINCT id_post FROM blog_table_temp_MAIN',conn)
    # temp_post = df_post['id_post'].unique() 


    # post_lista =[]
    # for i in temp_post:
    #     post_lista.append(i)


    # user_lista =[]
    # for i in temp_user:
    #     user_lista.append(i)
    # d = {}
    # for i in user_lista:
    #     for j in post_lista:
    #         df = pd.read_sql_query('SELECT author,read_time FROM blog_table_temp_MAIN WHERE id_post = "{}"'.format(int(j)),conn)
    #         Total = df['read_time'].sum()
    #         add_if_key_not_exist(d,j,Total)

    # if sc == "Author":
    #     df_autor = pd.read_sql_query('SELECT author FROM blog_table_temp_MAIN',conn)
    #     temp_autor = df_autor['author'].unique() 
    #     title_autor =[]
    #     for i in temp_autor:
    #         title_autor.append(i)
    #     autor_temp = st.selectbox("Select author name", options= list(title_autor))
    #     ###############

    #     df_autor = pd.read_sql_query('SELECT user_id FROM blog_table_temp_MAIN WHERE author = "{}"'.format(str(autor_temp)),conn)
    #     authorr = int(df_autor['user_id'][0])
    #     lista_au =[]
    #     lista_au.append(authorr)

    #     ###############
    #     if st.button("Submit author"):
    #         df_title_temp = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN ',conn)
    #         temp_user = df_title_temp['user_id'].unique() 
    #         user_lista =[]
    #         for i in temp_user:
    #             user_lista.append(i)
    #         df = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN',conn)
    #         df_new = df[['id_post','author','user_id','title','article','img','postdate']]
    #         a = df_new['id_post'].unique() 
    #         lista =[]
    #         for i in a:
    #             lista.append(i)
    #         for j in lista_au:
    #             df = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE user_id = "{}"'.format(int(j)),conn)
    #             for i in lista:
    #                 df_print = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
    #                 df_a_d_t = pd.read_sql_query('SELECT DISTINCT title,author,postdate FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
    #                 if df_a_d_t.empty != True :
    #                     temp_reading_time = d.get(i)
    #                     st.markdown(head_message_temp.format(df_a_d_t['title'][0],df_a_d_t['author'][0],df_a_d_t['postdate'][0],temp_reading_time),unsafe_allow_html=True)
    #                     for i in range(0,len(df_print)):
    #                         if type(df_print['img'][i]) != str and df_print['img'][i] != None:
    #                             test = np.frombuffer(df_print['img'][i], dtype=np.uint8)
    #                             opencv_image = cv2.imdecode(test, 1)
    #                             st.image(opencv_image, channels="BGR")
    #                         elif type(df_print['article'][i]) == str and df_print['article'][i] != None:
    #                             st.markdown(full_message_temp.format(df_print['article'][i]),unsafe_allow_html=True)
    #     st.success("Search posts by the Author name")

    # elif sc == "Title":
    #     df_autor = pd.read_sql_query('SELECT title FROM blog_table_temp_MAIN',conn)
    #     temp_autor = df_autor['title'].unique() 
    #     title_autor =[]
    #     for i in temp_autor:
    #         title_autor.append(i)
    #     title_autor = st.selectbox("Select title post", options= list(title_autor))

    #     ###############

    #     df_title = pd.read_sql_query('SELECT user_id FROM blog_table_temp_MAIN WHERE title = "{}"'.format(str(title_autor)),conn)
    #     titlee = int(df_title['user_id'][0])
    #     lista_title =[]
    #     lista_title.append(titlee)

    #     ###############
    #     if st.button("Submit title"):
    #         df_title_temp = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE title = "{}"'.format(str(title_autor)),conn)
    #         temp_user = df_title_temp['user_id'].unique() 
    #         user_lista =[]
    #         for i in temp_user:
    #             user_lista.append(i)
    #         df = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE title = "{}"'.format(str(title_autor)),conn)
    #         df_new = df[['id_post','author','user_id','title','article','img','postdate']]
    #         a = df_new['id_post'].unique() 
    #         lista =[]
    #         for i in a:
    #             lista.append(i)
    #         for j in lista_title:
    #             df = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE user_id = "{}"'.format(int(j)),conn)
    #             for i in lista:
    #                 df_print = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
    #                 df_a_d_t = pd.read_sql_query('SELECT DISTINCT title,author,postdate FROM blog_table_temp_MAIN WHERE user_id = "{}" AND id_post = "{}"'.format(int(j),int(i)),conn)
    #                 if df_a_d_t.empty != True :
    #                     temp_reading_time = d.get(i)
    #                     st.markdown(head_message_temp.format(df_a_d_t['title'][0],df_a_d_t['author'][0],df_a_d_t['postdate'][0],temp_reading_time),unsafe_allow_html=True)
    #                     for i in range(0,len(df_print)):
    #                         if type(df_print['img'][i]) != str and df_print['img'][i] != None:
    #                             test = np.frombuffer(df_print['img'][i], dtype=np.uint8)
    #                             opencv_image = cv2.imdecode(test, 1)
    #                             st.image(opencv_image, channels="BGR")
    #                         elif type(df_print['article'][i]) == str and df_print['article'][i] != None:
    #                             st.markdown(full_message_temp.format(df_print['article'][i]),unsafe_allow_html=True)
    #     st.success("Search posts by the Author name")

		