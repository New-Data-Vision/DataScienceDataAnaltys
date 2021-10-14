import streamlit as st 
import pandas as pd
import numpy as np
from sqlite3.dbapi2 import paramstyle
#import bcrypt
from functions import check_email,make_password,check_hashes,GETCoefficients,remove_duplicates
from database import create_usertable,add_user_data,check_double_email,check_double_username,login_user,check_userdatatable
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
#from League_functions.avg_Income_for_player_Departures import  BATCH_for_GetAVGExpendFORplayerArrivals
from functions import DataFrameFunc,NumberOfRows
from League_functions.EFPA_func import*
#coef = 'file.txt'

def app():
    create_usertable()
    st.subheader("SingUp")
    # Username
    form = st.sidebar.form(key='my_form')
    new_user = form.text_input(label='Username')
    # Password
    n_password = form.text_input(label='Password',type="password")        
    # Password Confirm
    re_type_password = form.text_input(label='Confirm Password',type="password") 
    # email
    email = form.text_input(label='Email')    
    submit_button = form.form_submit_button(label='Submit')
    if n_password == re_type_password:
        if submit_button:  
            flag = len(check_userdatatable())
            if flag == 0:
                valid = check_email(email)
                if valid:
                    while True:
                        hashed = make_password(n_password)
                        date_of_registration =  datetime.datetime.now()
                        create_usertable()
                        add_user_data(new_user,hashed,email,date_of_registration)
                        st.success("Successfully Registration ")
                        break
                else:
                    st.warning("Email is not valid !""!")
            else:
                valid = check_email(email)
                if valid:
                    flag = check_double_email(email)
                    if len(flag) == 0:
                        flag2 = check_double_username(new_user)
                        if len(flag2) == 0:
                            while True:
                                hashed = make_password(n_password)
                                date_of_registration =  datetime.datetime.now()
                                create_usertable()
                                add_user_data(new_user,hashed,email,date_of_registration)
                                st.success("Successfully Registration ")
                                break
                        else:
                            st.warning("Username is EXISTED !""!")
                    else:
                        st.warning("Email is EXISTED !""!")         
                else:
                    st.warning("Email is not valid !""!")
    else:
        st.warning("Password is not match !!")