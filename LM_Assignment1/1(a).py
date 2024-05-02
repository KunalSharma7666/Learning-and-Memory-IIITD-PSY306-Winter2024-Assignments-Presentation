

import matplotlib.pyplot as plt
import numpy as np
import scipy.io


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
    Mean = [0,0,0]
    Error = [0,0,0]

    Mean[0] = np.mean(Correct[0]) # Mean for setSize 4
    Error[0] = np.std(Correct[0]) / np.sqrt(len(Correct[0])) #Standard error for setSize 4
    Mean[1] = np.mean(Correct[1]) # Mean for setSize 6
    Error[1] = np.std(Correct[1]) / np.sqrt(len(Correct[1])) #Standard error for setSize 6
    Mean[2] = np.mean(Correct[2]) # Mean for setSize 8
    Error[2] = np.std(Correct[2]) / np.sqrt(len(Correct[2])) #Standard error for setSize 8

    print(f"Mean percentages: {Mean}")
    print(f"Standard Errors: {Error}")
    # Plotting the graph
    plt.bar(['4', '6', '8'], Mean, yerr=Error, capsize=5, width=0.4)
    plt.xlabel('setSize')
    plt.ylabel('Mean percent of total correct trials')
    plt.title('Mean percent of total correct trials across all set sizes')
    plt.show()