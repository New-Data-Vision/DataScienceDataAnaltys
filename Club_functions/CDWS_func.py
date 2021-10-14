import streamlit as st 
import pandas as pd
import numpy as np
from functions import*


def CDWS_base(DFrame):
    #count number of rows in date frame
    count = NumberOfRows(DFrame)

    #reserving the number of elements in a row
    Order = [0] * count # 0
    Name_of_club = [0] * count # 1
    State = [0] * count # 2
    Competition =  [0] * count # 3
    Expenditures = [0] * count # 4
    Arrivals = [0] * count # 5
    Income = [0] * count # 6
    Departures = [0] * count # 7
    Balance =  [0] * count # 8
    Season = [0] * count # 9

    koef =  [0] * count
    interception_Expenditures = [0] * count
    interception_Income =  [0] * count
    interception_Balance = [0] * count
    int_koef = [0]* count
    ###############################################################################

    # cast DataFrame rows to folat and int
    DFrame["Order_of_Expend"].astype(np.int) # 0
    DFrame["Club"].astype(np.str) # 1
    DFrame["State"].astype(np.str) # 2
    DFrame["Competition"].astype(np.str) # 3
    DFrame["Expenditures"].astype(np.float) # 4
    DFrame["Arrivals"].astype(np.int) # 5
    DFrame["Income"].astype(np.float) # 6
    DFrame["Departures"].astype(np.int) # 7
    DFrame["Balance"].astype(np.float) # 8
    DFrame["Season"].astype(np.int) # 9
    ###############################################################################


    #save values from the dateframe to a arrays
    i = 0
    for i in range(0,count):

        Order[i] = DFrame["Order_of_Expend"][i] # 0
        Name_of_club[i] = DFrame["Club"][i] # 1
        State[i] = DFrame["State"][i] # 2
        Competition[i] = DFrame["Competition"][i] # 3
        Expenditures[i] = DFrame["Expenditures"][i]# 4
        Arrivals[i] = DFrame["Arrivals"][i]# 5
        Income[i] = DFrame["Income"][i]# 6
        Departures[i] = DFrame["Departures"][i]# 7
        Balance[i] =  DFrame["Balance"][i]# 8
        Season[i] =  DFrame["Season"][i]# 9
        ############################################################################


    # calcualtion of coeficent for clubs seasons
    for i in range(0,count):
        temp = Season[i]
        a = GETCoefficients(coef,temp)
        koef[i] = a
        ###############################################################################

    # calculation of coeficent of inflacion
    for i in range (0,len(int_koef)):
        temp = float(koef[i])
        int_koef[i] = temp
        ###############################################################################

    # calculation  Inflation for Potential, Earned and Profit
    for i in range(0,count):
        a = float(Income[i])*int_koef[i]
        b = float(Balance[i])*int_koef[i]
        c = float(Expenditures[i])*int_koef[i]
        interception_Income[i] = round(a,2)
        interception_Balance[i] = round(b,2)
        interception_Expenditures[i] = round(c,2)
        ###############################################################################


    # conversion to numpy
    np_Order = np.asarray(Order,dtype='int') # 0
    np_Club = np.asarray(Name_of_club,dtype='str') # 1
    np_State = np.asarray(State,dtype='str') # 2
    np_Competition = np.asarray(Competition,dtype='str') # 3
    np_Expenditures = np.asarray(Expenditures,dtype='float') # 4
    np_Arrivals = np.asarray(Arrivals,dtype='int') # 5
    np_Income = np.asarray(Income,dtype='float') # 6
    np_Departures = np.asarray(Departures,dtype='int') # 7
    np_Balance = np.asarray(Balance,dtype='float') # 8
    np_Seasons =  np.asarray(Season,dtype='int') # 9

    np_INF_Income = np.asarray(interception_Income,dtype='float') # 10
    np_INF_Balance = np.asarray(interception_Balance,dtype='float') # 11
    np_INF_Expenditures = np.asarray(interception_Expenditures,dtype='float') # 12
    ###############################################################################

    # set the numpy arrays values into stack
    niz = np.stack((np_Order,np_Club,np_State,np_Competition,np_Expenditures,np_Arrivals,np_Income,np_Departures,
    np_Balance,np_Seasons,np_INF_Income,np_INF_Expenditures,np_INF_Balance),axis= -1)

    # convert from stack with values to data for dataFrame
    a = input_Menisort(niz)
    # set to DataFrame
    data = np.array(a)
    # set to DataFrame
    df = pd.DataFrame(data)

    df.columns = ["Order_of_Expend","Club","State","Competition","Expenditures",
                    "Arrivals","Income","Departures","Balance","Season",
                    "Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
    ###############################################################################

    # return DataFrame with head an names of collum
    return df

def input_Menisort(DFN):
    st.subheader("Meni options :: ")
    #   ,"Sort data by Expend + Inflation by player"
        
    options = st.selectbox("Chose  option  ::: ",["Sort data BY Order","Sorted by Club  !!!","Sorted by State  !!!","Sorted by Competition  !!!","Sorted by Expenditures  !!!","Sorted by Arrivals  !!!","Sorted by Income  !!!","Sorted by Departures  !!! ","Sorted by Balance !!!","Sorted by Season  !!!","Sorted by  Inflacion + Income  !!!","Sorted by  Inflacion + Expenditures  !!!","Sorted by  Inflacion + Balance  !!!","Sorted by Competition  !!!"])
    if options =="Sort data BY Order":
        st.subheader("Sort data BY Order")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[0]),reverse = b) #  Order sort ,int
        return a
        

    elif options == "Sorted by Club  !!!":
        st.subheader("Sorted by Club  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[1]),reverse = b) # Club sort ,str
        return a
            
        
    elif options == "Sorted by State  !!!":
        st.subheader("Sorted by State  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[2]),reverse = b) # State sort , str
        return a
            

    elif options == "Sorted by Expenditures  !!!":
        st.subheader("Sorted by Expenditures  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[4]),reverse = b) # Expenditures, float
        return a

    elif options == "Sorted by Arrivals  !!!":
        st.subheader("Sorted by Arrivals  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[5]),reverse = b) # Arrivals sort , int
        return a

    elif options == "Sorted by Income  !!!":
        st.subheader("Sorted by Income  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[6]),reverse = b) # Income sort , float
        return a

    elif options == "Sorted by sum of Depatrues  !!! ":
        st.subheader("Sorted by sum of Depatrues  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[7]),reverse = b) # Departures sort , int
        return a

    elif options == "Sorted by Balance !!!":
        st.subheader("Sorted by Balance !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[8]),reverse = b) # Balance sort ,float
        return a

    elif options == "Sorted by Season  !!!":
        st.subheader("Sorted by Season  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[9]),reverse = b) # Season sort ,int
        return a

    elif options == "Sorted by  Inflacion + Income  !!!":
        st.subheader("Sorted by  Inflacion + Income  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[10]),reverse = b) #  Inflacion + Income sort ,float
        return a

    elif options == "Sorted by  Inflacion + Expenditures  !!!":
        st.subheader("Sorted by  Inflacion + Expenditures  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[11]),reverse = b) #  Inflacion + Expenditures sort ,float
        return a
    
    elif options == "Sorted by  Inflacion + Balance  !!!":
        st.subheader("Sorted by  Inflacion + Balance  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[12]),reverse = b) #  Inflacion + Balance sort ,float
        return a
    
    elif options == "Sorted by Competition  !!!":
        st.subheader("Sorted by Competition  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[3]),reverse = b) # Competition sort , str
        return a

def CDWS_MENI(DFrame):
    # DataFrame to ecstract data
    nDFRAME = CDWS_base(DFrame)

    #count number of rows in date frame
    count = NumberOfRows(nDFRAME)

    #reserving the number of elements in a row
    Order  = [0] * count # indx 0
    Club = [0] * count # indx 1
    State = [0] * count # indx 2
    Competition =  [0] * count # indx 3
    Expenditures = [0] * count # indx 4
    Arrivals = [0] * count # indx 5
    Income = [0] * count # indx 6
    Departures = [0] * count # indx 7
    Balance =  [0] * count # indx 8
    Season = [0] * count # indx 9
    inflation_Income = [0] * count # indx 10
    inflation_Expenditures = [0] * count # indx 11
    inflation_Balance =  [0] * count # indx 12

    # "Order","Club","State","Competition","Expenditures",
    #                "Arrivals","Income","Departures","Balance","Season",
    #                "Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"

    # cast DataFrame rows to folat and int
    nDFRAME["Order_of_Expend"].astype(np.int)# ind 0
    nDFRAME["Club"].astype(np.str)# ind 1
    nDFRAME["State"].astype(np.str)# ind 2
    nDFRAME["Competition"].astype(np.str)# ind 3
    nDFRAME["Expenditures"].astype(np.float)# ind 4
    nDFRAME["Arrivals"].astype(np.int)# ind 5
    nDFRAME["Income"].astype(np.float)# ind 6
    nDFRAME["Departures"].astype(np.int)# ind 7
    nDFRAME["Balance"].astype(np.float)# ind 8
    nDFRAME["Season"].astype(np.int)# ind 9
    nDFRAME["Inflacion_Income"].astype(np.float)# ind 10
    nDFRAME["Inflacion_Expenditures"].astype(np.float)# ind 11
    nDFRAME["Inflacion_Balance"].astype(np.float)# ind 12
    ###############################################################################

    #save values from the dateframe to a arrays
    i = 0
    for i in range(0,count):

        Order[i] =  nDFRAME["Order_of_Expend"][i] # indx 0
        Club[i] = nDFRAME["Club"][i] # indx 1
        State[i] = nDFRAME["State"][i] # indx 2
        Competition[i] = nDFRAME["Competition"][i] # indx 3
        Expenditures[i] = nDFRAME["Expenditures"][i] # indx 4
        Arrivals[i] = nDFRAME["Arrivals"][i] # indx 5
        Income[i] = nDFRAME["Income"][i] # indx 6
        Departures[i] = nDFRAME["Departures"][i] # indx 7
        Balance[i] = nDFRAME["Balance"][i] # indx 8
        Season[i] = nDFRAME["Season"][i] # indx 9
        inflation_Income[i] = nDFRAME["Inflacion_Income"][i] # indx 10
        inflation_Expenditures[i] = nDFRAME["Inflacion_Expenditures"][i] # indx 11
        inflation_Balance[i] = nDFRAME["Inflacion_Balance"][i] # indx 12
        ###############################################################################

    # conversion to numpy
    np_Order = np.asarray(Order, dtype = 'int') # indx 0
    np_Club = np.asarray(Club,dtype='str')# indx 1
    np_State = np.asarray(State,dtype='str')# indx 2
    np_Competition = np.asarray(Competition, dtype = 'str') # indx 3
    np_Expenditures = np.asarray(Expenditures,dtype='float') # indx 4
    np_Arrivals = np.asarray(Arrivals, dtype ='int') # indx 5
    np_Income = np.asarray(Income,dtype='float') # indx 6
    np_Departures = np.asarray(Departures, dtype = 'int' ) # indx 7
    np_Balance = np.asarray(Balance,dtype='float') # indx 8
    np_Season = np.asarray(Season,dtype='int') # indx 9
    np_inflation_Income = np.asarray(inflation_Income, dtype = 'float' ) # indx 10
    np_inflation_Expenditures = np.asarray(inflation_Expenditures, dtype = 'float' ) # indx 11
    np_inflation_Balance = np.asarray(inflation_Balance, dtype = 'float' ) # indx 12
    ###############################################################################

    # set the numpy arrays values into stack
    a = np.stack((np_Order,np_Club,np_State,np_Competition,np_Expenditures,np_Arrivals,np_Income,np_Departures,np_Balance,
    np_Season,np_inflation_Income,np_inflation_Expenditures,np_inflation_Balance),axis= -1)
    ###############################################################################

    # convert from stack with values to data for dataFrame
    a_data = np.array(a)
    # set to DataFrame
    df_a = pd.DataFrame(a_data)
    # name of labels for head or names of collums
    df_a.columns = ["Order_of_Expend","Club","State","Competition","Expenditures",
                    "Arrivals","Income","Departures","Balance","Season",
                    "Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
    ###############################################################################
    # CLUB
    # convert data from numpay ndarray to list and remove duplicates elemtes of list for CLUB
    listClub = np_Club.tolist()
    listClub = remove_duplicates(listClub)
    listClub.sort()

    #STATE
    # convert data from numpay ndarray to list and remove duplicates elemtes of list for STATE
    listState = np_State.tolist()
    listState = remove_duplicates(listState)
    listState.sort()
    ###############################################################################

    # COMPETITION
    # convert data from numpay ndarray to list and remove duplicates elemtes of list for CLUB
    listCOMPETITION = np_Competition.tolist()
    listCOMPETITION = remove_duplicates(listCOMPETITION)
    listCOMPETITION.sort()

    # SESAON
    # convert data from numpay ndarray to list and remove duplicates elemtes of list for Competition
    listSESAON = np_Season.tolist()
    listSESAON = remove_duplicates(listSESAON)
    listSESAON.sort()
    ###############################################################################
    #######################################################################################################################################

    # a function in which a user selects a choice of country or championship,
    # and chooses the name of the state or championship after which the data is printed

    # temporary variables that note the value the ticker chooses
    flag = 0
    flagTemp = '0'

    task = st.selectbox("Chose a option of proces data by YEAR",["Club statistic !","State statistic !","Competition statistic !","Season statistic !"],key='key_options')

    if task == "Club statistic !":
        flag_option = "Club"
        flag = 1
        cont_CLUB = 0
        
        st.write("Enter Club ")
        for i in range(0,len(listClub)):
            cont_CLUB += 1
        options = ['0'] * cont_CLUB
        
        for i in range(0,len(listClub)):
            options[i] = listClub[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listClub)):
            if listClub[i] == remeber:
                break
            cnt +=1

        
    elif task == "State statistic !":
        flag_option = "State"
        flag = 2
        cont_State = 0
        
        st.write("Enter State ")
        
        for i in range(0,len(listState)):
            cont_State += 1
        options = ['0'] * cont_State
        for i in range(0,len(listState)):
            options[i] = listState[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listState)):
            if listState[i] == remeber:
                break
            cnt +=1

    elif task == "Competition statistic !":
        flag_option = "Competition"
        flag = 3
        cont_COMPETITION = 0
        
        st.write("Enter Competition ")
        for i in range(0,len(listCOMPETITION)):
            cont_COMPETITION += 1
        options = ['0'] * cont_COMPETITION
        
        for i in range(0,len(listCOMPETITION)):
            options[i] = listCOMPETITION[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listCOMPETITION)):
            if listCOMPETITION[i] == remeber:
                break
            cnt +=1

    elif task == "Season statistic !":
        flag_option = "Season"
        flag = 4
        cont_Seson = 0
        
        st.write("Enter Season ")
        for i in range(0,len(listSESAON)):
            cont_Seson += 1
        options = ['0'] * cont_Seson
        
        for i in range(0,len(listSESAON)):
            options[i] = listSESAON[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listSESAON)):
            if listSESAON[i] == remeber:
                break
            cnt +=1

    #count number of rows in date frame
    count = NumberOfRows(nDFRAME)

    # temp var for count number of roew for dynamic reserving
    bro = 0

    # count number of rows in date frame
    # CLUB
    if flag == 1:
        for i in range(0,len(a)):
            if str(a[i][1]) == flagTemp :
                bro +=1
    ###############################################################################
    # count number of rows in date frame
    # STATE
    if flag == 2:
        for i in range(0,len(a)):
            if str(a[i][2]) == flagTemp :
                bro +=1
    ###############################################################################
    # count number of rows in date frame
    # COMPETITION
    if flag == 3:
        for i in range(0,len(a)):
            if str(a[i][3]) == flagTemp :
                bro +=1
    ###############################################################################
    # count number of rows in date frame
    # SESAON
    if flag == 4:
        for i in range(0,len(a)):
            if int(a[i][9]) == flagTemp :
                bro +=1
    ###############################################################################
    #######################################################################################################################################
    # reserving the number of elements in a row
    array1 = [0] * bro
    array2 = [0] * bro
    array3 = [0] * bro
    array4 = [0] * bro
    array5 = [0] * bro
    array6 = [0] * bro
    array7 = [0] * bro
    array8 = [0] * bro
    array9 = [0] * bro
    array10 = [0] * bro
    array11 = [0] * bro
    array12 = [0] * bro
    array13 = [0] * bro
    ###############################################################################

    y = 0
    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from CLUB user chose options
    # CLUB
    if flag == 1:
        for i in range(0,len(a)):
            if str(a[i][1]) == flagTemp :
                array1[y] = a[i][0]
                array2[y] = a[i][1]
                array3[y] = a[i][2]
                array4[y] = a[i][3]
                array5[y] = a[i][4]
                array6[y] = a[i][5]
                array7[y] = a[i][6]
                array8[y] = a[i][7]
                array9[y] = a[i][8]
                array10[y] = a[i][9]
                array11[y] = a[i][10]
                array12[y] = a[i][11]
                array13[y] = a[i][12]
                y+=1
    ###############################################################################

    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from STATE user chose options
    # STATE
    if flag == 2:
        for i in range(0,len(a)):
            if str(a[i][2]) == flagTemp :
                array1[y] = a[i][0]
                array2[y] = a[i][1]
                array3[y] = a[i][2]
                array4[y] = a[i][3]
                array5[y] = a[i][4]
                array6[y] = a[i][5]
                array7[y] = a[i][6]
                array8[y] = a[i][7]
                array9[y] = a[i][8]
                array10[y] = a[i][9]
                array11[y] = a[i][10]
                array12[y] = a[i][11]
                array13[y] = a[i][12]
                y+=1
    ###############################################################################

    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from Competition user chose options
    # COMPETITION
    if flag == 3:
        for i in range(0,len(a)):
            if str(a[i][3]) == flagTemp :
                array1[y] = a[i][0]
                array2[y] = a[i][1]
                array3[y] = a[i][2]
                array4[y] = a[i][3]
                array5[y] = a[i][4]
                array6[y] = a[i][5]
                array7[y] = a[i][6]
                array8[y] = a[i][7]
                array9[y] = a[i][8]
                array10[y] = a[i][9]
                array11[y] = a[i][10]
                array12[y] = a[i][11]
                array13[y] = a[i][12]
                y+=1
    ###############################################################################

    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from Competition user chose options
    # SESAON
    if flag == 4:
        for i in range(0,len(a)):
            if int(a[i][9]) == flagTemp :
                array1[y] = a[i][0]
                array2[y] = a[i][1]
                array3[y] = a[i][2]
                array4[y] = a[i][3]
                array5[y] = a[i][4]
                array6[y] = a[i][5]
                array7[y] = a[i][6]
                array8[y] = a[i][7]
                array9[y] = a[i][8]
                array10[y] = a[i][9]
                array11[y] = a[i][10]
                array12[y] = a[i][11]
                array13[y] = a[i][12]
                y+=1
    ###############################################################################

    # reserving the number of elements in a row
    niz_N1 = [0]*bro
    #Initialize a new array
    np_niz1 = np.asarray(niz_N1, dtype = 'str')
    np_niz2 = np.asarray(niz_N1, dtype = 'int')
    np_niz3 = np.asarray(niz_N1, dtype = 'float')

    #set arr to stack for operations with data lik sort and convert
    new_niz = np.stack((np_niz2,np_niz1,np_niz1,np_niz1,np_niz3,np_niz2,np_niz3,np_niz2,np_niz3,np_niz2,np_niz3,np_niz3,np_niz3),axis= -1)
    #######################################################################################################################################

    # relocating data from temporary arrays to numpy arrays
    y = 0
    for i in range(0,bro):
        new_niz[i][0] = array1[y]
        new_niz[i][1] = array2[y]
        new_niz[i][2] = array3[y]
        new_niz[i][3] = array4[y]
        new_niz[i][4] = array5[y]
        new_niz[i][5] = array6[y]
        new_niz[i][6] = array7[y]
        new_niz[i][7] = array8[y]
        new_niz[i][8] = array9[y]
        new_niz[i][9] = array10[y]
        new_niz[i][10] = array11[y]
        new_niz[i][11] = array12[y]
        new_niz[i][12] = array13[y]
        y+=1
    ###############################################################################

    # convert from stack with values to data for dataFrame
    new_data = np.array(new_niz)
    # set to DataFrame
    df_new = pd.DataFrame(new_data)
    # name of labels for head or names of collums
    df_new.columns = ["Order_of_Expend","Club","State","Competition","Expenditures",
                    "Arrivals","Income","Departures","Balance","Season",
                    "Inflacion_Income","Inflacion_Expenditures","Inflacion_Balance"]
    return df_new,remm,flag_option