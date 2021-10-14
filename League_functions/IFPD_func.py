import streamlit as st 
import pandas as pd
import numpy as np
from functions import*


def IFPD_base(DFrame):
    #count number of rows in date frame
    count = NumberOfRows(DFrame)

    #reserving the number of elements in a row
    Nationality = [0] * count
    Income = [0] * count
    Departures = [0] * count
    leauge = [0] * count
    Season = [0] * count
    koef = [0] * count
    CUT =  [0] * count
    interception = [0] * count
    int_koef = [0] * count
    ###############################################################################

    # cast DataFrame rows to folat and int
    DFrame["Income"].astype(np.int)
    DFrame["Departures"].astype(np.int)
    DFrame["Nationality"].astype(np.str)
    DFrame["Competition"].astype(np.str)
    DFrame["Year"].astype(np.int)
    ###############################################################################

    #save values from the dateframe to a string
    i = 0
    for i in range(0,count):
        Income[i] = DFrame["Income"][i]
        Departures[i] = DFrame["Departures"][i]
        leauge[i] = DFrame["Competition"][i]
        Season[i] = DFrame["Year"][i]
        Nationality[i] = DFrame["Nationality"][i]
        ###############################################################################

    for i in range(0,count):
        temp = Season[i]
        a = GETCoefficients(coef,temp)
        koef[i] = a
        ###############################################################################

    for i in range(0,len(int_koef)):
        temp = float(koef[i])
        int_koef[i] = temp
        ###############################################################################

    for i in range(0,count):
        a = float(Income[i])*int_koef[i]
        interception[i] = round(a,2)
        ###############################################################################


    # conversion to numpy
    np_Income = np.asarray(Income, dtype='float')
    np_Departures = np.asarray(Departures, dtype='int')
    npNationality = np.asarray(Nationality, dtype='str')
    np_Season = np.asarray(Season, dtype='int')
    npLeauge = np.asarray(leauge, dtype='str')
    np_CUT = np.asarray(CUT, dtype='float')
    np_Interception = np.asarray(interception, dtype='float')
    ###############################################################################

    np_CUT = np_Income/np_Departures
    np_CUT_inflation = np_Interception/np_Departures

    niz = np.stack((npLeauge,np_Season,npNationality,np.round(np_CUT,2),np.round(np_CUT_inflation,2)), axis = -1)

    ###############################################################################
    a = input_Menisort(niz)
    # convert from stack with values to data for dataFrame
    data = np.array(a)
    # set to DataFrame
    df = pd.DataFrame(data)
    # name of labels for head or names of collums
    df.columns = ["Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"]
    ###############################################################################
    # return DataFrame with head an names of collums
    return df

