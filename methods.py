import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from math import sin, cos, sqrt, atan2, radians
from scipy import signal
import scipy

pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)


# attempt to automatically detect perturbation events in the data -> method does work in some cases but it is not reliable; perturbation events are therefore determined manually for this work
def find_perturbations(df, dv_threshold, stable_time, perturbation_length):
    # find periods with low speed difference
    df['d_v'] = df['Speed1'] - df['Speed2']
    df['stab_flag'] = df['d_v'].apply(lambda x: 1 if abs(x) <= dv_threshold else 0)

    # find perturbation events where low speed difference is maintained for some seconds
    count = 0
    pert = {'start': [], 'end': []}
    for index, row in df.iterrows():
        if count >= stable_time and row['stab_flag'] == 0:  # if the speed difference is low for at least 4 seconds, the platoon can be considered stable
            pert['start'].append(row['Time'] - stable_time)  # set perturbation interval from the beginning of stability and for the perturbation length
            pert['end'].append(row['Time'] + (perturbation_length - stable_time))
            count = 0
        if row['stab_flag'] == 1:
            count += 0.1  # summing up every 1/10 of a second where the speed difference is low
        else:
            count = 0

    return pd.DataFrame(pert)


# attempt to recreate the cross-correlation method proposed in Makridis et al. (2020b) -> not used in this work
def response_time(df_rt, perturbations, time, speed1, speed2):

    # time interval for calculating response times
    df_rt = df_rt[df_rt[time] <= 2000]
    df_rt = df_rt[df_rt[time] > 0]

    df_rt['d_v'] = df_rt[speed1]-df_rt[speed2]
    df_rt['acc1'] = df_rt[speed2].diff().multiply(10)

    def get_lag(df):
        def crosscorr(x_, y, lag=0, wrap=False):
            if wrap:
                shiftedy = y.shift(lag)
                shiftedy.iloc[:lag] = y.iloc[-lag:].values
                return x_.corr(shiftedy)
            else:
                return x_.corr(y.shift(lag))

        d1 = df['d_v']
        d2 = df['acc1']
        window = [-int(len(d1)/2), int(len(d1)/2)]
        n = window[1] - window[0]
        rs = [crosscorr(d1, d2, lag) for lag in range(window[0], window[1])]
        lag = -(len(rs)/2-np.argmax(rs))/10
        x = np.linspace(0, n/10, n)
        x_c = np.linspace(-len(rs)/2, len(rs)/2, len(rs))
        d2_corr = d2.shift(int(lag*10))

        print(f'\nOwn method maxlag: {round(lag, 1)} s, correlation = {round(max(rs), 3)}')

        # color, x, x_ccor, ccor, y1, y2, y2_corr, lag, title
        plot_rt_ccor('tab:blue', x, x_c, rs, d1, d2, d2_corr, lag*10, 'Response time estimation')

        return lag

    lags = []
    for index, row in perturbations.iterrows():
        # cut dataframe to perturbation length
        # print('OK')
        df_pert = df_rt.copy()
        df_pert.astype('float64')
        df_pert = df_pert[df_pert[time] <= row['end']]
        df_pert = df_pert[df_pert[time] > row['start']]

        # calculate get_lag for each perturbation
        lags.append(get_lag(df_pert))


# implementation of the cross-correlation method proposed by Makridis et al. (2020b)
def rt_makridis(df, time, speed1, speed2):
    lsp = df[speed1]  # speed of leading vehicle
    af = df[speed2].diff().multiply(10)  # acceleration of following vehicle
    ds = df[speed1] - df[speed2]  # speed difference between vehicles

    # set window
    start_win = int(len(lsp) / 5)
    window = [start_win, int(4 * len(lsp) / 5)]
    af_part = af[window[0]:window[1]]
    ds_part = ds[window[0]:window[1]]

    # create numpy arrays for the following computations
    npts = window[1] - window[0]
    x = np.linspace(0, npts / 10, npts)
    lags = np.arange(-npts + 1, npts)
    y1 = np.array(ds_part)
    y2 = np.array(af_part)

    # compute cross-covariance
    ccov = np.correlate(y1 - y1.mean(), y2 - y2.mean(), mode='full')

    # compute cross-correlation
    ccor = ccov / (npts * y1.std() * y2.std())

    # indentify maxlag
    maxlag = lags[np.argmax(ccor)]

    # plot original signals, cross-correlation and shifted signals
    y2_corr = np.array(af[window[0] - maxlag:window[1] - maxlag])

    x_ccor = np.linspace(-len(ccor) / 2, len(ccor) / 2, len(ccor))
    plot_rt_ccor('orangered', x, x_ccor, ccor, y1, y2, y2_corr, maxlag, 'Response Time Estimation (Makridis et al. 2020), Code: {}'.format(df['code'].iloc[0]))  # color, x, x_ccor, ccor, y1, y2, y2_corr, lag, title

    # return estimated delay and correlation coefficient
    return_list = [round(-maxlag/10, 1), round(max(ccor), 3)]
    return return_list


