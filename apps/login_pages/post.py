import streamlit as st
import os
import pandas as pd
import io
from io import BytesIO
import glob
import numpy as np
import sqlite3
#import cv2
#from opencv-python import cv2
from database import *
from PIL import Image
from subprocess import Popen, PIPE
import numpy as np 
from streamlit import caching
from datetime import datetime
from functions import *
from html_temp import*
import marshal
def app():
    st.write("post")
    create_post_table_temp_MAIN()
    
    conn = sqlite3.connect('data_new.db', check_same_thread=False)
    test_user_exisiting = return_post_id_temp_MAIN()
    if test_user_exisiting == []:
        username = return_username()
        i = (username[0])
        res = str(''.join(map(str, i)))
        return_user_idd = return_user_id(res)
        i = (return_user_idd[0])
        temp_save = int(''.join(map(str, i)))
        #.write("delamo sutra ujtro !!!")
            # if blog_option == "Create new post":
        st.title('Create New Post')
        if st.checkbox("Add title "):
            blog_title = st.text_input("Enther Post title: ")
            if blog_title  == "":
                st.warning("Please first Insert Blog Title !!")
            elif blog_title != "":
                if st.checkbox("add articles and images"):
                    blog_option = st.selectbox("Chose a option ",["Add article","Add Image"], key='dsa' )
                    if blog_option == "Add article":
                        blog_articles = st.text_area("Post Articles here",height=250,key='dasdsa')
                        if blog_articles is not None:
                            if st.button("Add"):
                                conn = sqlite3.connect('data_new.db', check_same_thread=False)
                                # df_post_id = pd.read_sql_query('SELECT id_post FROM blog_table_temp_MAIN',conn)
                                # temp_post_id = df_post_id['id_post'].unique()    
                                # if df_post_id.empty == True:
                                #     post__id = str(1)
                                # else :
                                #     post_lista =[]
                                #     for i in temp_post_id:
                                #         post_lista.append(i)    
                                #     temp2 = max(post_lista)
                                #     te = int(temp2) 
                                #     temp = te +1
                                #     post__id = str(temp)
                                df = pd.DataFrame()
                                #create_image_table()
                                #   (blog_table_id,id_post,user_id,width,height)
                                #data = marshal.dumps(a)
                                #add_data_to_image_to_table('1',temp_save,None,None)
                                df.insert(0,'id_post',['1'])
                                df.insert(0,'author',[res])
                                df.insert(0,'user_id',[temp_save])
                                df.insert(0,'title',[blog_title])
                                df.insert(0,'article',[blog_articles])
                                df.insert(0,'read_time',[readingTime(blog_articles)])
                                conn = sqlite3.connect('data_new.db', check_same_thread=False)
                                create_post_table()
                                df.to_sql('blog_table',con=conn,if_exists='append')
                                c = conn.cursor()
                                st.success("Articles added")
                                caching.clear_cache()
                    elif blog_option == "Add Image":
                        image_file = st.file_uploader("Upload a image ",type=['png','jpeg','jpg'],key='dsadsa1')
                        if image_file is not None:
                            
                            if st.button("Add"):
                                conn = sqlite3.connect('data_new.db', check_same_thread=False)
                                df_post_id = pd.read_sql_query('SELECT id_post FROM blog_table_temp_MAIN',conn)
                                temp_post_id = df_post_id['id_post'].unique()    
                                if df_post_id.empty == True:
                                    post__id = str(1)
                                else :
                                    post_lista =[]
                                    for i in temp_post_id:
                                        post_lista.append(i)    
                                    temp2 = max(post_lista)
                                    te = int(temp2) 
                                    temp = te +1
                                    post__id = str(temp)
                                
                                
                                df = pd.DataFrame()
                                width,height,a = convert_img_to_byte(image_file)
                                w = marshal.dumps(width)
                                h = marshal.dumps(height)
                                #create_image_table()
                                #   (blog_table_id,id_post,user_id,width,height)
                                nova_lista = a.tolist()
                                data = marshal.dumps(nova_lista)
                                # add_data_to_image_to_table('1',temp_save,width,height)
                                df.insert(0,'id_post',['1'])
                                df.insert(0,'author',[res])
                                df.insert(0,'user_id',[temp_save])
                                df.insert(0,'title',[blog_title])
                                df.insert(0,'article',[None])
                                df.insert(0,'read_time',[None])
                                df.insert(0,'img',[data])
                                df.insert(0,'h',[int(height)])
                                df.insert(0,'w',[int(width)])
                            
                                create_post_table()
                                df.to_sql('blog_table',con=conn,if_exists='append')
                                c = conn.cursor()
                                st.success("Image added")
                                caching.clear_cache()
        if st.button("Save post"):
            conn = sqlite3.connect('data_new.db', check_same_thread=False)
            username = return_username()
            i = (username[0])
            res = str(''.join(map(str, i)))
            return_user_idd = return_user_id(res)
            i = (return_user_idd[0])
            temp_save = int(''.join(map(str, i)))
            create_post_table()      
            df = pd.read_sql_query('SELECT * FROM blog_table WHERE user_id = "{}"'.format(temp_save),conn)
            df_new = df[['id_post','author','user_id','title','article','img','postdate','read_time','h','w']]
            #df_new = df[['id_post','author','user_id','title','article','img','postdate','read_time']]
            # post__id = df_new['id_post'].unique() 
            # st.write(post__id)
            # st.write("psot id ",post__id[0])
            # print(post__id)
            blog_post_date = st.date_input("Date",key='dsadsa2')
            size = len(df_new)
            list1 = [0] * size
            for i in range(0,size):
                list1[i] = str(blog_post_date)
            df_new['postdate'] = list1
            delite_post(temp_save)

            #st.dataframe(df_new)
            df_new.to_sql('blog_table_temp_MAIN',con=conn,if_exists='append')
            

            # a = return_post_id_for_image(post__id[0],temp_save)
            # lsita_post_id = []
            # for i in a:
            #     temp = (str(''.join(map(str, i))))  
            #     lsita_post_id.append(int(temp))
            
            # #st.write(lsita_post_id)

            # df = pd.read_sql_query('SELECT * FROM table_Image',conn)
            # df = df[['Image_id','blog_table_id','id_post','user_id','width','height']]
            # check_for_nan = df['height'].isnull()
            # arraa = check_for_nan.tolist()

            # counter = 0
            # temp = 0
            # for i in arraa:
            #     if i == False:   
            #         df.loc[counter,'blog_table_id']=lsita_post_id[temp]
            #         temp +=1
            #     counter +=1
            
            # df.to_sql('IMAGE_FINAL',con=conn,if_exists='append')


            c = conn.cursor()
            caching.clear_cache()
            st.success("Post saved!")   

    else:
        username = return_username()
        i = (username[0])
        res = str(''.join(map(str, i)))
        return_user_idd = return_user_id(res)
        i = (return_user_idd[0])
        temp_save = int(''.join(map(str, i)))
        create_post_table_temp_MAIN()

        #######################################################


        #dfsve = pd.read_sql_query('SELECT * FROM blog_table_temp_MAIN',conn)
        # st.write("dataframe ")
        # st.dataframe(dfsve)
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

        #######################################################
        st.info("Select option")
        blog_option = st.selectbox("Chose a option ",["Create new post","Search post by Author","Search post by Title","Delite post by Title"], key='post_options' )
        if blog_option == "Create new post":
            st.title('Create New Post')
            if st.checkbox("Add title "):
                blog_title = st.text_input("Enther Post title: ")
                if blog_title  == "":
                    st.warning("Please first Insert Blog Title !!")
                elif blog_title != "":
                    if st.checkbox("add articles and images"):
                        blog_option = st.selectbox("Chose a option ",["Add article","Add Image"], key='dsa' )
                        if blog_option == "Add article":
                            blog_articles = st.text_area("Post Articles here",height=250,key='dasdsa')
                            if blog_articles is not None:
                                if st.button("Add"):
                                    conn = sqlite3.connect('data_new.db', check_same_thread=False)
                                    df_post_id = pd.read_sql_query('SELECT id_post FROM blog_table_temp_MAIN',conn)
                                    temp_post_id = df_post_id['id_post'].unique()    
                                    if df_post_id.empty == True:
                                        post__id = str(1)
                                    else :
                                        post_lista =[]
                                        for i in temp_post_id:
                                            post_lista.append(i)    
                                        temp2 = max(post_lista)
                                        te = int(temp2) 
                                        temp = te +1
                                        post__id = str(temp)
                                    df = pd.DataFrame()
                                    #create_image_table()
                                    #   (blog_table_id,id_post,user_id,width,height)
                                    #data = marshal.dumps(a)
                                    # add_data_to_image_to_table(post__id,temp_save,None,None)
                                    df.insert(0,'id_post',[post__id])
                                    df.insert(0,'author',[res])
                                    df.insert(0,'user_id',[temp_save])
                                    df.insert(0,'title',[blog_title])
                                    df.insert(0,'article',[blog_articles])
                                    df.insert(0,'img',[None])
                                    df.insert(0,'read_time',[readingTime(blog_articles)])
                                    conn = sqlite3.connect('data_new.db', check_same_thread=False)
                                    create_post_table()
                                    df.to_sql('blog_table',con=conn,if_exists='append')
                                    c = conn.cursor()
                                    st.success("Articles added")
                                    caching.clear_cache()

                        elif blog_option == "Add Image":
                            image_file = st.file_uploader("Upload a image ",type=['png','jpeg','jpg'],key='dsadsa1')
                            if image_file is not None:
                                file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
                                bytes = file_bytes.tobytes()
                                if st.button("Add"):
                                    conn = sqlite3.connect('data_new.db', check_same_thread=False)
                                    df_post_id = pd.read_sql_query('SELECT id_post FROM blog_table_temp_MAIN',conn)
                                    temp_post_id = df_post_id['id_post'].unique()    
                                    if df_post_id.empty == True:
                                        post__id = str(1)
                                    else :
                                        post_lista =[]
                                        for i in temp_post_id:
                                            post_lista.append(i)    
                                        temp2 = max(post_lista)
                                        te = int(temp2) 
                                        temp = te +1
                                        post__id = str(temp)
                                    df = pd.DataFrame()
                                    width,height,a = convert_img_to_byte(image_file)
                                    # w = marshal.dumps(width)
                                    # h = marshal.dumps(height)
                                    #create_image_table()
                                    #   (blog_table_id,id_post,user_id,width,height)
                                    nova_lista = a.tolist()
                                    data = marshal.dumps(nova_lista)
                                    #data = marshal.dumps(a)
                                    # add_data_to_image_to_table(post__id,temp_save,width,height)
                                    df.insert(0,'id_post',[post__id])
                                    df.insert(0,'author',[res])
                                    df.insert(0,'user_id',[temp_save])
                                    df.insert(0,'title',[blog_title])
                                    df.insert(0,'article',[None])
                                    df.insert(0,'img',[data])
                                    df.insert(0,'w',[int(width)])
                                    df.insert(0,'h',[int(height)])
                                    create_post_table()
                                    df.to_sql('blog_table',con=conn,if_exists='append')
                                    c = conn.cursor()
                                    st.success("Image added")
                                    caching.clear_cache()
            if st.button("Save post"):
                conn = sqlite3.connect('data_new.db', check_same_thread=False)
                username = return_username()
                i = (username[0])
                res = str(''.join(map(str, i)))
                return_user_idd = return_user_id(res)
                i = (return_user_idd[0])
                temp_save = int(''.join(map(str, i)))
                
                create_post_table()      
                df = pd.read_sql_query('SELECT * FROM blog_table WHERE user_id = "{}"'.format(temp_save),conn)
                df_new = df[['id_post','author','user_id','title','article','img','postdate','read_time','h','w']]
                #post__id = df_new['id_post'].unique() 
                blog_post_date = st.date_input("Date",key='dsadsa2')
                size = len(df_new)
                list1 = [0] * size
                for i in range(0,size):
                    list1[i] = str(blog_post_date)
                df_new['postdate'] = list1
                #st.dataframe(df_new)
                df_new.to_sql('blog_table_temp_MAIN',con=conn,if_exists='append')
                delite_post(temp_save)

                # a = return_post_id_for_image(post__id[0],temp_save)
                # lsita_post_id = []
                # for i in a:
                #     temp = (str(''.join(map(str, i))))  
                #     lsita_post_id.append(int(temp))
                # #st.write(lsita_post_id)

                # df = pd.read_sql_query('SELECT * FROM table_Image',conn)
                # df = df[['Image_id','blog_table_id','id_post','user_id','width','height']]
                # check_for_nan = df['height'].isnull()
                # arraa = check_for_nan.tolist()

                # counter = 0
                # temp = 0
                # for i in arraa:
                #     if i == False:   
                #         df.loc[counter,'blog_table_id']=lsita_post_id[temp]
                #         temp +=1
                #     counter +=1

                # df.to_sql('IMAGE_FINAL',con=conn,if_exists='append')


                c = conn.cursor()
                caching.clear_cache()
                st.success("Post saved!")

        elif blog_option == "Search post by Title":
            st.success("Search posts by the Title name")
            df_title = pd.read_sql_query('SELECT title FROM blog_table_temp_MAIN',conn)
            temp_title = df_title['title'].unique() 

            title_lista =[]
            for i in temp_title:
                title_lista.append(i)
            st.write(title_lista)

            # st.write("Ispis naslova :: ")
            # for i in title_lista:
            #     st.write(i)
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
                #st.write("autor_temp",autor_temp)
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
                                    #type(df_print['img'][i]) != str and

                                    data = df_print['img'][i]
                                    h = int(df_print['h'][i])
                                    w = int(df_print['w'][i])
                                    nova_lista = marshal.loads(data)  
                                    arr = np.array(nova_lista)                            
                                    oimg = convert_bytes_to_img(w,h,arr)
                                    st.image(oimg)
                                    # test = np.frombuffer(df_print['img'][i], dtype=np.uint8)
                                    # opencv_image = cv2.imdecode(test, 1)
                                    #st.image(opencv_image, channels="BGR")
                                elif type(df_print['article'][i]) == str and df_print['article'][i] != None:
                                    st.markdown(full_message_temp.format(df_print['article'][i]),unsafe_allow_html=True)
                            st.success("end of post")

        elif blog_option =="Delite post by Title":
            st.success("Delit post")
            df_autor = pd.read_sql_query('SELECT title FROM blog_table_temp_MAIN WHERE user_id = "{}"'.format(temp_save),conn)
            temp_autor = df_autor['title'].unique() 
            if len(df_autor) > 0 and df_autor['title'][0] != None:
                title_autor =[]
                for i in temp_autor:
                    title_autor.append(i)


                autor_temp = st.selectbox("Select title post", options= list(title_autor))
                if st.button("Delite"):
                    delite_post_by_title(autor_temp) 
                    st.warning("Post successfully deleted!!!")
            else:
                st.warning("Please first create the post !!")






















    