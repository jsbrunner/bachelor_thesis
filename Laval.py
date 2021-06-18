import pandas as pd
import matplotlib.pyplot as plt
import lowess
from plots import plot_xvah

pd.set_option('display.max_columns', None)


# function reading data sets from the Laval et al. 2014 platooning campaign
def read_laval(filename, t_start, t_end):
    df = pd.read_csv(filename, sep=';')
    df = df.drop(columns=['Unnamed: 7', 'Unnamed: 8'])
    df = df.apply(lambda x: x.str.replace(',','.'))
    df = df.astype('float64')

    # crop data to start and end time
    df = df[df['LOCAL TIME'] < t_end]
    df = df[df['LOCAL TIME'] >= t_start]
    platoon_vehicles = ['Laval', 'Felipe', 'Toth', 'Rama', 'Hyun', 'Joy']

    # smooth trajectories
    for i in platoon_vehicles:
        df[i] = df[i].rolling(window=11, center=True).mean()
    # compute speed from trajectories
    for i in platoon_vehicles:
        # df[i] = lowess.lowess(df['LOCAL TIME'], df[i], bandwidth=(1 / df.shape[0]) * 10, polynomialDegree=1)
        df['{} Speed'.format(i)] = df[i].diff().multiply(5)
    # compute acceleration
    for i in platoon_vehicles:
        df['{} Acc.'.format(i)] = df['{} Speed'.format(i)].diff().multiply(5)
    # compute ivs (assuming an average vehicle length of 4.5 meters)
    for i in range(0, 5):
        df['ivs{}'.format(platoon_vehicles[i+1])] = df['{}'.format(platoon_vehicles[i])] - df['{}'.format(platoon_vehicles[i+1])] - 5
    # compute headway
    for i in range(0, 5):
        df['hw{}'.format(platoon_vehicles[i+1])] = (df['{}'.format(platoon_vehicles[i])] - df['{}'.format(platoon_vehicles[i+1])]) / df['{} Speed'.format(platoon_vehicles[i+1])]

    print(df.columns)

    # drop unnecessary columns
    df = df[['LOCAL TIME', 'Laval', 'Felipe', 'Toth', 'Rama', 'Hyun',
             'Laval Speed', 'Felipe Speed', 'Toth Speed', 'Rama Speed', 'Hyun Speed',
             'Laval Acc.', 'Felipe Acc.', 'Toth Acc.', 'Rama Acc.',
             'Hyun Acc.', 'ivsFelipe', 'ivsToth', 'ivsRama', 'ivsHyun',
             'hwFelipe', 'hwToth', 'hwRama', 'hwHyun']]
    # rename columns
    df = df.rename(columns={'LOCAL TIME': 'time', 'Laval': 'xL', 'Felipe': 'x1', 'Toth': 'x2', 'Rama': 'x3', 'Hyun': 'x4',
                            'Laval Speed': 'vL', 'Felipe Speed': 'v1', 'Toth Speed': 'v2', 'Rama Speed': 'v3', 'Hyun Speed': 'v4',
                            'Laval Acc.': 'aL', 'Felipe Acc.': 'a1', 'Toth Acc.': 'a2', 'Rama Acc.': 'a3', 'Hyun Acc.': 'a4',
                            'ivsFelipe': 'ivs1', 'ivsToth': 'ivs2', 'ivsRama': 'ivs3', 'ivsHyun': 'ivs4',
                            'hwFelipe': 'hL1', 'hwToth': 'h12', 'hwRama': 'h23', 'hwHyun': 'h34'})

    print(df.columns)
    return df
