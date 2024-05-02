import numpy as np
import scipy.io
import scipy.stats as stats
import pandas as pd
import pingouin as pg

def helper():
    i = 0
    while i < len(Subjects):   # Calculating d_Prime of each participant
        Subject = Subjects[i]
        # Adding data in different 2D arrays
        Change = Data_file[Subject]['change'][0][0]
        Accuracy = Data_file[Subject]['accuracy'][0][0]
        setSize = Data_file[Subject]['setSize'][0][0]
        Number_of_hits = [0,0,0]
        False_alarms = [0,0,0]
        Change_1 = [0,0,0]
        Change_0 = [0,0,0]
        j = 0
        while j < 192:         # Calculating d_Prime of a participant for 4,6 and 8 set size.
            temp1 = j//4
            temp2 = j%4
            if Change[temp1][temp2] == 1 and setSize[temp1][temp2] == 4:
                Change_1[0] +=1
            elif Change[temp1][temp2] == 0 and setSize[temp1][temp2] == 4:
                Change_0[0] +=1
            elif Change[temp1][temp2] == 1 and setSize[temp1][temp2] == 6:
                Change_1[1] +=1
            elif Change[temp1][temp2] == 0 and setSize[temp1][temp2] == 6:
                Change_0[1] +=1
            elif Change[temp1][temp2] == 1 and setSize[temp1][temp2] == 8:
                Change_1[2] +=1
            elif Change[temp1][temp2] == 0 and setSize[temp1][temp2] == 8:
                Change_0[2] +=1
            if Change[temp1][temp2] == 0 and Accuracy[temp1][temp2] == 0 and setSize[temp1][temp2] == 4:
                False_alarms[0] += 1
            elif Change[temp1][temp2] == 1 and Accuracy[temp1][temp2] == 1 and setSize[temp1][temp2] == 4:
                Number_of_hits[0] += 1
            elif Change[temp1][temp2] == 0 and Accuracy[temp1][temp2] == 0 and setSize[temp1][temp2] == 6:
                False_alarms[1] += 1
            elif Change[temp1][temp2] == 1 and Accuracy[temp1][temp2] == 1 and setSize[temp1][temp2] == 6:
                Number_of_hits[1] += 1
            elif Change[temp1][temp2] == 0 and Accuracy[temp1][temp2] == 0 and setSize[temp1][temp2] == 8:
                False_alarms[2] += 1
            elif Change[temp1][temp2] == 1 and Accuracy[temp1][temp2] == 1 and setSize[temp1][temp2] == 8:
                Number_of_hits[2] += 1
            
            j += 1
        
        k = 0
        while(k<=2): # Appending the d prime value into an array named d_Prime 
            d_Prime[k].append(stats.norm.ppf(Number_of_hits[k]/Change_1[k]) - stats.norm.ppf(False_alarms[k]/Change_0[k])) 
            k+=1
        i+=1
    
    return d_Prime

if __name__=="__main__": 
    
    # Loading data from the .mat file
    Data_file = scipy.io.loadmat('LM_A1_data.mat')

    # Taking participant keys
    Subjects = [f'p{i}' for i in range(1, 18)]

    d_Prime = [[],[],[]]

    helper()

    d_Primes = d_Prime[0] + d_Prime[1] + d_Prime[2]  # Merging the d_Primes lists.
    
    setSizes = [4,6,8]
    setSizes = np.repeat(setSizes, 17)
    setSizes = setSizes.tolist()
    array = np.tile(Subjects, 3)  # Copy the list three times
    participants = array.tolist() # Convert the resulting array back to a list

    data_frame = pd.DataFrame({'Participant': participants, 'Set Size': setSizes, 'd_Prime': d_Primes})
    print(data_frame)
    print(d_Primes)
    # Performing Mauchly's test to check assumption of sphericity
    result1 = pg.sphericity(data=data_frame, dv='d_Prime', subject='Participant', within='Set Size')[-1]
    print(f"Mauchly's Test Results: \np-value = {result1}")

    # Performing Shapiro-Wilk's test to check assumption of Normality
    result2 = pg.normality(data=data_frame, dv='d_Prime', group='Set Size')
    print(f"Shapiro-Wilk's Test Results: \n{result2}")

    #Performing Levene's test to check assumption of Equal Variances 
    result3 = pg.homoscedasticity(data_frame, dv='d_Prime', group='Set Size')
    print(f"Levene's Test Results: {result3}")

    # #Repeated measures anova
    # result4 = pg.rm_anova(dv='d_Prime', within='Set Size', subject='Participant', data=data_frame, detailed=True)
    # print(f"Repeated Measures Anova Test Results: {result4}")

    # Friedman's test
    result4 = pg.friedman(data=data_frame, dv='d_Prime', within='Set Size', subject='Participant')
    print(f"Friedman's Test Results: {result4}")

    #Post_hocs - bonferroni test
    result5 = pg.pairwise_tests(dv='d_Prime', within='Set Size', subject='Participant', padjust='bonferroni', data=data_frame)
    print(f"Post Hocs Results: {result5}")