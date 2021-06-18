import pandas as pd
from methods import rt_makridis
from methods import rt_lanaud
from methods import rt_li
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'figure.max_open_warning': 0})
df = pd.read_csv('aggregated_data.csv', low_memory=False)


# choose perturbation events from the aggregated data set
df_rt = df[df['rt'] == 1]
incl_runs = df_rt['code'].unique()
incl_runs = np.delete(incl_runs, [1, 13, 21, 22, 26, 27])  # runs excluded due to bad response time recognition

veh_list = ['L', '1', '2', '3', '4']

# dictionary to save estimated rt from the three methods
rt_dict = {'makridis': {'acc': {'AstaZero': [],
                                'ZalaZone': {'S': [],
                                             'M': [],
                                             'L': []}},
                        'cacc': {'CARMA2': []}},
           'lanaud': {'acc': {'AstaZero': [],
                              'ZalaZone': {'S': [],
                                           'M': [],
                                           'L': []}},
                      'cacc': {'CARMA2': []}},
           'li': {'acc': {'AstaZero': [],
                          'ZalaZone': {'S': [],
                                       'M': [],
                                       'L': []}},
                  'cacc': {'CARMA2': []}}}

# number to label the perturbation events
running_number = 1

# response time estimation with the 3 methods for each following vehicle in the platoon
for i in incl_runs:
    df_pert = df_rt[df_rt['code'] == i]
    for j in range(1, 5):
        print(i, 'v{}'.format(veh_list[j - 1]), 'v{}'.format(veh_list[j]))
        makridis = rt_makridis(df_pert, 'time', 'v{}'.format(veh_list[j - 1]), 'v{}'.format(veh_list[j]))
        lanaud = rt_lanaud(df_pert, 'time', 'v{}'.format(veh_list[j - 1]), 'v{}'.format(veh_list[j]), 0, 10, 50, 2, 0.75, 0.75)
        li = rt_li(df_pert, 'time', 'v{}'.format(veh_list[j - 1]), 'v{}'.format(veh_list[j]), df_pert['acc_dec'].iloc[0])
        # print(makridis, lanaud, li)
        if df_pert['campaign'].iloc[0] == 'ZalaZone':
            rt_dict['makridis']['acc']['ZalaZone'][df_pert['hw_set'].iloc[0]].append(makridis)
            rt_dict['lanaud']['acc']['ZalaZone'][df_pert['hw_set'].iloc[0]].append(lanaud)
            rt_dict['li']['acc']['ZalaZone'][df_pert['hw_set'].iloc[0]].append(li)
        else:
            rt_dict['makridis'][df_pert['mode'].iloc[0]][df_pert['campaign'].iloc[0]].append(makridis)
            rt_dict['lanaud'][df_pert['mode'].iloc[0]][df_pert['campaign'].iloc[0]].append(lanaud)
            rt_dict['li'][df_pert['mode'].iloc[0]][df_pert['campaign'].iloc[0]].append(li)

        # figure to check the response time immediately
        if j == 1:
            scatter_size = 20
            fig, ax = plt.subplots(1)
            fig.suptitle('N°{}, {}, {}\nMa: {} s | La: {} s | Li: {} s'.format(running_number, df_pert['mode'].iloc[0], df_pert['campaign'].iloc[0], makridis[0], lanaud[0], li[0]))
            fig.set_size_inches(3, 3)
            ax.plot(df_pert['time'], df_pert['vL'])
            ax.plot(df_pert['time'], df_pert['v1'])
            df_pert['time'] = round(df_pert['time'], 1)
            ax.scatter(lanaud[1], df_pert.loc[df_pert['time'] == lanaud[1], 'vL'], color='black', label='Lanaud leader instant', s=scatter_size)
            ax.scatter(li[1], df_pert.loc[df_pert['time'] == li[1], 'vL'], color='black', marker='D', label='Li leader instant', s=scatter_size)
            ax.scatter(lanaud[2], df_pert.loc[df_pert['time'] == lanaud[2], 'v1'], color='black', label='Lanaud follower instant', s=scatter_size)
            ax.scatter(li[2], df_pert.loc[df_pert['time'] == li[2], 'v1'], color='black', marker='D', label='Li follower instant', s=scatter_size)
            ax.set_xticks([])
            ax.set_yticks([])
            fig.tight_layout(pad=0.4)

            fig.savefig('plots' + '/' + 'rt' + '/' + 'pert_run_{}.png'.format(running_number), dpi=300, format='png')

            running_number += 1

# correlation coefficient threshold
ma_coefficient_threshold = 0.95
# rt-thresholds
ma_threshold = [0, 10]
la_threshold = [0, 10]
li_threshold = [0, 10]

# transferring the estimated response times into lists for plotting
ma_az = []
for i in rt_dict['makridis']['acc']['AstaZero']:
    if i[1] >= ma_coefficient_threshold and i[0] >= 1 and i[0] <= 2.5:
        ma_az.append(i[0])
