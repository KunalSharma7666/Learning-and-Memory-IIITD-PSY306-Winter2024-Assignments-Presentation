import pandas as pd
import pingouin as pg
import numpy as np
import scipy.io
import statsmodels.stats.multicomp as tu

def helper():
    i = 0
    while i < len(Subjects):   # Calculating correct trials of each participant
        Subject = Subjects[i]
        # Adding data in different 2D arrays
        Accuracy = Data_file[Subject]['accuracy'][0][0]
        setSize = Data_file[Subject]['setSize'][0][0]
        Correct_Trials = [0,0,0]
        Total_Trials = [0,0,0]
        j = 0
        while j < 192:         # Calculating correct trials of a participant for 4,6 and 8 set size. 
            if setSize[j//4][j%4] == 4:
                Total_Trials[0] += 1
            elif setSize[j//4][j%4] == 6:
                Total_Trials[1] += 1
            elif setSize[j//4][j%4] == 8:
                Total_Trials[2] += 1
            
            if Accuracy[j//4][j%4] == 1 and setSize[j//4][j%4] == 4:
                Correct_Trials[0] += 1
            elif Accuracy[j//4][j%4] == 1 and setSize[j//4][j%4] == 6:
                Correct_Trials[1] += 1
            elif Accuracy[j//4][j%4] == 1 and setSize[j//4][j%4] == 8:
                Correct_Trials[2] += 1
            j += 1
        
        
        k = 0
        while(k<=2):  # Appending the percentage into an array named correct
            Correct[k].append((Correct_Trials[k]/Total_Trials[k])*100) 
            k+=1
        i+=1
    
    return Correct



if __name__=="__main__": 
    
    # Loading data from the .mat file
    Data_file = scipy.io.loadmat('LM_A1_data.mat')

    # Taking participant keys
    Subjects = [f'p{i}' for i in range(1, 18)]
    Correct = [[],[],[]]
    helper()

    percentages = Correct[0] + Correct[1] + Correct[2]  # Merging the percentages lists.
    
    setSizes = [4,6,8]
    setSizes = np.repeat(setSizes, 17)
    setSizes = setSizes.tolist()
    array = np.tile(Subjects, 3)  # Copy the array three times
    participants = array.tolist() # Convert the resulting array back to a list

    data_frame = pd.DataFrame({'Participant': participants, 'Set Size': setSizes, 'Percentage': percentages})

    # Performing Mauchly's test to check assumption of sphericity
    result1 = pg.sphericity(data=data_frame, dv='Percentage', subject='Participant', within='Set Size')[-1]
    print(f"Mauchly's Test Results: \np-value = {result1}")

    # Performing Shapiro-Wilk's test to check assumption of Normality
    result2 = pg.normality(data=data_frame, dv='Percentage', group='Set Size')
    print(f"Shapiro-Wilk's Test Results: \n{result2}")

    #Performing Levene's test to check assumption of Equal Variances 
    result3 = pg.homoscedasticity(data_frame, dv='Percentage', group='Set Size')
    print(f"Levene's Test Results: {result3}")

    #Repeated measures anova
    result4 = pg.rm_anova(dv='Percentage', within='Set Size', subject='Participant', data=data_frame, detailed=True)
    print(f"Repeated Measures Anova Test Results: {result4}")

    # #Post_hocs
    # result5 = pg.pairwise_tests(dv='Percentage', within='Set Size', subject='Participant', padjust='bonferroni', data=data_frame)
    # print(f"Post Hocs Results: {result5}")

    # Post_hocs - Tukey's test
    result5 = tu.MultiComparison(data_frame['Percentage'],data_frame['Set Size']).tukeyhsd()
    print(f"Tukey's test results: {result5}")