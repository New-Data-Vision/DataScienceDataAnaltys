import streamlit as st 
import pandas as pd
import numpy as np
from functions import*


def DCWS_base(DFrame):
    #count number of rows in date frame
    count = NumberOfRows(DFrame)

    #reserving the number of elements in a row
    Nationality = [0] * count
    Arrivals = [0] * count
    Season = [0] * count
    leauge = [0] * count
    niz1 = [0] *count
    Expenditures = [0] *count
    Income = [0] *count
    Balance = [0] *count
    Departures = [0] *count

    koef = [0] * count
    inter_Balance = [0] *count
    inter_Expenditures = [0] *count
    inter_Income = [0] * count
    int_koef = [0] * count
    ###############################################################################

    # cast DataFrame rows to folat and int and str
    DFrame["Expenditures"].astype(np.int)
    DFrame["Income"].astype(np.int)
    DFrame["Balance"].astype(np.int)
    DFrame["Departures"].astype(np.int)
    DFrame["Arrivals"].astype(np.int)
    DFrame["Competition"].astype(np.str)
    DFrame["Year"].astype(np.int)
    ###############################################################################

    #save values from the dateframe to a string
    i = 0
    for i in range(0,count):
        Arrivals[i] = DFrame["Arrivals"][i]
        leauge[i] = DFrame["Competition"][i]
        Season[i] =  DFrame["Year"][i]
        Expenditures[i] =  DFrame["Expenditures"][i]
        Income[i] =  DFrame["Income"][i]
        Balance[i] =  DFrame["Balance"][i]
        Departures[i] =  DFrame["Departures"][i]
        ###############################################################################

    # calculation of coeficent of inflacion
    for i in range(0,count):
        temp = Season[i]
        a = GETCoefficients(coef,temp)
        koef[i] = a
        ###############################################################################

    for i in range(0,len(int_koef)):
        temp = float(koef[i])
        int_koef[i] = temp
        ###############################################################################
    # calculation  Inflation for Potential, Earned and Profit
    for i in range(0,count):
        a = float(Balance[i])*int_koef[i]
        b = float(Expenditures[i])*int_koef[i]
        c = float(Income[i])*int_koef[i]
        inter_Balance[i] = round(a,2)
        inter_Expenditures[i] = round(b,2)
        inter_Income[i] = round(c,2)
        ###############################################################################


    npLeauge = np.asarray(leauge, dtype = 'str')
    np_Arrival = np.asarray(Arrivals, dtype ='int')
    np_Season = np.asarray(Season, dtype = 'int' )
    np_Expenditures = np.asarray(inter_Expenditures, dtype = 'float' )
    np_Income = np.asarray(inter_Income, dtype = 'float' )
    np_Balance = np.asarray(inter_Balance, dtype = 'float' )
    np_Departures = np.asarray(Departures, dtype = 'int' )
    ###############################################################################


    np_niz1 = np.asarray(niz1, dtype = 'str')
    np_niz2 = np.asarray(niz1, dtype = 'int')
    np_niz3 = np.asarray(niz1, dtype = 'int')
    np_niz4 = np.asarray(niz1, dtype = 'int')

    #set arr to stack for operations with data lik sort and convert
    niz = np.stack((np_niz1,np_niz2,np_niz3,np_niz4,np_niz4,np_niz4,np_niz4,np_niz4,np_niz4,np_niz4,np_niz4,np_niz4,np_niz4,np_niz4), axis = -1)
    a = np.stack((np_Arrival,npLeauge,np_Expenditures,np_Income,np_Balance,np_Departures,np_Season), axis = -1)
    ###############################################################################

    # Function for sorting
    # varibales for sorting
    n = count
    t = 0

    visited = [False for i in range(n)]
    # Traverse through array elements
    # and count frequencies
    for i in range(n):
        # Skip this element if already
        # processed
        if (visited[i] == True):
            continue
        count = 1
        suma_Arrival = int(a[i][0])
        sum_Expenditures = float(a[i][2])
        sum_Income = float(a[i][3])
        sum_Balance = float(a[i][4])
        sum_Departures = int(a[i][5])
        ###############################################################################
        for j in range(i + 1, n, 1):
            if (a[i][6] == a[j][6]):
                suma_Arrival += int(a[j][0])
                sum_Expenditures += float(a[j][2])
                sum_Income += float(a[j][3])
                sum_Balance += float(a[j][4])
                sum_Departures += int(a[j][5])
                visited[j] = True
                count += 1
                ###############################################################################

        if a[i][1] != 0 :
            niz[t][1] = a[i][1]
            niz[t][0] = suma_Arrival
            niz[t][2] = count
            niz[t][3] = sum_Expenditures
            niz[t][4] = sum_Income
            niz[t][5] = sum_Departures
            niz[t][6] = sum_Balance
            niz[t][7] = round(sum_Expenditures/float(suma_Arrival),2)
            niz[t][8] = round(sum_Income/float(sum_Departures),2)
            niz[t][9] = round(sum_Balance/float(sum_Departures),2)
            niz[t][10] = round(sum_Expenditures/(count),2)
            niz[t][11] = round(sum_Income/(count),2)
            niz[t][12] = round(sum_Balance/float(count),2)
            niz[t][13] = a[i][6]
            ###############################################################################

            t +=1
            suma = 0

    # count array size with N
    N =0
    for i in range(0,len(niz)):
        if int(niz[i][0]) != 0:
            N +=1


    #Initialize a new array
    niz_1 = [0] * N


    np_niz_1 = np.asarray(niz_1,dtype='str')
    np_niz_2 = np.asarray(niz_1, dtype='int')
    np_niz_3 = np.asarray(niz_1, dtype='int')
    np_niz_4 = np.asarray(niz_1, dtype='float')


    new_niz = np.stack((np_niz_1,np_niz_2,np_niz_3,np_niz_4,np_niz_4,np_niz_4,np_niz_4,np_niz_4,np_niz_4,np_niz_4,np_niz_4,np_niz_4,np_niz_4), axis = -1)

    # avg Balance number the seasons
    for i in range(0,N):
        if int(niz[i][0]) != 0:
            # int(niz[i][0]) != 0
            new_niz[i][0] = niz[i][13] # year
            new_niz[i][1] = niz[i][3] # Expend
            new_niz[i][2] = niz[i][4] # Income
            new_niz[i][3] = niz[i][6] # Balance
            new_niz[i][4] = niz[i][2] # number of seasons
            new_niz[i][5] = niz[i][0] # sum of Arrivlas of all seasons
            new_niz[i][6] = niz[i][5] # sum of Depatrues of all seasons
            new_niz[i][7] = niz[i][7] # avg Expend of Arrivlas
            new_niz[i][8] = niz[i][8] # avg Income of Depatrues
            new_niz[i][9] = niz[i][9] # avg Balance of Depatrues
            new_niz[i][10] = niz[i][10] # avg Expend number the seasons
            new_niz[i][11] = niz[i][11] # avg Income number the seasons
            new_niz[i][12] = niz[i][12] # avg Balance number the seasons
            ###############################################################################


    # sort by appropriate elements and by columns
    # cekanje na funkciju !!!!!  meni napravljen

    # convert from stack with values to data for dataFrame
    a = input_Menisort(new_niz)
    data = np.array(a)
    # set to DataFrame
    df = pd.DataFrame(data)
    # name of labels for head or names of collums
    df.columns = ["Year_of_Season","Expend","Income","Balance","number_of_Season",
                           "sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues",
                           "avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]
    ###############################################################################
    # return DataFrame with head an names of collums
    return df

def input_Menisort(DFN):
    st.subheader("Meni options :: ")
    #   ,"Sort data by Expend + Inflation by player"
        
    options = st.selectbox("Chose sort option by ::: ",["Sorted by Order of Name of leauge","Sorted by Expend  !!! ","Sorted by Income  !!! ","Sorted by Balance  !!! ","Sorted by number of Season  !!! ","Sorted by sum of Arrivlas  !!! ","Sorted by sum of Depatrues  !!! ","Sorted by avg Expend of Arrivlas  !!! ","Sorted by avg Income of Depatrues !!! ","Sorted by avg Balance of Depatrues  !!! ","Sorted by avg Expend/Season  !!! ","Sorted by avg Income/Season !!! ","Sorted by avg Balance/Season !!! "])
    if options =="Sorted by Order of Name of leauge":
        st.subheader("Sorted by Order of Name of leauge")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[0]),reverse = b) # Order of Expend sort , str
        return a
        

    elif options == "Sorted by Expend  !!! ":
        st.subheader("Sorted by Expend  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[1]),reverse = b) # Club sort , float
        return a
            
        
    elif options == "Sorted by Income  !!! ":
        st.subheader("Sorted by Income  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[2]),reverse = b) # State sort , float 
        return a
            

    elif options == "Sorted by Balance  !!! ":
        st.subheader("Sorted by Balance  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[3]),reverse = b) # Balance sort , float
        return a

    elif options == "Sorted by number of Season  !!! ":
        st.subheader("Sorted by number of Season  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[4]),reverse = b) # number of Season sort , int
        return a

    elif options == "Sorted by sum of Arrivlas  !!! ":
        st.subheader("Sorted by sum of Arrivlas  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[5]),reverse = b) # sum of Arrivlas sort , int 
        return a

    elif options == "Sorted by sum of Depatrues  !!! ":
        st.subheader("Sorted by sum of Depatrues  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[6]),reverse = b) # sum of Arrivlas sort , int
        return a

    elif options == "Sorted by avg Expend of Arrivlas  !!! ":
        st.subheader("Sorted by avg Expend of Arrivlas  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[7]),reverse = b) #calculate avg Expend of Arrivlas sort , float
        return a

    elif options == "Sorted by avg Income of Depatrues !!! ":
        st.subheader("Sorted by avg Income of Depatrues !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[8]),reverse = b) #calculate avg Income of Depatrues sort,float
        return a

    elif options == "Sorted by avg Balance of Depatrues  !!! ":
        st.subheader("Sorted by avg Balance of Depatrues  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[9]),reverse = b) #  calculate avg Balance of Depatrues sort ,float
        return a

    elif options == "Sorted by avg Expend/Season  !!! ":
        st.subheader("Sorted by avg Expend/Season  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[10]),reverse = b) #  calculate avg Expend/Season sort ,float
        return a
    
    elif options == "Sorted by avg Income/Season !!! ":
        st.subheader("Sorted by avg Income/Season !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[11]),reverse = b) #calculate avg Income/Season sort ,float
        return a
    
    elif options == "Sorted by avg Balance/Season !!! ":
        st.subheader("Sorted by avg Balance/Season !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[12]),reverse = b) #calculate avg Balance/Season sort ,float
        return a

def DCWS_MAIN(DFrame):
    # DataFrame to ecstract data
    nDFRAME = DCWS_base(DFrame)

    #count number of rows in date frame
    count = NumberOfRows(nDFRAME)


    #reserving the number of elements in a row
    Year  = [0] * count # indx 0
    Expend = [0] * count # indx 1
    Income = [0] * count # indx 2
    Balance =  [0] * count # indx 3
    number_of_Season = [0] * count # indx 4
    sum_of_Arrivlas = [0] * count # indx 5
    sum_of_Depatrues = [0] * count # indx 6
    avg_Expend_of_Arrivlas = [0] * count # indx 7
    avg_Income_of_Depatrues =  [0] * count # indx 8
    avg_Balance_of_Depatrues = [0] * count # indx 9
    avg_Expend_Season = [0] * count # indx 10
    avg_Income_Season  =  [0] * count # indx 11
    avg_Balance_Season  =  [0] * count # indx 12

    # cast DataFrame rows to folat and int
    nDFRAME["Year_of_Season"].astype(np.int)# ind 0
    nDFRAME["Expend"].astype(np.str)# ind 1
    nDFRAME["Income"].astype(np.str)# ind 2
    nDFRAME["Balance"].astype(np.str)# ind 3
    nDFRAME["number_of_Season"].astype(np.int)# ind 4
    nDFRAME["sum_of_Arrivlas"].astype(np.int)# ind 5
    nDFRAME["sum_of_Depatrues"].astype(np.int)# ind 6
    nDFRAME["avg_Expend_of_Arrivlas"].astype(np.float)# ind 7
    nDFRAME["avg_Income_of_Depatrues"].astype(np.float)# ind 8
    nDFRAME["avg_Balance_of_Depatrues"].astype(np.float)# ind 9
    nDFRAME["avg_Expend_Season"].astype(np.float)# ind 10
    nDFRAME["avg_Income_Season"].astype(np.float)# ind 11
    nDFRAME["avg_Balance_Season"].astype(np.float)# ind 12
    ###############################################################################

    #save values from the dateframe to a arrays
    i = 0
    for i in range(0,count):

        Year[i] =  nDFRAME["Year_of_Season"][i] # indx 0
        Expend[i] = nDFRAME["Expend"][i] # indx 1
        Income[i] = nDFRAME["Income"][i] # indx 2
        Balance[i] = nDFRAME["Balance"][i] # indx 3
        number_of_Season[i] = nDFRAME["number_of_Season"][i] # indx 4
        sum_of_Arrivlas[i] = nDFRAME["sum_of_Arrivlas"][i] # indx 5
        sum_of_Depatrues[i] = nDFRAME["sum_of_Depatrues"][i] # indx 6
        avg_Expend_of_Arrivlas[i] = nDFRAME["avg_Expend_of_Arrivlas"][i] # indx 7
        avg_Income_of_Depatrues[i] = nDFRAME["avg_Income_of_Depatrues"][i] # indx 8
        avg_Balance_of_Depatrues[i] = nDFRAME["avg_Balance_of_Depatrues"][i] # indx 9
        avg_Expend_Season[i] = nDFRAME["avg_Expend_Season"][i] # indx 10
        avg_Income_Season[i] = nDFRAME["avg_Income_Season"][i] # indx 11
        avg_Balance_Season[i] = nDFRAME["avg_Balance_Season"][i] # indx 12
        ###############################################################################

    # conversion to numpy
    np_Year = np.asarray(Year, dtype = 'int') # indx 0
    np_Expend = np.asarray(Expend,dtype='float')# indx 1
    np_Income = np.asarray(Income,dtype='float')# indx 2
    np_Balance = np.asarray(Balance, dtype = 'float') # indx 3
    np_number_of_Season = np.asarray(number_of_Season,dtype='int') # indx 4
    np_sum_of_Arrivlas = np.asarray(sum_of_Arrivlas, dtype ='int') # indx 5
    np_sum_of_Depatrues = np.asarray(sum_of_Depatrues,dtype='int') # indx 6
    np_avg_Expend_of_Arrivlas = np.asarray(avg_Expend_of_Arrivlas, dtype = 'float' ) # indx 7
    np_avg_Income_of_Depatrues = np.asarray(avg_Income_of_Depatrues,dtype='float') # indx 8
    np_avg_Balance_of_Depatrues = np.asarray(avg_Balance_of_Depatrues, dtype = 'float' ) # indx 9
    np_avg_Expend_Season = np.asarray(avg_Expend_Season, dtype = 'float' ) # indx 10
    np_avg_Income_Season = np.asarray(avg_Income_Season, dtype = 'float' ) # indx 11
    np_avg_Balance_Season = np.asarray(avg_Balance_Season, dtype = 'float' ) # indx 12
    ###############################################################################

    # set the numpy arrays values into stack
    a = np.stack((np_Year,np_Expend,np_Income,np_Balance,np_number_of_Season,np_sum_of_Arrivlas,np_sum_of_Depatrues,
    np_avg_Expend_of_Arrivlas,np_avg_Income_of_Depatrues,np_avg_Balance_of_Depatrues,np_avg_Expend_Season,np_avg_Income_Season,np_avg_Balance_Season),axis= -1)
    ###############################################################################

    # convert from stack with values to data for dataFrame
    a_data = np.array(a)
    # set to DataFrame
    df_a = pd.DataFrame(a_data)
    # name of labels for head or names of collums
    df_a.columns = ["Year_of_Season","Expend","Income","Balance","number_of_Season",
                           "sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues",
                           "avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]
    ###############################################################################

    # convert data from numpay ndarray to list and remove duplicates elemtes of list for YEAR
    listYEAR = np_Year.tolist()
    listYEAR = remove_duplicates(listYEAR)
    listYEAR.sort()
    ###############################################################################


    # a function in which a user selects a choice of country or championship,
    # and chooses the name of the state or championship after which the data is printed

    # temporary variables that note the value the ticker chooses
    flag = 0
    flag_option = ''
    flagTemp = '0'
    remm = 0

    task = st.selectbox("Chose a option of proces data by YEAR",["YEAR"],key='key_options')

    if task == "YEAR":
        flag_option = "Year_of_Season"
        flag = 1
        cont_YEAR = 0
        
        st.write("Meni For - > YEAR !")
        for i in range(0,len(listYEAR)):
            cont_YEAR += 1
        options = ['0'] * cont_YEAR
        
        for i in range(0,len(listYEAR)):
            options[i] = listYEAR[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listYEAR)):
            if listYEAR[i] == remeber:
                break
            cnt +=1

     #count number of rows in date frame
    count = NumberOfRows(nDFRAME)

    # temp var for count number of roew for dynamic reserving
    bro = 0

    # count number of rows in date frame
    # YEAR
    if flag == 1:
        for i in range(0,len(a)):
            if int(a[i][0]) == flagTemp :
                bro +=1
    ###############################################################################

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

    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from State user chose options
    y = 0
    if flag == 1:
        for i in range(0,len(a)):
            if int(a[i][0]) == flagTemp :
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
    np_niz2 = np.asarray(niz_N1, dtype = 'int')
    np_niz3 = np.asarray(niz_N1, dtype = 'float')

    #set arr to stack for operations with data lik sort and convert
    new_niz = np.stack((np_niz2,np_niz3,np_niz3,np_niz3,np_niz2,np_niz2,np_niz2,np_niz3,np_niz3,np_niz3,np_niz3,np_niz3,np_niz3),axis= -1)
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
    df_new.columns = ["Year_of_Season","Expend","Income","Balance","number_of_Season",
                           "sum_of_Arrivlas","sum_of_Depatrues","avg_Expend_of_Arrivlas","avg_Income_of_Depatrues",
                           "avg_Balance_of_Depatrues","avg_Expend_Season","avg_Income_Season","avg_Balance_Season"]

    return df_new,remm,flag_option