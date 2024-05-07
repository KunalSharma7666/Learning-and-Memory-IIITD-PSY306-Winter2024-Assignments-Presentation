

import pandas
import numpy
import matplotlib.pyplot as plot

# Creates a figure with 5 subplots - Here No. of Rows = 5 and No. of Column = 1
Img, subImg = plot.subplots(5, 1, figsize=(8, 16))

i = 1
while i < 6:  # Loop to iterate on participant numbers

    # Reading the sheet
    Data_Frame = pandas.read_excel("LM_A3_Data1.xlsx", sheet_name=f"Sheet{i}", header=None)

    # Calculating the distance from the most recently recalled item for each trial
    dist = []
    j = 0
    while j < len(Data_Frame):
        row = Data_Frame.iloc[j]
        temp = 0
        k = 0
        while k < len(row):
            item = row[k]
            if item > 0:
                if temp > 0:
                    dist.append(abs(item - temp))
            temp = item                                    
            k += 1
        j += 1

    # Data generation for the histogram.
    bins = numpy.arange(0, numpy.max(dist) + 2)
    Data, var = numpy.histogram(dist, bins=bins)

    # Plotting for each participant
    subImg[i - 1].bar(range(0, len(Data)), Data, align='center')
    subImg[i - 1].grid(True)
    subImg[i - 1].set_xticks(range(0, len(Data)))
    subImg[i - 1].set_title(f'Participant {i}')
    subImg[i - 1].set_xlabel('Distance from the most recently recalled item')
    subImg[i - 1].set_ylabel('Frequency')
    i+=1

# Title
Img.suptitle('Variation in the distribution of distances from the last recalled item among participants')

plot.subplots_adjust(hspace=0.5,top=0.94)
plot.show()

