import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians

pd.options.mode.chained_assignment = None


# function calculating the vehicle's tractive power and total enery consumption
def energy_consumption(df, m, f0, f1, f2, time, speed, acc, vehicles, name):
    total_energy = {}
    for i in vehicles:
        df['power{}'.format(i)] = 0.0
        for index, row in df.iterrows():
            a = row['{}{}'.format(acc, i)]
            v = row['{}{}'.format(speed, i)]
            power_temp = (f0 + f1*v + f2*v**2 + 1.03*m*a + m*9.81*0) * v * 0.001
            if power_temp >= 0:
                df.at[index, 'power{}'.format(i)] = power_temp
            else:
                df.at[index, 'power{}'.format(i)] = 0
        total_energy[i] = ((df['power{}'.format(i)].sum()*0.1)/(0.036*df['{}{}'.format(speed, i)].sum()*0.1))
    print('kWh/100km per vehicle ({}): '.format(name), total_energy)
    # return dataframe with tractive power and dict with energy consumption of the vehicles
    return df, total_energy


# load the aggregated data set
df = pd.read_csv('aggregated_data.csv', low_memory=False)
# rolling window for smoothing of tractive power in plots
rolling_window_size = 31

# comparison A
# select comparable slices
df_A = df[df['ec'] == 'A']
incl_runs = df_A['code'].unique()
df_A1 = df_A[df_A['code'] == incl_runs[0]]
df_A2 = df_A[df_A['code'] == incl_runs[1]]

# set time to start with at
df_A1['time'] = df_A1['time'] - df_A1['time'].iloc[0]
df_A2['time'] = df_A2['time'] - df_A2['time'].iloc[0]

# compute the tractive power and energy consumption for the slices
df_A1, total_energy_A1 = energy_consumption(df_A1, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_A1['mode'].iloc[0] + ': ' + df_A1['campaign'].iloc[0] + ' ' + df_A1['dataset'].iloc[0])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name
df_A2, total_energy_A2 = energy_consumption(df_A2, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_A2['mode'].iloc[0] + ': ' + df_A2['campaign'].iloc[0] + ' ' + df_A2['dataset'].iloc[0])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name

