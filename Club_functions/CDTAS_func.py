import streamlit as st 
import pandas as pd
import numpy as np
from functions import*


def DCTAS_base(DFrame):

    #count number of rows in date frame
    count = NumberOfRows(DFrame)

    #reserving the number of elements in a row
    Order  = [0] * count # indx 0
    Name_of_club = [0] * count # indx 1
    State_of_club = [0] * count # indx 2
    Competition =  [0] * count # indx 3
    Expenditures = [0] * count # indx 4
    Arrivals = [0] * count # indx 5
    Income = [0] * count # indx 6
    Departures = [0] * count # indx 7
    Balance =  [0] * count # indx 8
    Season = [0] * count # ind 9
    ###############################################################################

    # optimized array for operation for counting of  inflation
    koef =  [0] * count
    interception_Expenditures = [0] * count # ind 10
    interception_Income =  [0] * count# ind 11
    interception_Balance = [0] * count# ind 12
    int_koef = [0]* count
    niz1 = [0]* count
    ###############################################################################

    # cast DataFrame rows to folat and int
    DFrame["Order_of_Expend"].astype(np.int)# ind 0
    DFrame["Club"].astype(np.str)# ind 1
    DFrame["State"].astype(np.str)# ind 2
    DFrame["Competition"].astype(np.str)# ind 3
    DFrame["Expenditures"].astype(np.float)# ind 4
    DFrame["Arrivals"].astype(np.int)# ind 5
    DFrame["Income"].astype(np.float)# ind 6
    DFrame["Departures"].astype(np.int)# ind 7
    DFrame["Balance"].astype(np.float)# ind 8
    DFrame["Season"].astype(np.int)# ind 9
    ###############################################################################

    #save values from the dateframe to a arrays
    i = 0
    for i in range(0,count):

        Order[i] = DFrame["Order_of_Expend"][i] # indx 0
        Name_of_club[i] = DFrame["Club"][i] # indx 1
        State_of_club[i] =  DFrame["State"][i]# indx 2
        Competition[i] = DFrame["Competition"][i] # indx 3
        Expenditures[i] =  DFrame["Expenditures"][i]# indx 4
        Arrivals[i] =  DFrame["Arrivals"][i]# indx 5
        Income[i] =  DFrame["Income"][i]# indx 6
        Departures[i] =  DFrame["Departures"][i]# indx 7
        Balance[i] =  DFrame["Balance"][i]# indx 8
        Season[i] =  DFrame["Season"][i]# ind 9
        ###############################################################################

    # calcualtion of coeficent for clubs seasons
    for i in range(0,count):
        temp = Season[i]
        a = GETCoefficients(coef,temp)
        koef[i] = a

    # calculation of coeficent of inflacion
    for i in range (0,len(int_koef)):
        temp = float(koef[i])
        int_koef[i] = temp

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
    np_Order = np.asarray(Order, dtype = 'int') # indx 0
    np_Name_of_club = np.asarray(Name_of_club,dtype='str')# indx 1
    np_State_of_club = np.asarray(State_of_club,dtype='str')# indx 2
    npLeauge = np.asarray(Competition, dtype = 'str') # indx 3
    np_Expenditures = np.asarray(Expenditures,dtype='float64') # indx 4
    np_Arrival = np.asarray(Arrivals, dtype ='int') # indx 5
    np_Income = np.asarray(Income,dtype='float') # indx 6
    np_Departures = np.asarray(Departures, dtype = 'int' ) # indx 7
    np_Balance = np.asarray(Balance,dtype='float') # indx 8
    np_Season = np.asarray(Season, dtype = 'int' ) # indx 9
    np_in_Expenditure = np.asarray(interception_Expenditures, dtype = 'float' ) # indx 10
    np_in_Income = np.asarray(interception_Income, dtype = 'float' ) # indx 11
    np_in_Balance = np.asarray(interception_Balance, dtype = 'float' ) # indx 12
    ###############################################################################


    # set the numpy arrays values into stack
    a = np.stack((np_Order,np_Name_of_club,np_State_of_club,npLeauge,np_Expenditures,np_Arrival,np_Income,
    np_Departures,np_Balance,np_Season,np_in_Expenditure,np_in_Income,np_in_Balance),axis= -1)


    np_niz1 = np.asarray(niz1, dtype = 'str')
    np_niz2 = np.asarray(niz1, dtype = 'int')
    np_niz3 = np.asarray(niz1, dtype = 'float')

    #set arr to stack for operations with data lik sort and convert
    niz = np.stack((np_niz2,np_niz1,np_niz1,np_niz1,np_niz3,np_niz2,np_niz3,np_niz2,np_niz3,np_niz2,np_niz3,np_niz3,np_niz3),axis= -1)
    ###############################################################################

    # Function for sorting
    # variables in function for sorting
    n = count
    t = 0
    flag =  0

    visited = [False for i in range(n)]
    # Traverse through array elements
    # and count frequencies
    for i in range(n):
        # Skip this element if already
        # processed
        if (visited[i] == True):
            continue
        count = 1
        club = a[i][1]

        if club != 0:
            flag +=1

        suma_Arrival = int(a[i][5])
        sum_INF_Expenditures = float(a[i][10])
        sum_INF_Income = float(a[i][11])
        sum_INF_Balance = float(a[i][12])
        sum_Expenditures = float(a[i][4])
        sum_Income = float(a[i][6])
        sum_Balance = float(a[i][8])
        sum_Departures = int(a[i][7])
        ###############################################################################

        for j in range(i + 1, n, 1):
            if (a[i][1] == a[j][1]):

                suma_Arrival += int(a[j][5])
                sum_Expenditures += float(a[j][4])
                sum_Income += float(a[j][6])
                sum_Balance += float(a[j][8])
                sum_Departures += int(a[j][7])
                sum_INF_Expenditures += float(a[j][10])
                sum_INF_Income += float(a[j][11])
                sum_INF_Balance += float(a[j][12])
                visited[j] = True
                count += 1
                ###############################################################################
        if a[i][1] != 0 :
            niz[t][0] = a[i][0]
            niz[t][1] = a[i][1]
            niz[t][2] = a[i][2]
            niz[t][3] = a[i][3]
            niz[t][4] = sum_Expenditures
            niz[t][5] = suma_Arrival
            niz[t][6] = sum_Income
            niz[t][7] = sum_Departures
            niz[t][8] = sum_Balance
            niz[t][9] = a[i][9]
            niz[t][10] = sum_INF_Expenditures
            niz[t][11] = sum_INF_Income
            niz[t][12] = sum_INF_Balance
            ###############################################################################

            t +=1
            suma = 0

    # count array size with N
    # variables for flag
    N = flag
    niz_N1 = [0] * flag


    #Initialize a new array

    np_niz1 = np.asarray(niz_N1, dtype = 'str')
    np_niz2 = np.asarray(niz_N1, dtype = 'int64')
    np_niz3 = np.asarray(niz_N1, dtype = 'float64')

    #set arr to stack for operations with data lik sort and convert
    new_niz = np.stack((np_niz2,np_niz1,np_niz1,np_niz1,np_niz3,np_niz2,np_niz3,np_niz2,np_niz3,np_niz3,np_niz3,np_niz3),axis= -1)

    # avg Balance number the seasons
    for i in range(0,N):
        new_niz[i][0] = niz[i][0]
        new_niz[i][1] = niz[i][1]
        new_niz[i][2] = niz[i][2]
        new_niz[i][3] = niz[i][3]
        new_niz[i][4] = niz[i][4]
        new_niz[i][6] = niz[i][5]
        new_niz[i][5] = niz[i][6]
        new_niz[i][7] = niz[i][7]
        new_niz[i][8] = niz[i][8]
        #new_niz[i][9] = niz[i][9]
        new_niz[i][9] = niz[i][10]
        new_niz[i][10] = niz[i][11]
        new_niz[i][11] = niz[i][12]
        ###############################################################################

    # sort by appropriate elements and by columns
    a = input_Menisort(new_niz)

    # convert from stack with values to data for dataFrame
    data = np.array(a)
    # set to DataFrame
    df = pd.DataFrame(data)
    # name of labels for head or names of collums
    df.columns = ["Order_of_Expend","Club","State","Competition","Expenditures",
                             "Income","Arrivals","Departures","Balance",
                             "inflation_Expenditure","inflation_Income","inflation_Balance"]
    ###############################################################################(
    # return DataFrame with head an names of collums
    return df

