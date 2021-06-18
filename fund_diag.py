import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from OpenACC import read_acc
from CARMA2 import read_cacc


# attempt to compute flow and density of a platoon and show the relation in a fundamental diagram
def fd(df):
    print(df.columns)

    # compute instantaneous flow from avg headway
    # 5 vehicles -> 4 headways per time step (ivs+5)/v
    # flow = 1/h_avg(t)

    # recompute headway with default vehicle length of 5 m
    for i in range(1, 5):
        df['h_5-{}'.format(i)] = (df['ivs{}'.format(i)] + 5) / df['v{}'.format(i)]
    # compute instantaneous flow with average of headways
    df['h_avg(t)'] = (df['h_5-1'] + df['h_5-2'] + df['h_5-3'] + df['h_5-4']) / 4
    df['inst_flow(t)'] = 1 / df['h_avg(t)']

    # compute instantaneous density from avg spacing
    # 5 vehicles -> 4 ivs + default length of 5m
    # density = 1/s_avg(t)

    # compute spacing with default vehicle length of 5 m
    for i in range(1, 5):
        df['space_5-{}'.format(i)] = df['ivs{}'.format(i)] + 5
    # compute instantaneous density with average of spacings
    df['s_avg(t)'] = (df['space_5-1'] + df['space_5-2'] + df['space_5-3'] + df['space_5-4']) / 4
    df['inst_density(t)'] = 1 / df['s_avg(t)']

    # speed is flow/density
    df['inst_speed(t)'] = df['inst_flow(t)'] / df['inst_density(t)']

    # plot FD with instantaneous values and colormap over time
    fig = plt.figure()
    fig.set_size_inches(7, 6)
    fig.suptitle('Density, flow and fundamental diagram', y=0.94)

    cmap='turbo'

    spec = gridspec.GridSpec(ncols=1, nrows=3,
                             width_ratios=[1], wspace=0.2,
                             hspace=0.4, height_ratios=[1, 1, 3])

    ax1 = fig.add_subplot(spec[0])
    ax2 = fig.add_subplot(spec[1])
    ax3 = fig.add_subplot(spec[2])

    ax1.scatter(df['time'], df['inst_flow(t)']*3600, label='Flow (veh/h)', s=1, c=df['time'], cmap=cmap)
    ax1.set_ylabel('instantaneous\nflow (veh/h)')

    ax2.scatter(df['time'], df['inst_density(t)']*1000, label='Density (veh/km)', s=1, c=df['time'], cmap=cmap)
    ax2.set_ylabel('instantaneous\ndensity (veh/km)')
    ax2.set_xlabel('time (s)')

    ax3.scatter(df['inst_density(t)']*1000, df['inst_flow(t)']*3600, c=df['time'], cmap=cmap, s=1)
    ax3.set_ylim(0, 3500)
    ax3.set_xlim(0, 100)
    ax3.set_ylabel('flow (veh/h)')
    ax3.set_xlabel('density (veh/km)')


df_test = read_acc('ASta_050719_platoon1.csv', 400, 520)
fd(df_test)