def IFPD_MAIN(DFrame):
    # DataFrame to ecstract data
    nDFRAME = IFPD_base(DFrame)

    #count number of rows in date frame
    count = NumberOfRows(nDFRAME)


    #reserving the number of elements in a row
    Name_of_leauge  = [0] * count # indx 0
    Year_of_Season = [0] * count # indx 1
    Nationality = [0] * count # indx 2
    Income_by_player = [0] * count # indx 3
    Income_Inflation_by_player = [0] * count # indx 4

    # '    Name of League |  ', '   Year of Season |  ','    Nationality |  ', '    Income by player|  ', '  Income + Inflation by player|  '
    # cast DataFrame rows to folat and int
    #   "Name_of_Legue","Year","Nationality","Income_by_player","Income_INFLACION"
    nDFRAME["Name_of_Legue"].astype(np.str)# ind 0
    nDFRAME["Year"].astype(np.int)# ind 1
    nDFRAME["Nationality"].astype(np.str)# ind 2
    nDFRAME["Income_by_player"].astype(np.float)# ind 3
    nDFRAME["Income_INFLACION"].astype(np.float)# ind 4
    ###############################################################################

    #save values from the dateframe to a arrays
    i = 0
    for i in range(0,count):
        Name_of_leauge[i] =  nDFRAME["Name_of_Legue"][i] # indx 0
        Year_of_Season[i] = nDFRAME["Year"][i] # indx 1
        Nationality[i] = nDFRAME["Nationality"][i] # indx 2
        Income_by_player[i] = nDFRAME["Income_by_player"][i] # indx 3
        Income_Inflation_by_player[i] = nDFRAME["Income_INFLACION"][i] # indx 4
        ###############################################################################

    # conversion to numpy
    np_Name_of_leauge = np.asarray(Name_of_leauge, dtype = 'str') # indx 0
    np_Year_of_Season = np.asarray(Year_of_Season,dtype='int64')# indx 1
    np_Nationality = np.asarray(Nationality,dtype='str')# indx 2
    np_Income_by_player = np.asarray(Income_by_player, dtype = 'float64') # indx 3
    np_Income_Inflation_by_player = np.asarray(Income_Inflation_by_player,dtype='float64') # indx 4
    ###############################################################################

    # set the numpy arrays values into stack
    a = np.stack((np_Name_of_leauge,np_Year_of_Season,np_Nationality,np_Income_by_player,np_Income_Inflation_by_player),axis= -1)
    ###############################################################################

    # convert from stack with values to data for dataFrame
    a_data = np.array(a)
    # set to DataFrame
    df_a = pd.DataFrame(a_data)
    # name of labels for head or names of collums
    df_a.columns = ["Name_of_Legue", "Year","Nationality", "Income_by_player", "Income_INFLACION"]
    ###############################################################################

    # convert data from numpay ndarray to list and remove duplicates elemtes of list for LEAUGE
    listLEAUGE = np_Name_of_leauge.tolist()
    listLEAUGE = remove_duplicates(listLEAUGE)
    listLEAUGE.sort()
    ###############################################################################

    # convert data from numpay ndarray to list and remove duplicates elemtes of list for Year_of_Season
    listYear_of_Season = np_Year_of_Season.tolist()
    listYear_of_Season = remove_duplicates(listYear_of_Season)
    listYear_of_Season.sort()
    ###############################################################################

    # convert data from numpay ndarray to list and remove duplicates elemtes of list for Nationality
    listNationality = np_Nationality.tolist()
    listNationality = remove_duplicates(listNationality)
    listNationality.sort()
    ###############################################################################
    #######################################################################################################################################

    # a function in which a user selects a choice of country or championship,
    # and chooses the name of the state or championship after which the data is printed

    # temporary variables that note the value the ticker chooses
    flag = 0
    flagTemp = '0'
    remm = 0
    task = st.selectbox("Task task meni",["LEAUGE statistic","Year_of_Season statistic","Nationality statistic"],key='key_options')

    if task == "LEAUGE statistic":
        flag_option ="LEAUGE"
        flag = 1
        cont_LEAUGE = 0
        
        st.write("Meni  LEAUGE statistic")
        for i in range(0,len(listLEAUGE)):
            cont_LEAUGE += 1
        options = ['0'] * cont_LEAUGE
        
        for i in range(0,len(listLEAUGE)):
            options[i] = listLEAUGE[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listLEAUGE)):
            if listLEAUGE[i] == remeber:
                break
            cnt +=1

    elif task == "Year_of_Season statistic":
        flag_option = "Year_of_Season"
        flag = 2
        cont_LEAUGE = 0
        
        st.write("Meni  Year_of_Season statistic")
        for i in range(0,len(listYear_of_Season)):
            cont_LEAUGE += 1
        options = ['0'] * cont_LEAUGE

        for i in range(0,len(listYear_of_Season)):
            options[i] = listYear_of_Season[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listYear_of_Season)):
            if listYear_of_Season[i] == remeber:
                break
            cnt +=1
        
    elif task == "Nationality statistic":
        flag_option = "Nationality"
        flag = 3
        cont_LEAUGE = 0
        
        st.write("Meni  listNationality")
        for i in range(0,len(listNationality)):
            cont_LEAUGE += 1
        options = ['0'] * cont_LEAUGE
        
        for i in range(0,len(listNationality)):
            options[i] = listNationality[i]

        remeber = st.selectbox("Select Dynamic",options= list(options))
        #st.write("Added ",remeber)
        flagTemp = remeber
        remm = remeber
        cnt = 1
        for i in range(0,len(listNationality)):
            if listNationality[i] == remeber:
                break
            cnt +=1


    #count number of rows in date frame
    count = NumberOfRows(nDFRAME)

    # temp var for count number of roew for dynamic reserving
    bro = 0

    # count number of rows in date frame
    # name of LEAUGE
    if flag == 1:
        for i in range(0,len(a)):
            if str(a[i][0]) == flagTemp :
                bro +=1
    ###############################################################################

    # count number of rows in date frame
    # number of Season
    if flag == 2:
        for i in range(0,len(a)):
            if int(a[i][1]) == flagTemp :
                bro +=1
    ###############################################################################

    #   count number of rows in date frame
    #   Nationality
    if flag == 3:
        for i in range(0,len(a)):
            if str(a[i][2]) == flagTemp :
                bro +=1
    ###############################################################################

    # reserving the number of elements in a row
    array1 = [0] * bro
    array2 = [0] * bro
    array3 = [0] * bro
    array4 = [0] * bro
    array5 = [0] * bro
    ###############################################################################

    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from State user chose options

    # name of LEAUGE
    y = 0
    if flag == 1:
        for i in range(0,len(a)):
            if str(a[i][0]) == flagTemp :
                array1[y] = a[i][0]
                array2[y] = a[i][1]
                array3[y] = a[i][2]
                array4[y] = a[i][3]
                array5[y] = a[i][4]
                y+=1
    ###############################################################################

    # number of Season
    if flag == 2:
        for i in range(0,len(a)):
            if int(a[i][1]) == flagTemp :
                array1[y] = a[i][0]
                array2[y] = a[i][1]
                array3[y] = a[i][2]
                array4[y] = a[i][3]
                array5[y] = a[i][4]
                y+=1
    ###############################################################################

    # Nationality
    if flag == 3:
        for i in range(0,len(a)):
            if str(a[i][2]) == flagTemp :
                array1[y] = a[i][0]
                array2[y] = a[i][1]
                array3[y] = a[i][2]
                array4[y] = a[i][3]
                array5[y] = a[i][4]
                y+=1
    ###############################################################################

    # reserving the number of elements in a row
    niz_N1 = [0]*bro

    #Initialize a new array
    np_niz1 = np.asarray(niz_N1, dtype = 'str')
    np_niz2 = np.asarray(niz_N1, dtype = 'int')
    np_niz3 = np.asarray(niz_N1, dtype = 'float')

    #set arr to stack for operations with data lik sort and convert
    new_niz = np.stack((np_niz1,np_niz2,np_niz1,np_niz3,np_niz3),axis= -1)
    #######################################################################################################################################

    # relocating data from temporary arrays to numpy arrays
    y = 0
    for i in range(0,bro):
        new_niz[i][0] = array1[y]
        new_niz[i][1] = array2[y]
        new_niz[i][2] = array3[y]
        new_niz[i][3] = array4[y]
        new_niz[i][4] = array5[y]
        y+=1
    ###############################################################################

    

    # convert from stack with values to data for dataFrame
    new_data = np.array(new_niz)
    # set to DataFrame
    df_new = pd.DataFrame(new_data)
    # name of labels for head or names of collums
    df_new.columns = ["Name_of_Legue", "Year","Nationality", "Income_by_player", "Income_INFLACION"]
    return df_new,remm,flag_option

def input_Menisort(DFN):
    st.subheader("Meni options :: ")
    #   ,"Sort data by Expend + Inflation by player"
        
    options = st.selectbox("Chose sort option by ::: ",["Sort data by Name of League","Sort data by Nationality","Sort data by Year of Season","Sort data by Income by player"])
    if options =="Sort data by Name of League":
        st.subheader("Sort data by Name of League")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[0]),reverse = b) 
        return a
        

    elif options == "Sort data by Year of Season":
        st.subheader("Sort data by Year of Season")
        b = Chose_sort()
        a = sorted(DFN, key=lambda DFN: int(DFN[1]),reverse = b) 
        return a
            
        
    elif options == "Sort data by Nationality":
        st.subheader("Sort data by Nationality")
        b = Chose_sort()
        a = sorted(DFN, key=lambda DFN: str(DFN[2]),reverse = b) 
        return a
            

    elif options == "Sort data by Income by player":
        st.subheader("Sort data by Income by player")
        b = Chose_sort()
        a = sorted(DFN, key=lambda DFN: float(DFN[3]),reverse = b) 
        return a