# plot the speed and tractive power for the comparison scenario
fig, ((ax3, ax1), (ax4, ax2), ) = plt.subplots(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle('Tractive Power (comparison A, AstaZero campaign)', y=0.98, fontsize='x-large')
linewidth = 0.6

for i in ['L', '1', '2', '3', '4']:

    ax1.plot(df_A1['time'], df_A1['{}{}'.format('v', i)], label='speed of veh. {}'.format(i), linewidth=linewidth)
    [ax1.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [16.5, 25]]
    ax1.set_ylim(ymin=7, ymax=33)
    ax1.set_title('Mode: ' + df_A1['mode'].iloc[0])
    df_A1['power{}'.format(i)] = df_A1['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax2.plot(df_A1['time'], df_A1['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylim(ymin=-3, ymax=63)

    ax3.plot(df_A2['time'], df_A2['{}{}'.format('v', i)], label='vehicle {}'.format(i), linewidth=linewidth)
    [ax3.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [16.5, 25]]
    ax3.set_ylabel('Speed (m/s)')
    ax3.set_ylim(ymin=7, ymax=33)
    ax3.set_title('Mode: ' + df_A2['mode'].iloc[0])
    df_A2['power{}'.format(i)] = df_A2['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax4.plot(df_A2['time'], df_A2['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    ax4.set_ylabel('Tractive power (kW)')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylim(ymin=-3, ymax=63)

ax3.legend(fontsize='x-small')

fig.savefig('plots' + '/' + 'ec' + '/' + 'ec_comparison_A.png', dpi=300, format='png')

# same procedure for the following comparisons
# comparison B
df_B = df[df['ec'] == 'B']
incl_runs = df_B['code'].unique()
df_B1 = df_B[df_B['code'] == incl_runs[0]]
df_B2 = df_B[df_B['code'] == incl_runs[1]]
df_B1['time'] = df_B1['time'] - df_B1['time'].iloc[0]
df_B2['time'] = df_B2['time'] - df_B2['time'].iloc[0]

df_B1, total_energy_B1 = energy_consumption(df_B1, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_B1['mode'].iloc[0] + ': ' + df_B1['campaign'].iloc[0] + ' ' + df_B1['dataset'].iloc[0])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name
df_B2, total_energy_B2 = energy_consumption(df_B2, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_B2['mode'].iloc[0] + ': ' + df_B2['campaign'].iloc[0] + ' ' + df_B2['dataset'].iloc[0])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name

fig, ((ax3, ax1), (ax4, ax2), ) = plt.subplots(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle('Tractive Power (comparison B, AstaZero campaign)', y=0.98, fontsize='x-large')
linewidth = 0.6

for i in ['L', '1', '2', '3', '4']:

    ax1.plot(df_B1['time'], df_B1['{}{}'.format('v', i)], label='speed of veh. {}'.format(i), linewidth=linewidth)
    [ax1.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [13.6, 27.5]]
    # ax1.set_ylabel('Speed [m/s]')
    ax1.set_ylim(ymin=7, ymax=36)
    ax1.set_title('Mode: ' + df_B1['mode'].iloc[0])
    df_B1['power{}'.format(i)] = df_B1['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax2.plot(df_B1['time'], df_B1['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    # ax2.set_ylabel('Tractive power [kW]')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylim(ymin=-3, ymax=80)

    ax3.plot(df_B2['time'], df_B2['{}{}'.format('v', i)], label='vehicle {}'.format(i), linewidth=linewidth)
    [ax3.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [13.6, 27.5]]
    ax3.set_ylabel('Speed (m/s)')
    ax3.set_ylim(ymin=7, ymax=36)
    ax3.set_title('Mode: ' + df_B2['mode'].iloc[0])
    df_B2['power{}'.format(i)] = df_B2['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax4.plot(df_B2['time'], df_B2['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    ax4.set_ylabel('Tractive power (kW)')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylim(ymin=-3, ymax=80)

ax3.legend(fontsize='x-small')

fig.savefig('plots' + '/' + 'ec' + '/' + 'ec_comparison_B.png', dpi=300, format='png')


# comparison C
df_C = df[df['ec'] == 'C']
incl_runs = df_C['code'].unique()
df_C1 = df_C[df_C['code'] == incl_runs[1]]
df_C2 = df_C[df_C['code'] == incl_runs[0]]
df_C1['time'] = df_C1['time'] - df_C1['time'].iloc[0]
df_C2['time'] = df_C2['time'] - df_C2['time'].iloc[0]

df_C1, total_energy_C1 = energy_consumption(df_C1, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_C1['mode'].iloc[0] + ': ' + df_C1['campaign'].iloc[0] + ' ' + df_C1['dataset'].iloc[0])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name
df_C2, total_energy_C2 = energy_consumption(df_C2, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_C2['mode'].iloc[0] + ': ' + df_C2['campaign'].iloc[0] + ' ' + df_C2['dataset'].iloc[0])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name

fig, ((ax3, ax1), (ax4, ax2), ) = plt.subplots(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle('Tractive Power (comparison C, CARMA1 campaign)', y=0.98, fontsize='x-large')
linewidth = 0.6

for i in ['L', '1', '2', '3', '4']:

    ax1.plot(df_C1['time'], df_C1['{}{}'.format('v', i)], label='speed of veh. {}'.format(i), linewidth=linewidth)
    [ax1.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [19.7, 26.2]]
    # ax1.set_ylabel('Speed [m/s]')
    ax1.set_ylim(ymin=12, ymax=32)
    ax1.set_title('Mode: ' + df_C1['mode'].iloc[0] + ' (CARMA1)')
    df_C1['power{}'.format(i)] = df_C1['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax2.plot(df_C1['time'], df_C1['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    # ax2.set_ylabel('Tractive power [kW]')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylim(ymin=-3, ymax=60)

    ax3.plot(df_C2['time'], df_C2['{}{}'.format('v', i)], label='vehicle {}'.format(i), linewidth=linewidth)
    [ax3.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [19.7, 26.2]]
    ax3.set_ylabel('Speed (m/s)')
    ax3.set_ylim(ymin=12, ymax=32)
    ax3.set_title('Mode: ' + df_C2['mode'].iloc[0])
    df_C2['power{}'.format(i)] = df_C2['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax4.plot(df_C2['time'], df_C2['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    ax4.set_ylabel('Tractive power (kW)')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylim(ymin=-3, ymax=60)

ax3.legend(fontsize='x-small')

fig.savefig('plots' + '/' + 'ec' + '/' + 'ec_comparison_C.png', dpi=300, format='png')


# comparison C_
df_C_ = df[df['ec'] == 'C']
incl_runs = df_C_['code'].unique()
df_C1_ = df_C_[df_C_['code'] == incl_runs[1]]
df_C2_ = df_C_[df_C_['code'] == incl_runs[2]]
df_C1_['time'] = df_C1_['time'] - df_C1_['time'].iloc[0]
df_C2_['time'] = df_C2_['time'] - df_C2_['time'].iloc[0]

df_C2_ = df_C2_.drop(df_C2_[(df_C2_['time'] > 104.5) & (df_C2_['time'] < 125.5)].index)
df_C2_.iloc[1046:]['time'] = df_C2_.iloc[1046:]['time'] - 21

df_C1_, total_energy_C1_ = energy_consumption(df_C1_, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_C1_['mode'].iloc[50] + ': ' + df_C1_['campaign'].iloc[50] + ' ' + df_C1_['dataset'].iloc[50])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name
df_C2_, total_energy_C2_ = energy_consumption(df_C2_, 1560, 213, 0.31, 0.035, 'time', 'v', 'a', ['L', '1', '2', '3', '4'], df_C2_['mode'].iloc[50] + ': ' + df_C2_['campaign'].iloc[50] + ' ' + df_C2_['dataset'].iloc[50])  # dataframe, mass, f0, f1, f2, time-column name, speed-column name, acceleration-column name, vehicles list, name

fig, ((ax3, ax1), (ax4, ax2), ) = plt.subplots(2, 2)
fig.set_size_inches(10, 6)
fig.suptitle('Tractive Power (comparison C+, CARMA1 and CARMA2 campaigns)', y=0.98, fontsize='x-large')
linewidth = 0.6

for i in ['L', '1', '2', '3', '4']:

    ax1.plot(df_C1_['time'], df_C1_['{}{}'.format('v', i)], label='speed of veh. {}'.format(i), linewidth=linewidth)
    [ax1.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [19.7, 26.2]]
    # ax1.set_ylabel('Speed [m/s]')
    ax1.set_ylim(ymin=12, ymax=32)
    ax1.set_title('Mode: ' + df_C1_['mode'].iloc[0] + ' (CARMA1)')
    df_C1_['power{}'.format(i)] = df_C1_['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax2.plot(df_C1_['time'], df_C1_['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    # ax2.set_ylabel('Tractive power [kW]')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylim(ymin=-3, ymax=60)

    ax3.plot(df_C2_['time'], df_C2_['{}{}'.format('v', i)], label='vehicle {}'.format(i), linewidth=linewidth)
    [ax3.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [19.7, 26.2]]
    ax3.set_ylabel('Speed (m/s)')
    ax3.set_ylim(ymin=12, ymax=32)
    ax3.set_title('Mode: ' + df_C2_['mode'].iloc[0] + ' (CARMA2)')
    df_C2_['power{}'.format(i)] = df_C2_['power{}'.format(i)].rolling(window=rolling_window_size, center=True).mean()
    ax4.plot(df_C2_['time'], df_C2_['power{}'.format(i)], label='power of veh. {}'.format(i), linewidth=linewidth)
    ax4.set_ylabel('Tractive power (kW)')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylim(ymin=-3, ymax=60)

ax3.legend(fontsize='x-small')

fig.savefig('plots' + '/' + 'ec' + '/' + 'ec_comparison_C+.png', dpi=300, format='png')


# create lists for the violin plot
energy_A1_list, energy_A2_list, energy_B1_list, energy_B2_list, energy_C1_list, energy_C2_list, energy_C1__list, energy_C2__list = \
    [], [], [], [], [], [], [], []

for i in total_energy_A1:
    energy_A1_list.append(total_energy_A1[i])
for i in total_energy_A2:
    energy_A2_list.append(total_energy_A2[i])
for i in total_energy_B1:
    energy_B1_list.append(total_energy_B1[i])
for i in total_energy_B2:
    energy_B2_list.append(total_energy_B2[i])
for i in total_energy_C1:
    energy_C1_list.append(total_energy_C1[i])
for i in total_energy_C2:
    energy_C2_list.append(total_energy_C2[i])
for i in total_energy_C1_:
    energy_C1__list.append(total_energy_C1_[i])
for i in total_energy_C2_:
    energy_C2__list.append(total_energy_C2_[i])

# create nested lists
list_combined_A = [energy_A1_list, energy_A2_list]
list_combined_B = [energy_B1_list, energy_B2_list]
list_combined_C = [energy_C2_list, energy_C1_list, energy_C2__list]

# violin plot
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
zord = 1000
ylim = [7, 15]
ylim1 = [7, 9.5]
hlines = [8, 9, 10, 11, 12, 13, 14]
axistitle_size = 'medium'
marker = "o"
fig, (axA, axB, axC) = plt.subplots(1, 3, gridspec_kw={'width_ratios': [2, 2, 3]})
fig.set_size_inches(9, 6)
fig.suptitle('Tractive Energy Consumption', y=0.98, fontsize='x-large')

axA.set_title('AstaZero\n(16.4 m/s - 25 m/s)', fontsize=axistitle_size)
axA.set_ylim(ylim)
axA.violinplot(list_combined_A, widths=0.5, showextrema=False)
axA.scatter([1, 1, 1, 1, 1], energy_A1_list, c=colors, zorder=zord, marker=marker)
axA.scatter([2, 2, 2, 2, 2], energy_A2_list, c=colors, zorder=zord, marker=marker)
axA.set_xticks([1, 2])
axA.set_xticklabels([df_A1['mode'].iloc[0], df_A2['mode'].iloc[0]])
axA.set_ylabel('Tractive energy consumption (kWh/100km)')
[axA.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in hlines]

axB.set_title('AstaZero\n(13.6 m/s - 27.5 m/s)', fontsize=axistitle_size)
axB.set_ylim(ylim)
axB.violinplot(list_combined_B, widths=0.5, showextrema=False)
axB.scatter([1, 1, 1, 1, 1], energy_B1_list, c=colors, zorder=zord, marker=marker)
axB.scatter([2, 2, 2, 2, 2], energy_B2_list, c=colors, zorder=zord, marker=marker)
axB.set_xticks([1, 2])
axB.set_xticklabels([df_B1['mode'].iloc[0], df_B2['mode'].iloc[0]])
axB.set_yticks([])
[axB.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in hlines]

axC.set_title('CARMA1 and CARMA2\n(19.6 m/s - 26.2 m/s)', fontsize=axistitle_size)
axC.set_ylim(ylim1)
axC.violinplot(list_combined_C, widths=0.5, showextrema=False)
axC.scatter([1, 1, 1, 1, 1], energy_C2_list, c=colors, zorder=zord, marker=marker)
axC.scatter([2, 2, 2, 2, 2], energy_C1_list, c=colors, zorder=zord, marker=marker)
axC.scatter([3, 3, 3, 3, 3], energy_C2__list, c=colors, zorder=zord, marker=marker)
axC.set_xticks([1, 2, 3])
axC.set_xticklabels([df_C2['mode'].iloc[0] + '\nCARMA1', df_C1['mode'].iloc[0] + '\nCARMA1', df_C2_['mode'].iloc[0] + '\nCARMA2'])
[axC.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in hlines]

fig.tight_layout(pad=2)

fig.savefig('plots' + '/' + 'ec' + '/' + 'ec_violinplot.png', dpi=300, format='png')
