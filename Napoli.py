import pandas as pd
import matplotlib.pyplot as plt
from plots import plot_xvah

pd.set_option('display.max_columns', None)


# function reading data from the Punzo and Simonelli campaign from 2005
def read_napoli(filename, t_start, t_end):
    df = pd.read_csv(filename, sep=';')

    # crop dataframe to start and end time
    df = df[df['time'] < t_end]
    df = df[df['time'] >= t_start]
    # vehicle specifications
    vehicle_specs = {'veh1': {'length': 3.71, 'dist_bump_ant': 2.30},
                     'veh2': {'length': 3.83, 'dist_bump_ant': 2.38},
                     'veh3': {'length': 3.83, 'dist_bump_ant': 2.38},
                     'veh4': {'length': 3.48, 'dist_bump_ant': 2.30}}
    veh_numbers = [1, 2, 3, 4]

    # calculate inter-vehicle-spacing (rear bumper to front bumper)
    df['ivs12'] = df['d12'] + vehicle_specs['veh1']['dist_bump_ant'] - vehicle_specs['veh1']['length'] - vehicle_specs['veh2']['dist_bump_ant']
    df['ivs23'] = df['d23'] + vehicle_specs['veh2']['dist_bump_ant'] - vehicle_specs['veh2']['length'] - vehicle_specs['veh3']['dist_bump_ant']
    df['ivs34'] = df['d34'] + vehicle_specs['veh3']['dist_bump_ant'] - vehicle_specs['veh3']['length'] - vehicle_specs['veh4']['dist_bump_ant']
    # compute trajectories
    for i in veh_numbers:
        df['pos{}'.format(i)] = df['veh{}'.format(i)].cumsum().multiply(0.1)
    # smooth trajectories
    for i in veh_numbers:
        df['pos{}'.format(i)] = df['pos{}'.format(i)].rolling(window=11, center=True).mean()
    # compute speed
    for i in veh_numbers:
        df['speed{}'.format(i)] = df['pos{}'.format(i)].diff().multiply(10)
    # compute acceleration
    for i in veh_numbers:
        df['acc{}'.format(i)] = df['speed{}'.format(i)].diff().multiply(10)
    # calculate headway (front bumper to front bumper)
    df['hw12'] = (df['d12'] + vehicle_specs['veh1']['dist_bump_ant'] - vehicle_specs['veh2']['dist_bump_ant']) / df['speed2']
    df['hw23'] = (df['d23'] + vehicle_specs['veh2']['dist_bump_ant'] - vehicle_specs['veh3']['dist_bump_ant']) / df['speed3']
    df['hw34'] = (df['d34'] + vehicle_specs['veh3']['dist_bump_ant'] - vehicle_specs['veh4']['dist_bump_ant']) / df['speed4']

    # drop unnecessary columns
    df = df[['time', 'ivs12', 'ivs23', 'ivs34', 'pos1', 'pos2',
             'pos3', 'pos4', 'speed1', 'speed2', 'speed3', 'speed4',
             'acc1', 'acc2', 'acc3', 'acc4', 'hw12', 'hw23', 'hw34']]
    # rename columns
    df = df.rename(columns={'time': 'time', 'ivs12': 'ivs1', 'ivs23': 'ivs2', 'ivs34': 'ivs3',
                            'pos1': 'xL', 'pos2': 'x1', 'pos3': 'x2', 'pos4': 'x3', 'speed1': 'vL',
                            'speed2': 'v1', 'speed3': 'v2', 'speed4': 'v3', 'acc1': 'aL', 'acc2': 'a1',
                            'acc3': 'a2', 'acc4': 'a3', 'hw12': 'hL1', 'hw23': 'h12', 'hw34': 'h23'})
    # add 0-column for 4th vehicle (necessary because the methods that assess the properties work with 5 vehicles)
    df[['ivs4', 'x4', 'v4', 'a4', 'h34']] = [0, 0, 0, 0, 0]
    return df