# implementation of the response time estimation method proposed by Lanaud et al. (2021)
def rt_lanaud(df, time, speed1, speed2, run_number=0, dt=20*1, DT=20*10, a=0.75, b=0.8, d=0.8):
    df = df.reset_index()
    h = 10  # size of time window to calculate means and std (corresponds to 1 second)

    df['mu_leader'] = df[speed1].rolling(h).mean()  # calculate rolling mean for leader's speed
    df['mu_leader'] = df['mu_leader'].shift(-(h-1), axis=0)  # .mean function writes value at the end of the rolling window but the method requires it to be at the start

    # calculate sigma
    df['sigma_leader'] = df[speed1].rolling(h).std(ddof=0)
    df['sigma_leader'] = df['sigma_leader'].shift(-(h-1), axis=0)  # same shifting for standard deviation

    # compute global standard deviation
    for i in range(len(df)-1):
        df.loc[i, 'dsigma_leader'] = df.loc[i+1, 'sigma_leader'] - df.loc[i, 'sigma_leader']  # calculate difference between sigmas for each 0.1 s
    dsigma_tot_leader = df['dsigma_leader'].std(ddof=0)  # calculate std of dsigmas

    speedchange_leader = []  # array to save timestamps where speed changes occur
    inc_prov = -1
    df['abs_dsigma_leader'] = df['dsigma_leader'].abs()

    for j in range(DT + 1, len(df) - dt):  # check if speed is stable for a longer period
        if max([df.loc[k, 'abs_dsigma_leader'] for k in range(j - DT, j)]) < a*dsigma_tot_leader:  # hier evtl. noch geringe Verschiebung um 1 wegen k
            inc = 0

            for k in range(j, j + dt):  # check if the set threshold is exceeded within a shorter time period
                if df.loc[k+1, 'abs_dsigma_leader'] > b*dsigma_tot_leader:
                    inc += 1

            if inc > d*dt:  # append speed change instant of the leader to the list
                if inc_prov == -1:
                    speedchange_leader.append(df.loc[j, time])
                    inc_prov += 1
                else:
                    if (df.loc[j, time] > speedchange_leader[inc_prov] + dt) and (df.loc[j, time] < df.iloc[-1][time] - 15):
                        speedchange_leader.append(df.loc[j, time])
                        inc_prov += 1

    # now the same procedure for the following vehicle

    df['mu_follower'] = df[speed2].rolling(h).mean()
    pd.set_option('display.max_columns', None)
    # print(df.tail(30))
    df['mu_follower'] = df['mu_follower'].shift(-(h - 1), axis=0)

    df['sigma_follower'] = df[speed2].rolling(h).std(ddof=0)
    df['sigma_follower'] = df['sigma_follower'].shift(-(h - 1), axis=0)

    for i in range(len(df) - 1):
        df.loc[i, 'dsigma_follower'] = df.loc[i + 1, 'sigma_follower'] - df.loc[i, 'sigma_follower']
    dsigma_tot_follower = df['dsigma_follower'].std(ddof=0)
    df['abs_dsigma_follower'] = df['dsigma_follower'].abs()

    speedchange_follower = []
    inc_prov = -1
    leader = 0

    for j in range(DT + 1, len(df) - dt):
        if leader < len(speedchange_leader):
            if speedchange_leader[leader] < df.loc[j, time] < speedchange_leader[leader] + 20:
                if df.loc[j+1, 'dsigma_follower'] > 0.5*b*dsigma_tot_follower:
                    inc = 0

                    for k in range(j, j + dt):
                        if df.loc[k + 1, 'abs_dsigma_follower'] > 0.5*b*dsigma_tot_follower:
                            inc += 1

                    if inc > 0.75*d*dt:
                        if inc_prov == -1:
                            speedchange_follower.append(df.loc[j, time])
                            inc_prov += 1
                            leader += 1
                        else:
                            if (df.loc[j, time] > speedchange_follower[inc_prov] + dt) and (df.loc[j, time] < df.iloc[-1][time] - 15):
                                speedchange_follower.append(df.loc[j, time])
                                inc_prov += 1
                                leader += 1

            # if speed change of follower is not within 20 seconds of the leader's speed change
            elif df.loc[j, time] > speedchange_leader[leader] + 20:
                speedchange_follower.append(-1)
                leader += 1

    # response time is differnce between detected speed change instants
    detected_rt = np.round(np.subtract(speedchange_follower, speedchange_leader), 1)

    # return list with response time, speed change instant of the leader and of the follower
    return_list = [round(detected_rt[0], 1), round(speedchange_leader[0], 1), round(speedchange_follower[0], 1)]
    return return_list


