

import pandas
import numpy
import matplotlib.pyplot as plot

# List contaning interstimulus Interstimulus_Intervals
Interstimulus_Intervals = [0.75, 1.5, 3, 8, 9]

# Creates a figure with 5 subplots - Here No. of Rows = 5 and No. of Column = 1
Img, subImg = plot.subplots(5, 1, figsize=(8, 16))

# Loop to iterate on each interstimulus interval
i = 0
while i < len(Interstimulus_Intervals):
    interval = Interstimulus_Intervals[i]
    if i == 0:
        sheet_name = "0.75s"
    elif i == 1:
        sheet_name = "1.5s"
    elif i == 2:
        sheet_name = "3s"
    elif i == 3:
        sheet_name = "8s"
    else:
        sheet_name = "9s"

    # Reading the sheet
    Data_Frame = pandas.read_excel("LM_A3_Data2.xls", sheet_name=sheet_name, header=None)

    # Retrieving EEG data corresponding to standard and deviant auditory stimuli
    std_data = Data_Frame.iloc[2:22, 1:101].to_numpy()  
    dev_data = Data_Frame.iloc[24:44, 1:101].to_numpy()  

    # Calculating the average EEG response across participants
    Average_Standard = numpy.mean(std_data, axis=0)
    Average_Deviant = numpy.mean(dev_data, axis=0)
    
    # Plotting average EEG response for standard and deviant tones
    subImg[i].plot(Average_Standard, color='blue', label='Standard Tone')
    subImg[i].plot(Average_Deviant, color='red', label='Deviant Tone')
    subImg[i].set_title(f'Interval: {interval} s')
    subImg[i].set_xlabel('Time Point')
    subImg[i].set_ylabel('EEG Response')
    subImg[i].legend()
    i += 1

# Set figure title
Img.suptitle('Average EEG Response for Standard and Deviant Tones')

plot.subplots_adjust(hspace=0.5,top=0.94)
plot.show()

