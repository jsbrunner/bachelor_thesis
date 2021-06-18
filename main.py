import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from plots import plot_xvah

# count number and length of slices within the aggregated data set
df_count = pd.read_csv('aggregated_data.csv', low_memory=False)

# number and driving distance of the response time estimation slices
df_count_rt = df_count[df_count['rt'] == 1]
runs_rt = df_count_rt['code'].unique()
runs_rt = np.delete(runs_rt, [1, 13, 21, 22, 26, 27])  # runs excluded due to bad response time recognition
dist_rt = 0
for i in runs_rt:
    df_count_rt_temp = df_count_rt[df_count_rt['code'] == i]
    dist_rt += df_count_rt_temp['len_dist'].iloc[0]

# number of slices used to observe the string stability
df_count_ss = df_count[df_count['rt'] == 1]
runs_ss = df_count_ss['code'].unique()

# number of slices and driving distance for headway estimation
df_count_hw = df_count[df_count['hw'] == 1]
runs_hw = df_count_hw['code'].unique()
dist_hw = 0
for i in runs_hw:
    df_count_hw_temp = df_count_hw[df_count_hw['code'] == i]
    dist_hw += df_count_hw_temp['len_dist'].iloc[0]

# number of slices and driving distance for energy consumtion comparison
df_count_ec = df_count[df_count['ec'].isin(['A', 'B', 'C'])]
runs_ec = df_count_ec['code'].unique()
runs_ec = np.delete(runs_ec, [6])
dist_ec = 0
for i in runs_ec:
    df_count_ec_temp = df_count_ec[df_count_ec['code'] == i]
    dist_ec += df_count_ec_temp['len_dist'].iloc[10]

print('\nRuns response time: ' + str(len(runs_rt)) + ', Distance: ' + str(dist_rt) + ' m',
      '\nRuns headway: ' + str(len(runs_hw)) + ', Distance: ' + str(dist_hw) + ' m',
      '\nRuns string stability: ' + str(len(runs_ss)),
      '\nRuns energy consumption: ' + str(len(runs_ec)) + ', Distance: ' + str(dist_ec) + ' m')


df = pd.read_csv('aggregated_data.csv', low_memory=False)
df = df[df['campaign'] == 'CARMA2']
df = df[df['rt'] == 1]
runs = df['code'].unique()
for i in runs:
    df_temp = df[df['code'] == i]
    plot_xvah(df_temp, i)
plt.show()