ma_zz_s = []
for i in rt_dict['makridis']['acc']['ZalaZone']['S']:
    if i[1] >= ma_coefficient_threshold and i[0] >= ma_threshold[0] and i[0] <= ma_threshold[1]:
        ma_zz_s.append(i[0])
ma_zz_m = []
for i in rt_dict['makridis']['acc']['ZalaZone']['M']:
    if i[1] >= ma_coefficient_threshold and i[0] >= ma_threshold[0] and i[0] <= 2.1:
        ma_zz_m.append(i[0])
ma_zz_l = []
for i in rt_dict['makridis']['acc']['ZalaZone']['L']:
    if i[1] >= ma_coefficient_threshold and i[0] >= ma_threshold[0] and i[0] <= ma_threshold[1]:
        ma_zz_l.append(i[0])
ma_carma = []
for i in rt_dict['makridis']['cacc']['CARMA2']:
    if i[1] >= ma_coefficient_threshold and i[0] >= ma_threshold[0] and i[0] <= 1:
        ma_carma.append(i[0])

la_az = []
for i in rt_dict['lanaud']['acc']['AstaZero']:
    if i[0] >= 0.5 and i[0] <= 3:
        la_az.append(i[0])
la_zz_s = []
for i in rt_dict['lanaud']['acc']['ZalaZone']['S']:
    if i[0] >= la_threshold[0] and i[0] <= la_threshold[1]:
        la_zz_s.append(i[0])
la_zz_m = []
for i in rt_dict['lanaud']['acc']['ZalaZone']['M']:
    if i[0] >= 0.5 and i[0] <= 3:
        la_zz_m.append(i[0])
la_zz_l = []
for i in rt_dict['lanaud']['acc']['ZalaZone']['L']:
    if i[0] >= 0.5 and i[0] <= 3:
        la_zz_l.append(i[0])
la_carma = []
for i in rt_dict['lanaud']['cacc']['CARMA2']:
    if i[0] >= la_threshold[0] and i[0] <= 0.5:
        la_carma.append(i[0])

li_az = []
for i in rt_dict['li']['acc']['AstaZero']:
    if i[0] >= li_threshold[0] and i[0] <= 3:
        li_az.append(i[0])
li_zz_s = []
for i in rt_dict['li']['acc']['ZalaZone']['S']:
    if i[0] >= 0.5 and i[0] <= 2:
        li_zz_s.append(i[0])
li_zz_m = []
for i in rt_dict['li']['acc']['ZalaZone']['M']:
    if i[0] >= li_threshold[0] and i[0] <= li_threshold[1]:
        li_zz_m.append(i[0])
li_zz_l = []
for i in rt_dict['li']['acc']['ZalaZone']['L']:
    if i[0] >= 1 and i[0] <= 3:
        li_zz_l.append(i[0])
li_carma = []
for i in rt_dict['li']['cacc']['CARMA2']:
    if i[0] >= li_threshold[0] and i[0] <= 1:
        li_carma.append(i[0])

# created nested lists for violinplot
nested_makridis = [ma_az, ma_zz_s, ma_zz_m, ma_zz_l, ma_carma]
nested_lanaud = [la_az, la_zz_s, la_zz_m, la_zz_l, la_carma]
nested_li = [li_az, li_zz_s, li_zz_m, li_zz_l, li_carma]

# plot response times
fig_bp, (ax_ma, ax_la, ax_li) = plt.subplots(3)
fig_bp.set_size_inches(8, 8)
ymin = 0
ymax = 3.5
width = 0.7
x_ticks = ['ACC Astazero', 'ACC ZalaZone\nsmall headway', 'ACC ZalaZone\nmedium headway', 'ACC ZalaZone\nlarge headway', 'CACC CARMA2']

ax_ma.set_title('Estimations with method from Makridis et al. (2020b)')
ax_ma.violinplot(nested_makridis, widths=width)
ax_ma.set_ylabel('Response time (s)')
ax_ma.set_ylim(ymin=ymin, ymax=ymax)
ax_ma.set_xticks([1, 2, 3, 4, 5])
ax_ma.set_xticklabels(x_ticks)

ax_la.set_title('Estimations with method from Lanaud et al. (2021)')
ax_la.violinplot(nested_lanaud, widths=width)
ax_la.set_ylabel('Response time (s)')
ax_la.set_ylim(ymin=ymin, ymax=ymax)
ax_la.set_xticks([1, 2, 3, 4, 5])
ax_la.set_xticklabels(x_ticks)

ax_li.set_title('Estimations with method from Li et al. (2021)')
ax_li.violinplot(nested_li, widths=width)
ax_li.set_ylabel('Response time (s)')
ax_li.set_ylim(ymin=ymin, ymax=ymax)
ax_li.set_xticks([1, 2, 3, 4, 5])
ax_li.set_xticklabels(x_ticks)

fig_bp.tight_layout(pad=1.5)

fig_bp.savefig('plots' + '/' + 'rt' + '/' + 'boxplots.png', dpi=300, format='png')