def input_Menisort(DFN):
    st.subheader("Meni options :: ")
    #   ,"Sort data by Expend + Inflation by player"
        
    options = st.selectbox("Chose  option  ::: ",["Sort data BY inflation calculate on Income","Sorted by inflation calculate on Expenditure sort  !!!","Sorted by Balance sort !!!","Sorted by Departures  !!!","Sorted by Arrivals  !!!","Sorted by Income  !!!","Sorted by Expenditures  !!!","Sort data BY Competition","Sorted by Order of Expend  !!!","Sorted by Club sort  !!!","Sorted by State sort  !!! "])
    if options =="Sorted by Order of Expend  !!!":
        st.subheader("Sorted by Order of Expend  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[0]),reverse = b) # Order of Expend sort , int
        return a
        

    elif options == "Sorted by Club sort  !!!":
        st.subheader("Sorted by Club sort  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[1]),reverse = b) # Club sort , str
        return a
            
        
    elif options == "Sorted by State sort  !!! ":
        st.subheader("Sorted by State sort  !!! ")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[2]),reverse = b) # State sort , str
        return a
            

    elif options == "Sort data BY Competition":
        st.subheader("Sort data BY Competition")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: str(DFN[3]),reverse = b) # Competition sort , str
        return a

    elif options == "Sorted by Expenditures  !!!":
        st.subheader("Sorted by Expenditures  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[4]),reverse = b) # Expenditures sort , float
        return a

    elif options == "Sorted by Income  !!!":
        st.subheader("Sorted by Income  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[5]),reverse = b) # Income sort , float
        return a

    elif options == "Sorted by Arrivals  !!!":
        st.subheader("Sorted by Arrivals  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[6]),reverse = b) # Arrivals sort , int
        return a

    elif options == "Sorted by Departures  !!!":
        st.subheader("Sorted by Departures  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: int(DFN[7]),reverse = b) # Departures sort , int
        return a

    elif options == "Sorted by Balance sort !!!":
        st.subheader("Sorted by Balance sort !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[8]),reverse = b) # Balance sort ,float
        return a

    elif options == "Sorted by inflation calculate on Expenditure sort  !!!":
        st.subheader("Sorted by inflation calculate on Expenditure sort  !!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[9]),reverse = b) # inflation calculate on Expenditure sort ,float
        return a

    elif options == "Sort data BY inflation calculate on Income":
        st.subheader("Sort data BY inflation calculate on Income")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[10]),reverse = b) # inflation calculate on Income sort ,float
        return a
    
    elif options == "Sorted by inflation calculate on Balance sort  !!!":
        st.subheader("Sorted by inflation calculate on Balance sort  !!!!")
        b = Chose_sort()
        a =  sorted(DFN, key=lambda DFN: float(DFN[11]),reverse = b) # inflation calculate on Balance sort ,float
        return a
    

def DCTAS_MAIN(DFrame):
    # DataFrame to ecstract data
    nDFRAME = DCTAS_base(DFrame)

    #count number of rows in date frame
    count = NumberOfRows(nDFRAME)


    #reserving the number of elements in a row
    Order_of_Expend  = [0] * count # indx 0
    Club = [0] * count # indx 1
    State = [0] * count # indx 2
    Competition =  [0] * count # indx 3
    Expenditures = [0] * count # indx 4
    Income = [0] * count # indx 5
    Arrivals = [0] * count # indx 6
    Departures = [0] * count # indx 7
    Balance =  [0] * count # indx 8
    inflation_Expenditure = [0] * count # indx 9
    inflation_Income = [0] * count # indx 10
    inflation_Balance =  [0] * count # indx 11


    # cast DataFrame rows to folat and int
    nDFRAME["Order_of_Expend"].astype(np.int)# ind 0
    nDFRAME["Club"].astype(np.str)# ind 1
    nDFRAME["State"].astype(np.str)# ind 2
    nDFRAME["Competition"].astype(np.str)# ind 3
    nDFRAME["Expenditures"].astype(np.float)# ind 4
    nDFRAME["Income"].astype(np.float)# ind 5
    nDFRAME["Arrivals"].astype(np.int)# ind 6
    nDFRAME["Departures"].astype(np.int)# ind 7
    nDFRAME["Balance"].astype(np.float)# ind 8
    nDFRAME["inflation_Expenditure"].astype(np.float)# ind 9
    nDFRAME["inflation_Income"].astype(np.float)# ind 10
    nDFRAME["inflation_Balance"].astype(np.float)# ind 11
    ###############################################################################

    #save values from the dateframe to a arrays
    i = 0
    for i in range(0,count):
        Order_of_Expend[i] =  nDFRAME["Order_of_Expend"][i] # indx 0
        Club[i] = nDFRAME["Club"][i] # indx 1
        State[i] = nDFRAME["State"][i] # indx 2
        Competition[i] = nDFRAME["Competition"][i] # indx 3
        Expenditures[i] = nDFRAME["Expenditures"][i] # indx 4
        Income[i] = nDFRAME["Income"][i] # indx 5
        Arrivals[i] = nDFRAME["Arrivals"][i] # indx 6
        Departures[i] = nDFRAME["Departures"][i] # indx 7
        Balance[i] = nDFRAME["Balance"][i] # indx 8
        inflation_Expenditure[i] = nDFRAME["inflation_Expenditure"][i] # indx 9
        inflation_Income[i] = nDFRAME["inflation_Income"][i] # indx 10
        inflation_Balance[i] = nDFRAME["inflation_Balance"][i] # indx 11
        ###############################################################################

    # conversion to numpy
    np_Order_of_Expend = np.asarray(Order_of_Expend, dtype = 'int') # indx 0
    np_Club = np.asarray(Club,dtype='str')# indx 1
    np_State = np.asarray(State,dtype='str')# indx 2
    np_Competition = np.asarray(Competition, dtype = 'str') # indx 3
    np_Expenditures = np.asarray(Expenditures,dtype='float') # indx 4
    np_Income = np.asarray(Income, dtype ='float') # indx 5
    np_Arrivals = np.asarray(Arrivals,dtype='int') # indx 6
    np_Departures = np.asarray(Departures, dtype = 'int' ) # indx 7
    np_Balance = np.asarray(Balance,dtype='float') # indx 8
    np_inflation_Expenditure = np.asarray(inflation_Expenditure, dtype = 'float' ) # indx 9
    np_inflation_Income = np.asarray(inflation_Income, dtype = 'float' ) # indx 10
    np_inflation_Balance = np.asarray(inflation_Balance, dtype = 'float' ) # indx 11
    ###############################################################################

    # set the numpy arrays values into stack
    a = np.stack((np_Order_of_Expend,np_Club,np_State,np_Competition,np_Expenditures,np_Income,np_Arrivals,np_Departures,
    np_Balance,np_inflation_Expenditure,np_inflation_Income,np_inflation_Balance),axis= -1)
    ###############################################################################

    # convert from stack with values to data for dataFrame
    a_data = np.array(a)
    # set to DataFrame
    df_a = pd.DataFrame(a_data)
    # name of labels for head or names of collums
    df_a.columns = ["Order_of_Expend","Club","State","Competition","Expenditures",
                             "Income","Arrivals","Departures","Balance",
                             "inflation_Expenditure","inflation_Income","inflation_Balance"]
    ###############################################################################

    # convert data from numpay ndarray to list and remove duplicates elemtes of list for states
    listSTATE = np_State.tolist()
    listSTATE = remove_duplicates(listSTATE)

    # convert data from numpay ndarray to list and remove duplicates elemtes of list for Competition
    listCompetition = np_Competition.tolist()
    listCompetition = remove_duplicates(listCompetition)
    ###############################################################################

    # a function in which a user selects a choice of country or championship,
    # and chooses the name of the state or championship after which the data is printed

    # temporary variables that note the value the ticker chooses
    flag = 0
    remm = 0
    flagTemp = '0'
    task = st.selectbox("Chose a option of proces ",["State !","Competition !"],key='key_options')

    if task == "State !":
        flag_option = "State"
        flag = 1
        cont_state = 0
        
        st.write("Enter Club ")
        for i in range(0,len(listSTATE)):
            cont_state += 1
        options = ['0'] * cont_state
        
        for i in range(0,len(listSTATE)):
            options[i] = listSTATE[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listSTATE)):
            if listSTATE[i] == remeber:
                break
            cnt +=1

    elif task == "Competition !":
        flag_option = "Competition"
        flag = 2
        cont_Compe = 0
        
        st.write("Enter Club ")
        for i in range(0,len(listCompetition)):
            cont_Compe += 1
        options = ['0'] * cont_Compe
        
        for i in range(0,len(listCompetition)):
            options[i] = listCompetition[i]

        remeber = st.selectbox("Select Dynamic", options= list(options))
        #st.write("Added ",remeber)
        remm = remeber
        flagTemp = remeber
        cnt = 1
        for i in range(0,len(listCompetition)):
            if listCompetition[i] == remeber:
                break
            cnt +=1

    #count number of rows in date frame
    count = NumberOfRows(nDFRAME)

    # temp var for count number of roew for dynamic reserving
    bro = 0

    # count number of rows in date frame
    if flag == 1:
        for i in range(0,len(a)):
            if str(a[i][2]) == flagTemp :
                bro +=1
    ###############################################################################
    # count number of rows in date frame
    if flag == 2:
        for i in range(0,len(a)):
            if str(a[i][3]) == flagTemp :
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
    ###############################################################################

    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from State user chose options
    y = 0
    if flag == 1:
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
                y+=1
    ###############################################################################

    # temporarily storing data from a numpy array into a
    # common array to allocate as many places as you need to avoid empty places in the DataFrame
    # storing data from Competition user chose options
    if flag == 2:
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
                y+=1
    ###############################################################################

    # reserving the number of elements in a row
    niz_N1 = [0]*bro
    #Initialize a new array
    np_niz1 = np.asarray(niz_N1, dtype = 'str')
    np_niz2 = np.asarray(niz_N1, dtype = 'int64')
    np_niz3 = np.asarray(niz_N1, dtype = 'float64')

    #set arr to stack for operations with data lik sort and convert
    new_niz = np.stack((np_niz2,np_niz1,np_niz1,np_niz1,np_niz3,np_niz3,np_niz2,np_niz2,np_niz3,np_niz3,np_niz3,np_niz3),axis= -1)
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
        y+=1
    ###############################################################################

    # convert from stack with values to data for dataFrame
    new_data = np.array(new_niz)
    # set to DataFrame
    df_new = pd.DataFrame(new_data)
    # name of labels for head or names of collums
    df_new.columns = ["Order_of_Expend","Club","State","Competition","Expenditures",
                             "Income","Arrivals","Departures","Balance",
                             "inflation_Expenditure","inflation_Income","inflation_Balance"]
    return df_new,remm,flag_option
