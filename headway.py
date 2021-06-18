import pandas as pd
import matplotlib.pyplot as plt
from plots import plot_headway_const
from plots import plot_headway_pert
from plots import plot_headway_pert_up

pd.set_option('display.max_columns', None)

df = pd.read_csv('aggregated_data.csv', low_memory=False)


# function to compute the median headway between all successive vehicles in the platoon
def comp_hw(df):
    veh_hw = ['hL1', 'h12', 'h23', 'h34']
    if df['campaign'].iloc[0] == 'Napoli':
        veh_hw = ['hL1', 'h12', 'h23']
    hw_list = list()
    for i in veh_hw:
        hw_list.append(df[i].median())
    return hw_list

# compute headways for each mode and campaign and save them into lists
# AstaZero human
df_az_human = df[(df['campaign'] == 'AstaZero') & (df['mode'] == 'human')]
az_human_scatter_list = comp_hw(df_az_human)
az_human_violin_list = az_human_scatter_list

# Laval
df_laval = df[(df['campaign'] == 'Laval') & (df['mode'] == 'human')]
unique_data = df_laval['dataset'].unique()
laval_scatter_list = list()
for i in unique_data:
    df_temp = df_laval[df_laval['dataset'] == i]
    laval_scatter_list.append(comp_hw(df_temp))
laval_violin_list = [item for sublist in laval_scatter_list for item in sublist]

# Napoli
df_napoli = df[(df['campaign'] == 'Napoli') & (df['mode'] == 'human')]
unique_data = df_napoli['dataset'].unique()
napoli_scatter_list = list()
for i in unique_data:
    df_temp = df_napoli[df_napoli['dataset'] == i]
    napoli_scatter_list.append(comp_hw(df_temp))
napoli_violin_list = [item for sublist in napoli_scatter_list for item in sublist]

# AstaZero acc
df_az_acc = df[(df['campaign'] == 'AstaZero') & (df['mode'] == 'acc')]
az_acc_scatter_list = comp_hw(df_az_acc)
az_acc_violin_list = az_acc_scatter_list

# ZalaZone S-hw
df_zz_s = df[(df['campaign'] == 'ZalaZone') & (df['mode'] == 'acc') & (df['hw_set'] == 'S')]
unique_data = df_zz_s['dataset'].unique()
zz_s_scatter_list = list()
for i in unique_data:
    df_temp = df_zz_s[df_zz_s['dataset'] == i]
    zz_s_scatter_list.append(comp_hw(df_temp))
zz_s_violin_list = [item for sublist in zz_s_scatter_list for item in sublist]

# ZalaZone M-hw
df_zz_m = df[(df['campaign'] == 'ZalaZone') & (df['mode'] == 'acc') & (df['hw_set'] == 'M')]
unique_data = df_zz_m['dataset'].unique()
zz_m_scatter_list = list()
for i in unique_data:
    df_temp = df_zz_m[df_zz_m['dataset'] == i]
    zz_m_scatter_list.append(comp_hw(df_temp))
zz_m_violin_list = [item for sublist in zz_m_scatter_list for item in sublist]

# Zalazone L-hw
df_zz_l = df[(df['campaign'] == 'ZalaZone') & (df['mode'] == 'acc') & (df['hw_set'] == 'L')]
unique_data = df_zz_l['dataset'].unique()
zz_l_scatter_list = list()
for i in unique_data:
    df_temp = df_zz_l[df_zz_l['dataset'] == i]
    zz_l_scatter_list.append(comp_hw(df_temp))
zz_l_violin_list = [item for sublist in zz_l_scatter_list for item in sublist]

# CARMA1 acc
df_carma1_acc = df[(df['campaign'] == 'CARMA1') & (df['mode'] == 'acc')]
unique_data = df_carma1_acc['dataset'].unique()
carma1_acc_scatter_list = list()
for i in unique_data:
    df_temp = df_carma1_acc[df_carma1_acc['dataset'] == i]
    carma1_acc_scatter_list.append(comp_hw(df_temp))
carma1_acc_violin_list = [item for sublist in carma1_acc_scatter_list for item in sublist]

# CARMA1 cacc
df_carma1_cacc = df[(df['campaign'] == 'CARMA1') & (df['mode'] == 'cacc')]
unique_data = df_carma1_cacc['dataset'].unique()
carma1_cacc_scatter_list = list()
for i in unique_data:
    df_temp = df_carma1_cacc[df_carma1_cacc['dataset'] == i]
    carma1_cacc_scatter_list.append(comp_hw(df_temp))
carma1_cacc_violin_list = [item for sublist in carma1_cacc_scatter_list for item in sublist]

# CARMA2 cacc
df_carma2_cacc = df[(df['campaign'] == 'CARMA2') & (df['mode'] == 'cacc')]
unique_data = df_carma2_cacc['dataset'].unique()
carma2_cacc_scatter_list = list()
for i in unique_data:
    df_temp = df_carma2_cacc[df_carma2_cacc['dataset'] == i]
    carma2_cacc_scatter_list.append(comp_hw(df_temp))
carma2_cacc_violin_list = carma2_cacc_scatter_list[3]

# create a nested list for violin plot
list_combined = [laval_violin_list, napoli_violin_list, az_acc_violin_list, zz_s_violin_list, zz_m_violin_list,
                 zz_l_violin_list, carma1_acc_violin_list, carma1_cacc_violin_list, carma2_cacc_violin_list]

# figure with violin and scatterplots for headway
colors = ['tab:orange', 'tab:green', 'tab:red', 'tab:purple']
marker = 'o'
zord = 1000
fig, ax = plt.subplots()
fig.set_size_inches(9, 6)
fig.suptitle('Headway Comparison', y=0.98, fontsize='x-large')