# implementation of the response time estimation method proposed by Li et al. (2021)
# which uses the oblique speed profile and wavelet transform to detect acceleration starting points
def rt_li(df, time, speed1, speed2, minmax):
    df = df.reset_index()
    speeds = [speed1, speed2]
    t_s = []

    # determine perturbation starting points for leading and following vehicles
    for s in speeds:
        # cut data at the maximum/minimum speed during the perturbation
        if minmax == 'dec':
            t_vmin_id = df[s].idxmin()
            t = df.iloc[t_vmin_id][time]
            t_speed = df.iloc[t_vmin_id][s]
        else:
            t_vmax_id = df[s].idxmax()
            t = df.iloc[t_vmax_id][time]
            t_speed = df.iloc[t_vmax_id][s]
        df_cut = df[df[time] <= t]

        # get oblique speed by subtracting a linear function from the speed
        speed_start = df_cut.iloc[0][s]
        time_start = df_cut.iloc[0][time]
        df_cut['function'] = speed_start + ((t_speed - speed_start)/(t - time_start)) * (df_cut[time] - time_start)
        df_cut[str('oblique_' + s)] = df_cut[s] - df_cut['function']

        # applying the continuous wavelet transform on the oblique speed
        widths = np.arange(1, 64)
        cwtmatr = scipy.signal.cwt(df_cut[str('oblique_' + s)], signal.ricker, widths)
        cwtmatr = np.absolute(cwtmatr)

        # average energy of wavelet transform over all scales
        cwt_avg_energy = np.absolute(cwtmatr).mean(0)
        time_axis = np.linspace(0, len(cwt_avg_energy)/10, len(cwt_avg_energy), endpoint=False)
        df_avg_energy = pd.DataFrame(list(zip(time_axis, cwt_avg_energy, cwtmatr[32], cwtmatr[60])), columns=['time', 'avg_energy', '32_energy', '60_energy'])

        # identify the time instant with the highest average wavelet energy
        index_max_energy = df_avg_energy['avg_energy'].idxmax()
        t_relevant = df_avg_energy.iloc[index_max_energy][time]
        t_s.append(t_relevant)

        # plot the procedure with speed, oblique speed, wavelet coefficients across all scales and average wavelet energy
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
        fig.set_size_inches(8, 8)
        fig.suptitle('Wavelet transform method for {}'.format(s))
        ax1.plot(df_cut[time], df_cut[s], label='Speed')
        ax1.plot(df_cut[time], df_cut['function'], label='Function')
        ax1.plot(t, t_speed, 'o', label='$T_{min}$')
        ax1.set_ylabel('Speed (m/s)')
        ax1.get_xaxis().set_visible(False)

        ax2.plot(df_cut[time], df_cut[str('oblique_' + s)], label='Oblique speed')
        ax2.set_ylabel('Oblique speed (m/s)\n(Speed - Function)')
        ax2.get_xaxis().set_visible(False)

        ax3.imshow(cwtmatr, extent=[-1, 1, 1, 64], cmap='binary', aspect='auto', label='$MIN (white) -- MAX (black)$')  # , vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max()
        ax3.get_xaxis().set_visible(False)
        ax3.set_ylabel('WT coefficients\n(absolute values)')

        ax4.plot(df_avg_energy['time'] + df.iloc[0][time], df_avg_energy['avg_energy'], label='Average wavelet energy')
        ax4.set_ylabel('Average energy\nacross scales')
        ax4.set_xlabel('Time (s)')
        ax4.set_ylim(ymin=0)
        ax4.plot(t_relevant+df.iloc[0][time], df_avg_energy.iloc[index_max_energy]['avg_energy'], 'o', color='black', label='$T_s$ (maximum)')
        ax1.plot(t_relevant+df.iloc[0][time], df_cut.iloc[index_max_energy][s], 'o', color='black', label='$T_s$')
        ax2.plot(t_relevant+df.iloc[0][time], df_cut.iloc[index_max_energy][str('oblique_' + s)], 'o', color='black', label='$T_s$')

        ax4.legend(loc='upper right', fontsize='small')
        ax2.legend(loc='upper right', fontsize='small')
        ax1.legend(loc='upper right', fontsize='small')

        fig.tight_layout()

    # plot speeds and detected points
    fig, ax_s = plt.subplots()
    fig.set_size_inches(7, 4.5)
    fig.suptitle('Response time = {} s'.format(round(t_s[1] - t_s[0], 1)), y=0.93)
    ax_s.plot(df[time], df[speed1], label='Speed leader')
    ax_s.plot(df[time], df[speed2], label='Speed follower')
    ax_s.set_ylabel('Speed (m/s)')
    ax_s.set_xlabel('Time (s)')
    ax_s.vlines(t_s[0]+df.iloc[0][time], ymin=df[speed2].min()-0.5, ymax=df[speed2].max()+0.5, linestyles='dashed', color='black')
    ax_s.vlines(t_s[1]+df.iloc[0][time], ymin=df[speed2].min()-0.5, ymax=df[speed2].max()+0.5, linestyles='dashed', color='black')
    ax_s.plot(t_s[0]+df.iloc[0][time], df[df[time] == round(t_s[0]+df.iloc[0][time], 1)][speed1], 'D', color='black')
    ax_s.text(t_s[0]+df.iloc[0][time] - 7.5, df[df[time] == round(t_s[0]+df.iloc[0][time], 1)][speed1] + 0.4, '$T_{s, leader}$')
    ax_s.plot(t_s[1]+df.iloc[0][time], df[df[time] == round(t_s[1]+df.iloc[0][time], 1)][speed2], 'D', color='black')
    ax_s.text(t_s[1]+df.iloc[0][time] + 0.9, df[df[time] == round(t_s[1]+df.iloc[0][time], 1)][speed2] + 0.2, '$T_{s, follower}$')
    ax_s.legend(loc='upper right', fontsize='small')

    # return response time and time instants where the perturbation begins for the leading and the following vehicle
    return_list = [round(t_s[1] - t_s[0], 1), round(t_s[0]+df.iloc[0][time], 1), round(t_s[1]+df.iloc[0][time], 1)]
    return return_list


