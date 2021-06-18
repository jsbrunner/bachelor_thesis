import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


# Plotting speeds, trajectories and acceleration
def plot_xvah(df_plot, title):
    fig, (ax2, ax1, ax4) = plt.subplots(3, 1)
    fig.suptitle('Position, Speed, and Acceleration\n{}'.format(title), y=0.95)
    fig.set_size_inches(9, 6, forward=True)

    # parameters for iteration and plot
    list_vehicles = ['L', '1', '2', '3', '4']
    grid = True
    width = 0.7

    for i in list_vehicles:
        ax1.plot(df_plot['time'], df_plot['v{}'.format(i)], label='V {}'.format(i), linewidth=width)
    ax1.set_ylabel('Speed (m/s)')
    ax1.grid(grid)

    for i in list_vehicles:
        ax2.plot(df_plot['time'], df_plot['x{}'.format(i)]/1000, label='Vehicle {}'.format(i), linewidth=width)
    ax2.set_ylabel('Position (km)')
    ax2.grid(grid)

    for i in list_vehicles:
        ax4.plot(df_plot['time'], df_plot['a{}'.format(i)], label='A {}'.format(i), linewidth=width)
    ax4.set_ylabel('Acceleration (m/s²)')
    ax4.grid(grid)
    ax4.set_xlabel('Time (s)')

    ax2.legend(fontsize='small', ncol=1)


# plot comarison of different speed measurements
def compare_speed_measurements(df):
    fig_speeds, ax_s = plt.subplots(1)
    fig_speeds.suptitle('Speed measurement comparison: GPS CARMA2 Pinpoint,\nGPS CARMA2 Pinpoint (smoothed), GPS ADMAS, and Wheel', y=0.97)
    fig_speeds.set_size_inches(8, 6)

    ax_s.plot(df['Elapsed_Time'], df['velocity_fwd_pinpoint_BLACK'], label='GPS CARMA2 Pinpoint')
    ax_s.plot(df['Elapsed_Time'], df['velocity_BLACK'], label='GPS CARMA2 Pinpoint smoothed BLACK')
    ax_s.plot(df['Elapsed_Time'], df['velocity_fwd_admas_BLACK'], label='GPS ADMAS')
    ax_s.plot(df['Elapsed_Time'], df['vehspdavgdrvn_srx_BLACK'], label='Wheel')
    # ax_s.plot(df['Elapsed_Time'], df['velocity_smoothed_GREEN'], label='Velocity smoothed GREEN')
    # ax_s.plot(df['Elapsed_Time'], df['velocity_from_IVS_GREEN'], label='Velocity from IVS GREEN')
    # ax_s.plot(df['Elapsed_Time'], df['velocity_smoothed_GREY'], label='Velocity smoothed GREY')
    # ax_s.plot(df['Elapsed_Time'], df['velocity_from_IVS_GREY'], label='Velocity from IVS GREY')
    # ax_s.plot(df['Elapsed_Time'], df['command_mode_cacc_BLACK'], label='CACC BLACK active')
    ax_s.set_ylabel('Speed (m/s)')
    ax_s.set_xlabel('Time (s)')
    ax_s.grid(True)
    ax_s.legend()


# plot acceleration measurements (derivation from speed and directly measured in vehicle (CARMA2))
def compare_acc_measurements(df):
    fig_acc, ax_a = plt.subplots(1)
    fig_acc.suptitle('Acceleration comparison:\nacceleration from data and acceleration derived from speeds', y=0.97)
    fig_acc.set_size_inches(8, 6)

    ax_a.plot(df['Elapsed_Time'], df['p29_actual_vehicle_acceleration_BLACK'], label='Acc. from data')
    ax_a.plot(df['Elapsed_Time'], df['acc_BLACK'], label='Derivation of interpolated, smoothed speed')
    ax_a.set_ylabel('Acc. (m/s²)')
    ax_a.grid(True)
    ax_a.legend()


# plot single perturbation
def perturbation_plot(df_plot):
    fig, ax1 = plt.subplots(1)
    fig.set_size_inches(5, 3, forward=True)

    # parameters for iteration and plot
    list_vehicles = ['L', '1', '2', '3', '4']
    grid = True
    width = 1

    for i in list_vehicles:
        ax1.plot(df_plot['time'], df_plot['v{}'.format(i)], label='Vehicle {}'.format(i), linewidth=width)
    ax1.set_ylabel('Speed (m/s)')
    ax1.legend(fontsize='small', ncol=1)
    ax1.set_xlabel('Time (s)')
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.tight_layout()


# plot platoon speeds for a data slice
def plot_speed(df):
    fig, ax1 = plt.subplots(1)
    fig.set_size_inches(6, 4, forward=True)

    # parameters for iteration and plot
    list_vehicles = ['L', '1', '2', '3', '4']
    grid = True
    width = 1

    for i in list_vehicles:
        ax1.plot(df['time'], df['v{}'.format(i)], label='Vehicle {}'.format(i), linewidth=width)
    ax1.set_ylabel('Speed (m/s)')
    ax1.vlines(340, ymin=20, ymax=27.5, linestyles='dashed', color='darkred')
    ax1.legend(fontsize='small', ncol=1)
    ax1.set_xlabel('Time (s)')
    fig.tight_layout()


