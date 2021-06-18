import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.max_open_warning': 0})

df = pd.read_csv('aggregated_data.csv', low_memory=False)

# choose slices in aggregated data set suitable for string stability observation
df_ss = df[df['ss'] == 1]
runs_ss = df_ss['code'].unique()
# print(runs_ss)

# plot perturbations
for i in runs_ss:
    df_ss_temp = df_ss[df_ss['code'] == i]
    fig, ax = plt.subplots()
    fig.suptitle('{}, {}, hw. = {}'.format(df_ss_temp['campaign'].iloc[0], df_ss_temp['dataset'].iloc[0], df_ss_temp['hw_set'].iloc[0]))
    for j in ['vL', 'v1', 'v2', 'v3', 'v4']:
        ax.plot(df_ss_temp['time'], df_ss_temp[j], label=j)
    ax.set_ylabel('Speed (m/s)')
    ax.set_xlabel('Time (s)')
    ax.legend()
plt.show()


# manually determined equilibrium speeds and leader magnitdues as well as difference between leader's and followers' magnitudes
magnitudes_az_down = [[19.3, 2.9], [19.3, 4.4], [19.3, 4.3], [19.5, 5.8], [19.4, 7],
                      [19.3, 2.9], [19.4, 4.4]]  # speed and drop of VL
magn_diff_az_down = [[0, 0.9, 2.4, 3.2, 3.9], [0, 1.2, 3.2, 4.5, 5.7], [0, 0.9, 2.6, 3.3, 4.4],
                     [0, 1.2, 3.3, 4.7, 6], [0, 1.1, 2.9, 4.1, 5.7], [0, 0.8, 2.3, 3, 3.7],
                     [0, 1, 2.8, 3.8, 5]]

magnitudes_az_up = [[19.1, -8.4], [13.7, -13.9], [13.7, -13.8], [19.1, -8.4], [13.7, -13.8], [19.1, -8.5],
                    [19, -8.6], [13.6, -14], [16.4, -8.5]]

magnitudes_az_up = [[j * -1 for j in i] for i in magnitudes_az_up]
magn_diff_az_up = [[0, -1.9, -3.8, -4.8, -6.4], [0, -1.8, -4.1, -5.4, -6.8], [0, -2, -4.3, -5.5, -6.9],
                   [0, -1.3, -2.9, -4, -5.5], [0, -1, -3, -4.4, -6.1], [0, -0.1, -0.8, -3.2, -4.3],
                   [0, -0.4, -2, -4.7, -5.8], [0, -2.5, -4.7, -5.1, -6.4], [0, -0.5, -2.2, -4.6, -4.8]]
magn_diff_az_up = [[j * -1 for j in i] for i in magn_diff_az_up]

magnitudes_zz_s = [[11.1, 1.9], [11.2, 3.4], [11.1, 4.7], [8.1, 2.1], [8.1, 3.5]]
magn_diff_zz_s = [[0, 1.4, 1.7, 2.7, 3.6], [0, 1.2, 1.9, 3.5, 4.4], [0, 2.1, 2.9, 4.8, 5.7],
                  [0, 0.5, 1.2, 2, 2.4], [0, 0.6, 1, 1.7, 2.1]]

magnitudes_zz_m = [[8.1, 2.4], [8.2, 3.6], [11.1, 6], [11.1, 8], [11.1, 7.9]]
magn_diff_zz_m = [[0, -0.2, -0.2, -0.7, -1], [0, -0.6, -0.4, -0.3, -0.5], [0, -0.5, -0.1, -0.2, -0.6],
                  [0, -0.7, -0.9, -0.9, -1.3], [0, -0.7, -0.7, -0.5, -0.5]]

magnitudes_zz_l = [[8.1, 2.1], [8.2, 3.6], [11, 1.9], [11.1, 3.3], [11.1, 5.1]]
magn_diff_zz_l = [[0, -0.9, -1.2, -1.1, -1.1], [0, -0.8, -1.4, -1.4, -1.6], [0, -0.1, -0.3, -0.4, -0.1],
                  [0, 0, -0.2, -0.4, -0.8], [0, -0.4, -0.9, -1.2, -0.7]]

magnitudes_carma2_down = [[26.7, 6.7], [26.7, 6.6], [26.7, 6.6], [26.7, 6.6]]
magn_diff_carma2_down = [[0, 0, -0.3, -0.6, -0.7], [0, 0.3, 0, -0.3, -0.5], [0, -0.2, -0.4, -0.7, -0.9],
                         [0, 0.1, -0.1, -0.4, -0.5]]

magnitudes_carma2_up = [[19.9, -6.6], [20, -6.9], [20.2, -6.6], [20.2, -6.6], [20.1, -6.7]]
magnitudes_carma2_up = [[j * -1 for j in i] for i in magnitudes_carma2_up]
magn_diff_carma2_up = [[0, -0.1, 0.1, 0.3, 0.4], [0, 0, 0.3, 0.4, 0.7], [0, 0, 0.4, 0.4, 0.6],
                       [0, -0.1, 0, 0.2, 0], [0, -0.1, 0.1, 0.3, -0.2]]
