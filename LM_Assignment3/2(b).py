import pandas
import numpy
from scipy import stats

# List contaning interstimulus Interstimulus_Intervals
Interstimulus_Intervals = [0.75, 1.5, 3, 8, 9]

var=0
# Loop through each interstimulus interval
index = 0
prev_p_value = None
prev_interval = None
var = 0
while index < len(Interstimulus_Intervals):
    interval = Interstimulus_Intervals[index]
    df = pandas.read_excel("LM_A3_Data2.xls", sheet_name=f"{interval}s", header=None)
    # Extracting EEG data for standard tones
    std_data = df.iloc[2:22, 1:101].to_numpy()
    # Extracting EEG data for deviant tones
    dev_data = df.iloc[24:44, 1:101].to_numpy()
    # Average EEG response across participants for standard tones
    Average_Standard = numpy.mean(std_data, axis=0)
    # Average EEG response across participants for deviant tones
    Average_Deviant = numpy.mean(dev_data, axis=0)
    # Paired t-test for every individual time point
    t_statistic, p_values = stats.ttest_rel(Average_Standard, Average_Deviant, axis=0)
    print(f"Interstimulus Interval: {interval}s, p-value: {p_values}")
    # Finding range where the p-value transitions from significant to non-significant
    if p_values > 0.05 and var == 0:
        ans = f"Echoic Memory Time Scale: {interval}s"
        var=1
    index += 1

# Printing the Calculated Echoic Memory Time Scale
print(ans)    
