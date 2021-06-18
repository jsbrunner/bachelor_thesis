import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians
import lowess
from plots import plot_xvah
from plots import perturbation_plot
from ZalaZone import read_zalazone

pd.set_option('display.max_columns', None)


# function reading data from the AstaZero campaign
def read_acc(filename, t_start, t_end):
    # handle first rows of data
    df = pd.read_csv(filename, header=None, low_memory=False)
    specs = df.iloc[0:5, 0:6]
    specs.columns = ['Cat.', '-', '-', '-', '-', '-']
    df = df[5:]
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    df.reset_index(drop=True, inplace=True)
    df.dropna(axis='columns', inplace=True)
    df = df.drop(columns={'Driver1', 'Driver2', 'Driver3', 'Driver4', 'Driver5'})
    df = df.astype('float64')

    # cut dataframe to start and end time
    df = df[df['Time'] < t_end]
    df = df[df['Time'] >= t_start]

    # rename columns
    df = df.rename(columns={"Speed1": "SpeedL", "Speed2": "Speed1", "Speed3": "Speed2", "Speed4": "Speed3", "Speed5": "Speed4"})

    # function to calculate distance from longitude and latitude coordinates
    def calc_dist(lat1, lon1, lat2, lon2):
        r = 6373000
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return r * c

    # For trajectories calculate starting distance between vehicles with coordinates (function) and subtract them from the distances as a constant
    pos = [df.iloc[0]['Lat1'], df.iloc[0]['Lon1'], df.iloc[0]['Lat2'], df.iloc[0]['Lon2'], df.iloc[0]['Lat3'], df.iloc[0]['Lon3'], df.iloc[0]['Lat4'], df.iloc[0]['Lon4'], df.iloc[0]['Lat5'],
           df.iloc[0]['Lon5']]
    starting_dist = [calc_dist(pos[0], pos[1], pos[2], pos[3]), calc_dist(pos[0], pos[1], pos[4], pos[5]), calc_dist(pos[0], pos[1], pos[6], pos[7]), calc_dist(pos[0], pos[1], pos[8], pos[9])]

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

    # Subtracting the line-up distance at the start for each vehicle ("Speed"-columns now mean the distance from start)
    df['Dist1'] = df['Dist1'] - starting_dist[0]
    df['Dist2'] = df['Dist2'] - starting_dist[1]
    df['Dist3'] = df['Dist3'] - starting_dist[2]
    df['Dist4'] = df['Dist4'] - starting_dist[3]

    # Calculate headway
    df['headway_L1'] = (df['IVS1(m)'] + 5) / df['Speed1']
    df['headway_12'] = (df['IVS2(m)'] + 5) / df['Speed2']
    df['headway_23'] = (df['IVS3(m)'] + 5) / df['Speed3']
    df['headway_34'] = (df['IVS4(m)'] + 5) / df['Speed4']

    # Calculate acceleration
    for i in list_vehicles:
        df['Acc{}'.format(i)] = df['Speed{}'.format(i)].diff().multiply(10)

    # drop unnecessary columns
    df = df[['Time', 'SpeedL', 'Speed1', 'Speed2', 'Speed3', 'Speed4', 'IVS1(m)',
                     'IVS2(m)', 'IVS3(m)', 'IVS4(m)', 'DistL', 'Dist1', 'Dist2', 'Dist3',
                     'Dist4', 'headway_L1', 'headway_12', 'headway_23',
                     'headway_34', 'AccL', 'Acc1', 'Acc2', 'Acc3', 'Acc4']]

    # rename columns to suit fixed pattern
    df = df.rename(columns={'Time': 'time', "SpeedL": "vL", "Speed1": "v1", "Speed2": "v2", "Speed3": "v3", "Speed4": "v4",
                            'IVS1(m)': 'ivs1', 'IVS2(m)': 'ivs2', 'IVS3(m)': 'ivs3', 'IVS4(m)': 'ivs4',
                            'DistL': 'xL', 'Dist1': 'x1', 'Dist2': 'x2', 'Dist3': 'x3',
                            'Dist4': 'x4', 'headway_L1': 'hL1', 'headway_12': 'h12', 'headway_23': 'h23', 'headway_34': 'h34', 'AccL': 'aL',
                            'Acc1': 'a1', 'Acc2': 'a2', 'Acc3': 'a3', 'Acc4': 'a4'})

    return df