magn_diff_carma2_up = [[j * -1 for j in i] for i in magn_diff_carma2_up]

# plot deceleration perturbation
fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 2]})
fig.suptitle('String Stability of Deceleration Perturbations')
fig.set_size_inches(9, 3.5)
marker = 'x-'
scatter_marker = 'x'
markersize = 0.5
markersize_scatter = 20
linewidth = 0.7

# speed and magnitude of leader for deceleration perturbations
for i in magnitudes_az_down:
    print(i, i[0], i[1])
    ax1.scatter(i[0], i[1], s=markersize_scatter, marker=scatter_marker, color='yellowgreen', label='AstaZero acc')
for i in magnitudes_zz_s:
    ax1.scatter(i[0], i[1], s=markersize_scatter, marker=scatter_marker, color='gold', label='ZalaZone acc, small hw.')
for i in magnitudes_zz_m:
    ax1.scatter(i[0], i[1], s=markersize_scatter, marker=scatter_marker, color='indianred', label='ZalaZone acc, medium hw.')
for i in magnitudes_zz_l:
    ax1.scatter(i[0], i[1], s=markersize_scatter, marker=scatter_marker, color='cornflowerblue', label='ZalaZone acc, large hw.')
for i in magnitudes_carma2_down:
    ax1.scatter(i[0], i[1], s=markersize_scatter, marker=scatter_marker, color='black', label='CARMA2 cacc')

# magnitudes of followers for deceleration perturbations
for i in magn_diff_az_down:
    ax2.plot([1, 2, 3, 4, 5], i, marker, linewidth=linewidth, color='yellowgreen', label='AstaZero acc')
for i in magn_diff_zz_s:
    ax2.plot([1, 2, 3, 4, 5], i, marker, linewidth=linewidth, color='gold', label='ZalaZone acc, small hw.')
for i in magn_diff_zz_m:
    ax2.plot([1, 2, 3, 4, 5], i, marker, linewidth=linewidth, color='indianred', label='ZalaZone acc, medium hw.')
for i in magn_diff_zz_l:
    ax2.plot([1, 2, 3, 4, 5], i, marker, linewidth=linewidth, color='cornflowerblue', label='ZalaZone acc, large hw.')
for i in magn_diff_carma2_down:
    ax2.plot([1, 2, 3, 4, 5], i, marker, linewidth=linewidth, color='black', label='CARMA2 cacc')

ax1.set_ylabel('Magnitude (m/s)', fontsize='small')
ax1.set_xlabel('Stable speed (m/s)', fontsize='small')
ax2.set_ylabel('Magnitude difference\n$m_{follower} - m_{leader}$ (m/s)', fontsize='small')
ax2.set_xticks([1, 2, 3, 4, 5])
ax2.set_xticklabels(['leader', 'follower 1', 'follower 2', 'follower 3', 'follower 4'], rotation=0, fontsize='small')

fig.tight_layout(pad=1)

fig.savefig('plots' + '/' + 'ss' + '/' + 'string_stability_deceleration.png', dpi=300, format='png')


# plot acceleration perturbation
fig, (ax3, ax4) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 2]})
fig.suptitle('String Stability of Acceleration Perturbations')
fig.set_size_inches(9, 3.5)
marker = 'x-'
scatter_marker = 'x'
markersize = 0.5
markersize_scatter = 20
linewidth = 0.7

# speed and magnitude of leader for acceleration perturbations
for i in magnitudes_az_up:
    ax3.scatter(i[0]*-1, i[1], s=markersize_scatter, marker=scatter_marker, color='yellowgreen', label='AstaZero acc')
for i in magnitudes_carma2_up:
    ax3.scatter(i[0]*-1, i[1], s=markersize_scatter, marker=scatter_marker, color='black', label='CARMA2 cacc')

# magnitudes of followers for acceleration perturbations
for i in magn_diff_az_up:
    ax4.plot([1, 2, 3, 4, 5], i, marker, linewidth=linewidth, color='yellowgreen', label='AstaZero acc')
for i in magn_diff_carma2_up:
    ax4.plot([1, 2, 3, 4, 5], i, marker, linewidth=linewidth, color='black', label='CARMA2 cacc')

ax3.set_ylabel('Magnitude (m/s)', fontsize='small')
ax3.set_xlabel('Stable speed (m/s)', fontsize='small')
ax4.set_ylabel('Magnitude difference\n$m_{leader} - m_{follower}$ (m/s)', fontsize='small')
ax4.set_xticks([1, 2, 3, 4, 5])
ax4.set_xticklabels(['leader', 'follower 1', 'follower 2', 'follower 3', 'follower 4'], rotation=0, fontsize='small')

fig.tight_layout(pad=1)

fig.savefig('plots' + '/' + 'ss' + '/' + 'string_stability_acceleration.png', dpi=300, format='png')
