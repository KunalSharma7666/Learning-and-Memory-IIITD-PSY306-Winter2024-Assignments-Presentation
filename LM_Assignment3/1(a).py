

import pandas
import matplotlib.pyplot as plot


# Creates a figure with 5 subplots - Here No. of Rows = 5 and No. of Column = 1
Img, subImg = plot.subplots(5, 1, figsize=(8, 16))

i = 1
while i < 6:  # Loop to iterate on participant numbers
    
    # Reading the sheet
    Data_Frame = pandas.read_excel("LM_A3_Data1.xlsx", sheet_name=f"Sheet{i}", header=None)

    item_freq = [0] * 16  # List to store item frequencies

    index = 0
    # Loop to Iterate on each row in the DataFrame
    while index < len(Data_Frame):
        row = Data_Frame.iloc[index]  

        col_index = 0
        
        # Loop to Iterate on each item in the row
        while col_index < len(row):
            item = row[col_index]  
            
            if 0 < item <= 16:
                item_freq[item - 1] += 1  # Increment the corresponding frequency in item_freq
                
            col_index += 1 
            
        index += 1 

    # List of tuples for conversion to DataFrame
    freq_data = [(i + 1, freq) for i, freq in enumerate(item_freq)]  

    # Converting list of tuples to DataFrame
    freq_df = pandas.DataFrame(freq_data, columns=['Item', 'Frequency'])

    # Sorting DataFrame by item number
    freq_df.sort_values(by='Item', inplace=True)

    # Plotting for each participant
    subImg[i - 1].plot(freq_df['Item'], freq_df['Frequency'], marker='o', linestyle='-')
    subImg[i - 1].grid(True)
    subImg[i - 1].set_xticks(range(1, 17))
    subImg[i - 1].set_title(f'Participant {i}')
    subImg[i - 1].set_xlabel('Item Position')
    subImg[i - 1].set_ylabel('Recall Frequency') 
    i+=1

# Title
Img.suptitle("Participant's Frequency of Recalling Items")

plot.subplots_adjust(hspace=0.5,top=0.94)
plot.show()