ax.violinplot(list_combined, widths=0.5, showextrema=True)

# scatter not included in the final figure since it is confusing
'''
ax.scatter([1, 1, 1, 1], az_human_scatter_list, c=colors, zorder=zord, marker=marker)
for i in laval_scatter_list:
    ax.scatter([2, 2, 2, 2], i, c=colors, zorder=zord, marker=marker)
for i in napoli_scatter_list:
    ax.scatter([3, 3, 3], i, c=['tab:orange', 'tab:green', 'tab:red'], zorder=zord, marker=marker)
ax.scatter([4, 4, 4, 4], az_acc_scatter_list, c=colors, zorder=zord, marker=marker)
for i in zz_s_scatter_list:
    ax.scatter([5, 5, 5, 5], i, c=colors, zorder=zord, marker=marker)
for i in zz_m_scatter_list:
    ax.scatter([6, 6, 6, 6], i, c=colors, zorder=zord, marker=marker)
for i in zz_l_scatter_list:
    ax.scatter([7, 7, 7, 7], i, c=colors, zorder=zord, marker=marker)
for i in carma1_acc_scatter_list:
    ax.scatter([8, 8, 8, 8], i, c=colors, zorder=zord, marker=marker)
for i in carma1_cacc_scatter_list:
    ax.scatter([9, 9, 9, 9], i, c=colors, zorder=zord, marker=marker)
for i in [carma2_cacc_scatter_list[3]]:
    ax.scatter([10, 10, 10, 10], i, c=colors, zorder=zord, marker=marker)
'''

ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9])
ax.set_xticklabels(['Human driver\nLaval et al. 2014', 'Human driver\nPunzo et al. 2005', 'ACC\nAstaZero\nSmall headway',
                    'ACC\nZalaZone\nSmall headway', 'ACC\nZalaZone\nMedium headway', 'ACC\nZalaZone\nLarge headway',
                    'ACC\nCARMA1', 'CACC\nCARMA1', 'CACC\nCARMA2'], rotation=90)
ax.set_ylabel('Headway (s)')
[ax.axhline(y=i, linewidth=0.5, color='black', alpha=0.2) for i in [1, 1.5, 2, 2.5, 3, 3.5]]
fig.tight_layout()

fig.savefig('plots' + '/' + 'hw' + '/' + 'hw_violinplot.png', dpi=300, format='png')


# headway plotting for approx constant speed
df = df[df['hw'] == 1]
df_human = df[(df['mode'] == 'human') & (df['dataset'] == 'trajectories_segment_5.csv')]
df_human = df_human[(df_human['time'] <= 150) & (df_human['time'] > 110)]
df_human['time'] = df_human['time'] - df_human['time'].iloc[0]

df_acc = df[(df['mode'] == 'acc') & (df['campaign'] == 'AstaZero')]
df_acc = df_acc[(df_acc['time'] <= 140) & (df_acc['time'] > 100)]
df_acc['time'] = df_acc['time'] - df_acc['time'].iloc[0]

df_cacc = df[(df['mode'] == 'cacc') & (df['dataset'] == 'run 10')]
df_cacc = df_cacc[(df_cacc['time'] <= 490) & (df_cacc['time'] > 450)]
df_cacc['time'] = df_cacc['time'] - df_cacc['time'].iloc[0]

plot_headway_const(df_human, df_acc, df_cacc)


# headway plotting for a deceleration perturbation
df = pd.read_csv('aggregated_data.csv', low_memory=False)

df_human_pert = df[(df['mode'] == 'human') & (df['dataset'] == 'ASta_040719_platoon3.csv')]
df_human_pert = df_human_pert[(df_human_pert['time'] <= 760) & (df_human_pert['time'] > 720)]
df_human_pert['time'] = df_human_pert['time'] - df_human_pert['time'].iloc[0]

df_acc_pert = df[df['code'] == 4]
df_acc_pert = df_acc_pert[(df_acc_pert['time'] <= 2000) & (df_acc_pert['time'] > 1700)]
df_acc_pert['time'] = df_acc_pert['time'] - df_acc_pert['time'].iloc[0]

df_cacc_pert = df[df['code'] == 39]
df_cacc_pert = df_cacc_pert[(df_cacc_pert['time'] <= 2000) & (df_cacc_pert['time'] > 595)]
df_cacc_pert['time'] = df_cacc_pert['time'] - df_cacc_pert['time'].iloc[0]

plot_headway_pert(df_human_pert, df_acc_pert, df_cacc_pert)


# headway plotting for an acceleration perturbation
df = pd.read_csv('aggregated_data.csv', low_memory=False)

df_human_pert_up = df[(df['mode'] == 'human') & (df['dataset'] == 'ASta_040719_platoon3.csv')]
df_human_pert_up = df_human_pert_up[(df_human_pert_up['time'] <= 695) & (df_human_pert_up['time'] > 650)]
df_human_pert_up['time'] = df_human_pert_up['time'] - df_human_pert_up['time'].iloc[0]

df_acc_pert_up = df[df['code'] == 8]
df_acc_pert_up = df_acc_pert_up[(df_acc_pert_up['time'] <= 620) & (df_acc_pert_up['time'] > 575)]
df_acc_pert_up['time'] = df_acc_pert_up['time'] - df_acc_pert_up['time'].iloc[0]

df_cacc_pert_up = df[df['code'] == 40]
df_cacc_pert_up['time'] = df_cacc_pert_up['time'] - df_cacc_pert_up['time'].iloc[0]

plot_headway_pert_up(df_human_pert_up, df_acc_pert_up, df_cacc_pert_up)
