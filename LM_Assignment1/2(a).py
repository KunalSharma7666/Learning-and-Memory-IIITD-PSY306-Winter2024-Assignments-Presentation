import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import scipy.stats as stats


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
    Mean = [0,0,0]
    Error = [0,0,0]

    Mean[0] = np.mean(d_Prime[0]) # Mean for setSize 4
    Error[0] = np.std(d_Prime[0]) / np.sqrt(len(d_Prime[0])) #Standard error for setSize 4
    Mean[1] = np.mean(d_Prime[1]) # Mean for setSize 6
    Error[1] = np.std(d_Prime[1]) / np.sqrt(len(d_Prime[1])) #Standard error for setSize 6
    Mean[2] = np.mean(d_Prime[2]) # Mean for setSize 8
    Error[2] = np.std(d_Prime[2]) / np.sqrt(len(d_Prime[2])) #Standard error for setSize 8

    print(f"Average d_prime: {Mean}")
    print(f"Standard Error: {Error}")
    # Plotting the graph
    plt.bar(['4', '6', '8'], Mean, yerr=Error, capsize=5, width=0.4)
    plt.xlabel('setSize')
    plt.ylabel('d_Prime mean')
    plt.title('d_Prime mean across all set sizes')
    plt.show()