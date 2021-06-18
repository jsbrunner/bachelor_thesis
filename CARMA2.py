import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import lowess
from datetime import datetime
from plots import plot_xvah
from plots import compare_speed_measurements
from plots import compare_acc_measurements
from plots import plot_speed

pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)


# function reading individual runs of the CARMA2 campaign data set
def read_cacc(run, t_start, t_end):
    # run numbers 5, 6, 9, 10, 13 are platoons with 5 vehicles in the same order
    df = pd.read_csv('Cooperative_Automated_Research_Mobility_Applications__CARMA__2.csv', low_memory=False)
    df = df[df['RunNo'] == run]

    # only consider specific columns
    use_columns = ['LocationDateTime', 'RunNo', 'Elapsed_Time']
    veh_colors = ['BLACK', 'GREEN', 'GREY', 'SILVER', 'WHITE']
    columns_per_v = ['veh_color', 'bin_utc_time_s', 'command_mode_cacc', 'vehspdavgdrvn_srx',
                     'flrrtrk1range_srx', 'flrrtrk7range_srx', 'flrrtrk9range_srx', 'velocity_fwd_pinpoint',
                     'velocity_fwd_admas', 'p29_actual_vehicle_acceleration']
    for i in veh_colors:
        for j in columns_per_v:
            use_columns.append(j + '_' + i)
    df = df[use_columns]

    # cut dataframe to start and end time
    df = df[df['Elapsed_Time'] < t_end]
    df = df[df['Elapsed_Time'] >= t_start]

    df['bin_utc_time'] = pd.to_datetime(df['bin_utc_time_s_BLACK'], unit='s')
    df = df.sort_values(['Elapsed_Time'], ascending=True)

    # set negative speeds to 0
    for i in veh_colors:
        df['velocity_fwd_pinpoint_{}'.format(i)][df['velocity_fwd_pinpoint_{}'.format(i)] < 0] = 0

    # trajectories from GPS pinpoint speeds
    for i in veh_colors:
        df['trajectory_{}'.format(i)] = df['velocity_fwd_pinpoint_{}'.format(i)].cumsum().multiply(0.1)

    # smooth trajectories with lowess (locally weighted scatterplot smoothing) or rolling average for faster computation
    for i in veh_colors:
        # df['trajectory_{}'.format(i)] = lowess.lowess(df['Elapsed_Time'], df['trajectory_{}'.format(i)], bandwidth=(1/df.shape[0])*10, polynomialDegree=1)  # bandwith makes the difference
        df['trajectory_{}'.format(i)] = df['trajectory_{}'.format(i)].rolling(window=11, center=True).mean()  # old smoothing algorithm, but faster

    # compute relative speed to leading vehicle to compute speed of followers -> idea dismissed
    '''
    # calculate distance to leader (vehicle length not included but also not necessary for this application) for every follower
    for i in veh_colors:
        if i != 'BLACK':
            df['flrrtrk1range_srx_{}'.format(i)] = df['flrrtrk1range_srx_{}'.format(i)].rolling(window=20, center=True).mean()

    df['dist_to_leadvehicle_GREEN'] = df['flrrtrk1range_srx_GREEN']
    df['dist_to_leadvehicle_GREY'] = df['flrrtrk1range_srx_GREEN'] + df['flrrtrk1range_srx_GREY']
    df['dist_to_leadvehicle_SILVER'] = df['flrrtrk1range_srx_GREEN'] + df['flrrtrk1range_srx_GREY'] + df['flrrtrk1range_srx_SILVER']
    df['dist_to_leadvehicle_WHITE'] = df['flrrtrk1range_srx_GREEN'] + df['flrrtrk1range_srx_GREY'] + df['flrrtrk1range_srx_SILVER'] + df['flrrtrk1range_srx_WHITE']

    for i in veh_colors:  # get relative velocity to the leading vehicle
        if i != 'BLACK':
            df['rel_vel_to_leadvehicle_{}'.format(i)] = df['dist_to_leadvehicle_{}'.format(i)].diff().multiply(10)
    '''

    # speeds from trajectories
    for i in veh_colors:
        df['velocity_{}'.format(i)] = df['trajectory_{}'.format(i)].diff().multiply(10)

    # calculate acceleration from GPS CARMA2 Pinpoint
    for i in veh_colors:
        df['acc_{}'.format(i)] = df['velocity_{}'.format(i)].diff().multiply(10)

    # calculate headway
    for i in veh_colors:
        if i != 'BLACK':
            df['headway_{}'.format(i)] = (df['flrrtrk1range_srx_{}'.format(i)] + 5) / df['velocity_{}'.format(i)]

    # call plotting of different speed measurements
    compare_speed_measurements(df)

    # drop useless columns
    df = df[['Elapsed_Time', 'flrrtrk1range_srx_GREEN',
             'flrrtrk1range_srx_GREY', 'flrrtrk1range_srx_SILVER', 'flrrtrk1range_srx_WHITE',
             'trajectory_BLACK', 'trajectory_GREEN', 'trajectory_GREY',
             'trajectory_SILVER', 'trajectory_WHITE', 'velocity_BLACK',
             'velocity_GREEN', 'velocity_GREY', 'velocity_SILVER', 'velocity_WHITE',
             'acc_BLACK', 'acc_GREEN', 'acc_GREY', 'acc_SILVER', 'acc_WHITE',
             'headway_GREEN', 'headway_GREY', 'headway_SILVER', 'headway_WHITE']]

    # rename columns to match the desired naming pattern
    df = df.rename(columns={'Elapsed_Time': 'time', 'flrrtrk1range_srx_GREEN': 'ivs1',
                            'flrrtrk1range_srx_GREY': 'ivs2', 'flrrtrk1range_srx_SILVER': 'ivs3', 'flrrtrk1range_srx_WHITE': 'ivs4',
                            'trajectory_BLACK': 'xL', 'trajectory_GREEN': 'x1', 'trajectory_GREY': 'x2',
                            'trajectory_SILVER': 'x3', 'trajectory_WHITE': 'x4', 'velocity_BLACK': 'vL',
                            'velocity_GREEN': 'v1', 'velocity_GREY': 'v2', 'velocity_SILVER': 'v3', 'velocity_WHITE': 'v4',
                            'acc_BLACK': 'aL', 'acc_GREEN': 'a1', 'acc_GREY': 'a2', 'acc_SILVER': 'a3', 'acc_WHITE': 'a4',
                            'headway_GREEN': 'hL1', 'headway_GREY': 'h12', 'headway_SILVER': 'h23', 'headway_WHITE': 'h34'})

    return df