# plot for the cross-correlation method
def plot_rt_ccor(color, x, x_ccor, ccor, y1, y2, y2_corr, lag, title):

    # compute ratio of standard deviations of ds and af to match plot heights afterwards
    ds_std = y1.std()
    af_std = y2.std()
    factor = ds_std / af_std

    # plot ds and af, crosscorrelation and correlated signals within window
    fig, (ax1, ax3, ax4) = plt.subplots(3, 1)
    fig.set_size_inches(8, 6.5)
    fig.suptitle(title, fontsize=16.0)
    fig.subplots_adjust(hspace=0.8)

    color_ds = 'black'
    color_af = color

    ax1.set_title('Signals measured')
    ax1.plot(x, y1, color=color_ds, label='ds')
    ax1.set_ylim(-2 * factor, 2 * factor)
    ax1.set_ylabel('Speed diff.\n(m/s)', color=color_ds)
    ax1.set_xlabel('Time (s)')
    ax1.tick_params(axis='y', labelcolor=color_ds)

    ax2 = ax1.twinx()
    ax2.plot(x, y2, color=color_af, label='af')
    ax2.set_ylim(-factor, factor)
    ax2.set_ylabel('Acc. follower\n(m/s²)', color=color_af)
    ax2.tick_params(axis='y', labelcolor=color_af)

    ax3.set_title(f'Cross-correlation between signals (max. at {round(lag/10, 1)} s)')
    ax3.plot(x_ccor, ccor, color='black')
    ax3.set_ylabel('Correlation')
    ax3.set_xlabel('Lag between time series (0.1 s)')

    ax4.set_title('Signals shifted')
    ax4.plot(x, y1, color=color_ds, label='ds')
    ax4.set_ylim(-2 * factor, 2 * factor)
    ax4.set_ylabel('Speed diff.\n(m/s)', color=color_ds)
    ax4.set_xlabel('Time (s)')
    ax4.tick_params(axis='y', labelcolor=color_ds)

    ax5 = ax4.twinx()
    ax5.plot(x, y2_corr, color=color_af, label='af_corr')
    ax5.set_ylim(-factor, factor)
    ax5.set_ylabel('Acc. follower\n(m/s²)', color=color_af)
    ax5.tick_params(axis='y', labelcolor=color_af)

    fig.tight_layout(pad=2)
