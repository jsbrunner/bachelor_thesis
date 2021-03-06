import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians
from plots import plot_xvah

pd.set_option('display.max_columns', None)


# function reading data sets from the ZalaZone campaign
def read_zalazone(filename, t_start, t_end):
    # handle head of data set
    rows_not_included = [0, 1, 2, 3, 4]
    df = pd.read_csv(filename, low_memory=False, skiprows=rows_not_included)

    # cut dataframe to start and end time
    df = df[df['Time'] < t_end]
    df = df[df['Time'] >= t_start]

    # rename columns
    df = df.rename(columns={"Speed1": "SpeedL", "Speed2": "Speed1", "Speed3": "Speed2", "Speed4": "Speed3", "Speed5": "Speed4"})

    # Calculate distance as sum of speeds
    df[["DistL", "Dist1", "Dist2", "Dist3", "Dist4"]] = df[["SpeedL", "Speed1", "Speed2", "Speed3", "Speed4"]].cumsum().multiply(0.1)

    # Smooth trajectories with lowesss (or rolling mean)
    list_vehicles = ['L', '1', '2', '3', '4']
    # for i in list_vehicles:
        # df["Dist{}_smoothed".format(i)] = lowess.lowess(df['Time'], df["Dist{}".format(i)], bandwidth=(1/df.shape[0])*10, polynomialDegree=1)  # bandwith makes the difference
    df[["DistL", "Dist1", "Dist2", "Dist3", "Dist4"]] = df[["DistL", "Dist1", "Dist2", "Dist3", "Dist4"]].rolling(window=21, center=True).mean()

    # Calculate Speeds
    # df[["SpeedL_smoothed", "Speed1_smoothed", "Speed2_smoothed", "Speed3_smoothed", "Speed4_smoothed"]] = df[["DistL_smoothed", "Dist1_smoothed", "Dist2_smoothed", "Dist3_smoothed", "Dist4_smoothed"]].diff().multiply(10)
    df[["SpeedL", "Speed1", "Speed2", "Speed3", "Speed4"]] = df[["DistL", "Dist1", "Dist2", "Dist3", "Dist4"]].diff().multiply(10)

    # Calculate headway
    df['headway_L1'] = (df['IVS1'] + 5) / df['Speed1']
    df['headway_12'] = (df['IVS2'] + 5) / df['Speed2']
    df['headway_23'] = (df['IVS3'] + 5) / df['Speed3']
    df['headway_34'] = (df['IVS4'] + 5) / df['Speed4']

    # Calculate acceleration
    for i in list_vehicles:
        df['Acc{}'.format(i)] = df['Speed{}'.format(i)].diff().multiply(10)

    # drop unnecessary columns
    df = df[['Time', 'SpeedL', 'Speed1', 'Speed2', 'Speed3', 'Speed4', 'IVS1',
                     'IVS2', 'IVS3', 'IVS4', 'DistL', 'Dist1', 'Dist2', 'Dist3',
                     'Dist4', 'headway_L1', 'headway_12', 'headway_23',
                     'headway_34', 'AccL', 'Acc1', 'Acc2', 'Acc3', 'Acc4']]

    # rename columns to suit fixed pattern
    df = df.rename(columns={'Time': 'time', "SpeedL": "vL", "Speed1": "v1", "Speed2": "v2", "Speed3": "v3", "Speed4": "v4",
                            'IVS1': 'ivs1', 'IVS2': 'ivs2', 'IVS3': 'ivs3', 'IVS4': 'ivs4',
                            'DistL': 'xL', 'Dist1': 'x1', 'Dist2': 'x2', 'Dist3': 'x3',
                            'Dist4': 'x4', 'headway_L1': 'hL1', 'headway_12': 'h12', 'headway_23': 'h23', 'headway_34': 'h34', 'AccL': 'aL',
                            'Acc1': 'a1', 'Acc2': 'a2', 'Acc3': 'a3', 'Acc4': 'a4'})
    return df


# plot that compares the platoons stabiliy at perturbation events with different headway settings
rows_not_included = [0, 1, 2, 3, 4]
df_S = pd.read_csv('dynamic_part1.csv', low_memory=False, skiprows=rows_not_included)
df_M = pd.read_csv('dynamic_part9.csv', low_memory=False, skiprows=rows_not_included)
df_L = pd.read_csv('dynamic_part2.csv', low_memory=False, skiprows=rows_not_included)
# print(df_S.head(1), df_M.head(1), df_L.head(1))

vehicles = [1, 2, 3, 4, 5]  # data with S and L headway have a 6th vehicle

fig, (ax_s, ax_m, ax_l) = plt.subplots(1, 3)
fig.suptitle('Headway Setting Comparison (ZalaZone campaign)', y=0.98, fontsize='x-large')
fig.set_size_inches(10, 5)

upper_border = 380
lower_border = 300

df_S = df_S[df_S['Time'] < upper_border]
df_S = df_S[df_S['Time'] >= lower_border]
df_S['Time'] = df_S['Time'] - df_S['Time'].iloc[0]

df_M = df_M[df_M['Time'] < upper_border]
df_M = df_M[df_M['Time'] >= lower_border]
df_M['Time'] = df_M['Time'] - df_M['Time'].iloc[0]

df_L = df_L[df_L['Time'] < upper_border]
df_L = df_L[df_L['Time'] >= lower_border]
df_L['Time'] = df_L['Time'] - df_L['Time'].iloc[0]

linewidth = 0.6

for i in vehicles:
    ax_s.plot(df_S['Time'], df_S['Speed{}'.format(i)], label='Vehicle {}'.format(i), linewidth=linewidth)

for i in vehicles:
    ax_m.plot(df_M['Time'], df_M['Speed{}'.format(i)], label='Vehicle {}'.format(i), linewidth=linewidth)

for i in vehicles:
    ax_l.plot(df_L['Time'], df_L['Speed{}'.format(i)], label='Vehicle {}'.format(i), linewidth=linewidth)

ax_s.set_ylim(ymin=-0.5, ymax=16)
ax_m.set_ylim(ymin=-0.5, ymax=16)
ax_l.set_ylim(ymin=-0.5, ymax=16)

ax_s.set_title('Small headway setting')
ax_m.set_title('Medium headway setting')
ax_l.set_title('Large headway setting')

ax_s.set_ylabel('Speed (m/s)')
ax_s.set_xlabel('Time (s)')
ax_m.set_xlabel('Time (s)')
ax_l.set_xlabel('Time (s)')

ax_s.legend(fontsize='x-small', loc='lower right')

plt.tight_layout(pad=2)

fig.savefig('plots' + '/' + 'ss' + '/' + 'ss_headway_3_settings.png', dpi=300, format='png')