# plot headway comparison for data slices with approximately constant speed
def plot_headway_const(df_human, df_acc, df_cacc):
    fig, ((ax1, ax3, ax5), (ax2, ax4, ax6)) = plt.subplots(2, 3)
    fig.set_size_inches(10, 6)
    width = 0.8

    speed_list = ['vL', 'v1', 'v2', 'v3', 'v4']
    hw_list = ['hL1', 'h12', 'h23', 'h34']

    for i in speed_list:
        ax1.plot(df_human['time'], df_human[i], linewidth=width, label=i)
        ax3.plot(df_acc['time'], df_acc[i], linewidth=width, label=i)
        ax5.plot(df_cacc['time'], df_cacc[i], linewidth=width, label=i)
    for i in hw_list:
        ax2.plot(df_human['time'], df_human[i], linewidth=width, label=i)
        ax4.plot(df_acc['time'], df_acc[i], linewidth=width, label=i)
        ax6.plot(df_cacc['time'], df_cacc[i], linewidth=width, label=i)

    ax2.set_ylim(0, 4)
    ax4.set_ylim(0, 4)
    ax6.set_ylim(0, 4)

    ax1.set_ylim(5, 20)
    ax3.set_ylim(14, 19)
    ax5.set_ylim(24, 29)

    ax1.set_title('Human drivers')
    ax3.set_title('ACC')
    ax5.set_title('CACC')

    ax1.set_ylabel('Speed (m/s)')
    ax2.set_ylabel('Headway (s)')

    ax2.set_xlabel('Time (s)')
    ax4.set_xlabel('Time (s)')
    ax6.set_xlabel('Time (s)')

    ax1.set_xticks([])
    ax3.set_xticks([])
    ax5.set_xticks([])

    ax1.legend(ncol=5, fontsize='xx-small', loc='lower left')
    ax2.legend(ncol=4, fontsize='xx-small', loc='lower left')

    fig.tight_layout()

    fig.savefig('plots' + '/' + 'hw' + '/' + 'hw_profiles_constant.png', dpi=300, format='png')


# plot headway comparison for data slices with deceleration perturbation events
def plot_headway_pert(df_human, df_acc, df_cacc):
    fig, ((ax1, ax3, ax5), (ax2, ax4, ax6)) = plt.subplots(2, 3)
    fig.set_size_inches(10, 6)
    width = 0.8

    speed_list = ['vL', 'v1', 'v2', 'v3', 'v4']
    hw_list = ['hL1', 'h12', 'h23', 'h34']

    for i in speed_list:
        ax1.plot(df_human['time'], df_human[i], linewidth=width, label=i)
        ax3.plot(df_acc['time'], df_acc[i], linewidth=width, label=i)
        ax5.plot(df_cacc['time'], df_cacc[i], linewidth=width, label=i)
    for i in hw_list:
        ax2.plot(df_human['time'], df_human[i], linewidth=width, label=i)
        ax4.plot(df_acc['time'], df_acc[i], linewidth=width, label=i)
        ax6.plot(df_cacc['time'], df_cacc[i], linewidth=width, label=i)

    ax2.set_ylim(0, 4)
    ax4.set_ylim(0, 4)
    ax6.set_ylim(0, 4)

    ax1.set_ylim(14, 27)
    ax3.set_ylim(5, 22)
    ax5.set_ylim(18, 28)

    ax1.set_title('Human drivers')
    ax3.set_title('ACC')
    ax5.set_title('CACC')

    ax1.set_ylabel('Speed (m/s)')
    ax2.set_ylabel('Headway (s)')

    ax2.set_xlabel('Time (s)')
    ax4.set_xlabel('Time (s)')
    ax6.set_xlabel('Time (s)')

    ax1.set_xticks([])
    ax3.set_xticks([])
    ax5.set_xticks([])

    ax1.legend(ncol=5, fontsize='xx-small', loc='lower left')
    ax2.legend(ncol=4, fontsize='xx-small', loc='lower left')

    fig.tight_layout()

    fig.savefig('plots' + '/' + 'hw' + '/' + 'hw_profiles_pert.png', dpi=300, format='png')


# plot headway comparison for data slices with acceleration perturbation events
def plot_headway_pert_up(df_human, df_acc, df_cacc):
    fig, ((ax1, ax3, ax5), (ax2, ax4, ax6)) = plt.subplots(2, 3)
    fig.set_size_inches(10, 6)
    width = 0.8

    speed_list = ['vL', 'v1', 'v2', 'v3', 'v4']
    hw_list = ['hL1', 'h12', 'h23', 'h34']

    for i in speed_list:
        ax1.plot(df_human['time'], df_human[i], linewidth=width, label=i)
        ax3.plot(df_acc['time'], df_acc[i], linewidth=width, label=i)
        ax5.plot(df_cacc['time'], df_cacc[i], linewidth=width, label=i)
    for i in hw_list:
        ax2.plot(df_human['time'], df_human[i], linewidth=width, label=i)
        ax4.plot(df_acc['time'], df_acc[i], linewidth=width, label=i)
        ax6.plot(df_cacc['time'], df_cacc[i], linewidth=width, label=i)

    ax2.set_ylim(0, 4)
    ax4.set_ylim(0, 4)
    ax6.set_ylim(0, 4)

    ax1.set_ylim(14, 27)
    ax3.set_ylim(11, 35)
    ax5.set_ylim(18.5, 28)

    ax1.set_title('Human drivers')
    ax3.set_title('ACC')
    ax5.set_title('CACC')

    ax1.set_ylabel('Speed (m/s)')
    ax2.set_ylabel('Headway (s)')

    ax2.set_xlabel('Time (s)')
    ax4.set_xlabel('Time (s)')
    ax6.set_xlabel('Time (s)')

    ax1.set_xticks([])
    ax3.set_xticks([])
    ax5.set_xticks([])

    ax1.legend(ncol=5, fontsize='xx-small', loc='lower left')
    ax2.legend(ncol=4, fontsize='xx-small', loc='lower left')

    fig.tight_layout()

    fig.savefig('plots' + '/' + 'hw' + '/' + 'hw_profiles_pert_up.png', dpi=300, format='png')
