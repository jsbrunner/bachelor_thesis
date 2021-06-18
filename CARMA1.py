import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from plots import plot_xvah

mpl.rcParams['agg.path.chunksize'] = 10000

pd.set_option('display.max_columns', None)


# function reading individual runs of the CARMA1 campaign data set
def read_carma1(run, t_start, t_end):
    df = pd.read_csv('Test_Data_of_Proof-of-Concept_Vehicle_Platooning_Based_on_Cooperative_Adaptive_Cruise_Control__CACC_.csv')
    df = df.sort_values('bin_utc_time_formatted')
    df = df[df['Run'] == run]

    # run 29: BLACK, GREEN, WHITE, SILVER, GREY: 60-45-60 for 5 mins -> Hybrid
    # run 30: BLACK, WHITE, GREY, GREEN, SILVER: 55-60-45-60-45 for 10 min -> ACC
    # run 68: BLACK, GREEN, WHITE, SILVER, GREY: 60-45-60 for 5 mins -> CACC
    # run 69: BLACK, WHITE, SILVER, GREY, GREEN: 60-45-60 for 5 mins -> CACC
    # run 70: BLACK, SILVER, GREY, GREEN, WHITE: 60-45-60 for 5 mins -> CACC
    # run 71: BLACK, GREY, GREEN, WHITE, SILVER: 60-45-60 for 5 mins -> CACC
    # run 72: BLACK, GREEN, WHITE, SILVER, GREY: 60-45-60 for 5 mins -> CACC

    # each run has a different order of vehicles in the platoon
    suffixes = list()
    if run == 29:
        suffixes = ['-bl', '-grn', '-wt', '-ag', '-gry']
    if run == 30:
        suffixes = ['-bl', '-wt', '-gry', '-grn', '-ag']
    if run == 68:
        suffixes = ['-bl', '-grn', '-wt', '-ag', '-gry']
    if run == 69:
        suffixes = ['-bl', '-wt', '-ag', '-gry', '-grn']
    if run == 70:
        suffixes = ['-bl', '-ag', '-gry', '-grn', '-wt']
    if run == 71:
        suffixes = ['-bl', '-gry', '-grn', '-wt', '-ag']
    if run == 72:
        suffixes = ['-bl', '-grn', '-wt', '-ag', '-gry']

    use_columns = ['Run', 'bin_utc_time_formatted', 'elapsed_time (s)']
    columns_per_veh = ['bin_utc_time_s', 'setSpeed_CACC', 'distToPVeh_CACC', 'speed_CACC', 'velocity_fwd_PINPOINT', 'max_accel_CACC']

    for i in suffixes:
        for j in columns_per_veh:
            use_columns.append(j + i)
    df = df[use_columns]
    print(df.columns)

    # interpolate missing speed values
    for i in suffixes:
        df['speed{}'.format(i)] = df['speed_CACC{}'.format(i)].interpolate()

    # compute trajectories
    for i in suffixes:
        df['pos{}'.format(i)] = df['speed{}'.format(i)].cumsum().multiply(0.05)
        df['pos{}'.format(i)] = df['pos{}'.format(i)].rolling(window=21, center=True).mean()

    # compute speed from trajectories
    for i in suffixes:
        df['speed{}'.format(i)] = df['pos{}'.format(i)].diff().multiply(20)

    # compute acceleration
    for i in suffixes:
        df['acc{}'.format(i)] = df['speed{}'.format(i)].diff().multiply(20)

    # interpolate range measurements
    for i in suffixes:
        df['distToPVeh_CACC{}'.format(i)] = df['distToPVeh_CACC{}'.format(i)].interpolate()

    # compute headway
    for i in range(0, 4):
        df['hw{}{}'.format(suffixes[i], suffixes[i + 1])] = (df['distToPVeh_CACC{}'.format(suffixes[i + 1])] + 5) / df['speed{}'.format(suffixes[i + 1])]

    # drop useless columns
    df = df[['elapsed_time (s)', 'distToPVeh_CACC{}'.format(suffixes[1]), 'distToPVeh_CACC{}'.format(suffixes[2]),
             'distToPVeh_CACC{}'.format(suffixes[3]), 'distToPVeh_CACC{}'.format(suffixes[4]),
             'speed-bl', 'speed-wt', 'speed-ag', 'speed-gry', 'speed-grn', 'pos-bl', 'pos-wt', 'pos-ag',
             'pos-gry', 'pos-grn', 'acc-bl', 'acc-wt', 'acc-ag', 'acc-gry', 'acc-grn', 'hw{}{}'.format(suffixes[0], suffixes[1]),
             'hw{}{}'.format(suffixes[1], suffixes[2]), 'hw{}{}'.format(suffixes[2], suffixes[3]), 'hw{}{}'.format(suffixes[3], suffixes[4])]]

    # rename columns to match the desired naming pattern
    df = df.rename(columns={'elapsed_time (s)': 'time', 'distToPVeh_CACC{}'.format(suffixes[1]): 'ivs1', 'distToPVeh_CACC{}'.format(suffixes[2]): 'ivs2',
                            'distToPVeh_CACC{}'.format(suffixes[3]): 'ivs3', 'distToPVeh_CACC{}'.format(suffixes[4]): 'ivs4', 'speed{}'.format(suffixes[0]): 'vL',
                            'speed{}'.format(suffixes[1]): 'v1', 'speed{}'.format(suffixes[2]): 'v2', 'speed{}'.format(suffixes[3]): 'v3',
                            'speed{}'.format(suffixes[4]): 'v4', 'pos{}'.format(suffixes[0]): 'xL', 'pos{}'.format(suffixes[1]): 'x1',
                            'pos{}'.format(suffixes[2]): 'x2', 'pos{}'.format(suffixes[3]): 'x3', 'pos{}'.format(suffixes[4]): 'x4',
                            'acc{}'.format(suffixes[0]): 'aL', 'acc{}'.format(suffixes[1]): 'a1', 'acc{}'.format(suffixes[2]): 'a2',
                            'acc{}'.format(suffixes[3]): 'a3', 'acc{}'.format(suffixes[4]): 'a4', 'hw{}{}'.format(suffixes[0], suffixes[1]): 'hL1',
                            'hw{}{}'.format(suffixes[1], suffixes[2]): 'h12', 'hw{}{}'.format(suffixes[2], suffixes[3]): 'h23',
                            'hw{}{}'.format(suffixes[3], suffixes[4]): 'h34'})

    # crop data to specified length
    df = df[df['time'] < t_end]
    df = df[df['time'] >= t_start]

    return df
