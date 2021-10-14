# functions
from os import makedirs
import streamlit as st
#import bcrypt
import re
import hashlib
import numpy as np
import pandas as pd
from collections import Counter
from operator import itemgetter
from sort_functions import*
import numpy as np
import pandas as pd
import csv
import sys
import base64
import io
from io import BytesIO
from PIL import Image
coef = 'file.txt'

def png_bytes_to_numpy(png):
    return np.array(Image.open(BytesIO(png)))
#@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img
def image_to_byte_array(image:Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def convert_img_to_byte(uploaded_file):
    dimenzije = Image.open(uploaded_file)
    width, height = dimenzije.size
    img = load_image(uploaded_file)
    a = image_to_byte_array(img)
    bytes_temp = png_bytes_to_numpy(a)
    return width, height, bytes_temp

def convert_bytes_to_img(width,height,a):
    data = np.zeros((height, width, 4), dtype=np.uint8)
    data[0:2560, 0:2560] = a # red patch in upper left
    img = Image.fromarray(data, 'RGBA')
    return img

def add_if_key_not_exist(dict_obj, key, value):
    if key not in dict_obj:
        dict_obj.update({key: value})

# Reading Time
def readingTime(mytext):
	total_words = len([ token for token in mytext.split(" ")])
	estimatedTime = total_words/200.0
	return estimatedTime

def stringToList(string):
    listRes = list(string.split(" "))
    return listRes

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'

def Chose_sort():

    sort_option = st.radio("Sort option",["Clasic sort","Reverse sort"])

    if sort_option == "Clasic sort":
        a = False
        return a
            
    elif sort_option == "Reverse sort":
        a = True
        return a

def get_table_download_link_csv(df):
    #csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csv file</a>'
    return href

def GETCoefficients(files,year):

    lenght = file_lengthy(files) # count the length of lines for the required size allocation of the string

    with open(files, "r") as f: # open the file
        data = f.readlines()

    count = 0 # counter for arrays

    #reserving the number of elements in a row
    y = [0] * lenght
    k = [0] * lenght

    for line in data:
        words = line.split()

        y[count] = words[0] # years
        k[count] = words[1] # coefficient
        count += 1

    # conversion to numpy
    np_years = np.asarray(y, dtype='int64')
    np_koef = np.asarray(k, dtype='float64')

    # the intake part put a try catch between the 2000 and 2009 intervals and to index them with the 2019 index

    np_specific_coefficient = np_koef[np_years == year]
    #print("\n\t You have chosen a year :  ",i)

    return np_specific_coefficient

def NumberOfRows(datFrame): # for data frame

    total_rows = len(datFrame)
    return  total_rows

def Delite_DataFrame_from_memory(DatFr):

    print("\n\t Release DataFrame memory !!!")
    del(DatFr)

def Write_multiple_DF(csv_file,dat):
    with open(csv_file, 'a') as f:  # Use append mode.
        dat.to_csv(f, index=False,header=False)

def DataFrameFunc_THROUGHT_Seasons(filePath):

    colls = ["Year_of_Season","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFunc_CLUB_THROUGHT_Seasons(filePath):

    colls = ["Order_of_Expend","Club","State","Competition","Expenditures",
                             "Income","Arrivals","Departures","Balance",
                             "inflation_Expenditure","inflation_Income","inflation_Balance"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFunc_CLUBS_Seasons(filePath):

    colls = ["Order","Club","State","Competition","Expenditures",
                    "Arrivals","Income","Departures","Balance","Season",
                    "Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFuncSeasons(filePath):

    colls = ["Name_of_Legue","Expend","Income","Balance","number_of_Season","sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues","avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFuncBalance(filePath):

    colls = ["Name_of_Legue", "Year","Nationality", "Balance_by_player", "Balance_INFLACION"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFuncIncome(filePath):

    colls = ["Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFuncExpend(filePath):

    colls = ["Name_of_Legue","Year","Nationality","Expend_by_player","Expend_INFLACION"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFuncClubs(filePath):

    colls = ["Order_of_Expend","Club","State","Competition","Expenditures","Arrivals","Income","Departures","Balance","Season"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat

def DataFrameFunc(filePath):
    #"0","Nationality","Competition","Expenditures","Arrivals","Income","Departures","Balance","Year"

    colls = ["0","Nationality","Competition","Expenditures","Arrivals","Income","Departures","Balance","Year"]
    dat = pd.read_csv(filePath,header = None , names = colls)
    return dat 

def make_password(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_password(password) == hashed_text:
		return hashed_text
	return False

# a function in python that erases repeating sequence members from the array
def remove_duplicates(l):

    return list(set(l))

# a function in python that release  memory for dataframes
def Delite_DataFrame_from_memory(DatFr):

    print("\n\t Release DataFrame memory !!!")
    del(DatFr)

#function count number of rows for specific DateFrame
def NumberOfRows(datFrame): # for data frame

    total_rows = len((datFrame))
    return  total_rows # function ~ 3.

# function  count the length of lines for the required size allocation of the string #TXT
def file_lengthy(fname):

    with open(fname) as f:
        for i ,j in enumerate (f):
            pass
        return i +1 #

#function get Coefients for specific year
def GETCoefficients(files,year):

    lenght = file_lengthy(files) # count the length of lines for the required size allocation of the string

    with open(files, "r") as f: # open the file
        data = f.readlines()

    count = 0 # counter for arrays

    #reserving the number of elements in a row
    y = [0] * lenght
    k = [0] * lenght

    for line in data:
        words = line.split()

        y[count] = words[0] # years
        k[count] = words[1] # coefficient
        count += 1

    # conversion to numpy
    np_years = np.asarray(y, dtype='int64')
    np_koef = np.asarray(k, dtype='float64')

    # the intake part put a try catch between the 2000 and 2009 intervals and to index them with the 2019 index

    np_specific_coefficient = np_koef[np_years == year]
    #print("\n\t You have chosen a year :  ",i)

    return np_specific_coefficient

# Security functions
#   -----------------------------------------------------------------
def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)




