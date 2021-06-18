import pandas as pd
from Laval import read_laval
from Napoli import read_napoli
from CARMA1 import read_carma1
from CARMA2 import read_cacc
from OpenACC import read_acc
from ZalaZone import read_zalazone

pd.set_option('display.max_columns', None)

names_of_datasets = {'AstaZero': {'ACC_min': ['ASta_050719_platoon1.csv', 'ASta_050719_platoon2.csv', 'ASta_040719_platoon5.csv', 'ASta_040719_platoon6.csv',
                                              'ASta_040719_platoon7.csv', 'ASta_040719_platoon8.csv', 'ASta_040719_platoon9.csv'],
                                  'ACC_max': ['ASta_040719_platoon4.csv'],
                                  'human': ['ASta_040719_platoon3.csv', 'ASta_040719_platoon10.csv']},
                     'ZalaZone': {'small_hw': ['dynamic_part1.csv', 'dynamic_part4.csv', 'dynamic_part5.csv', 'dynamic_part6.csv', 'dynamic_part7.csv',
                                               'dynamic_part12.csv', 'dynamic_part13.csv', 'dynamic_part14.csv', 'dynamic_part17.csv', 'dynamic_part20.csv',
                                               'dynamic_part21.csv', 'dynamic_part22.csv', 'dynamic_part23.csv'],
                                  'medium_hw': ['dynamic_part8.csv', 'dynamic_part9.csv'],
                                  'large_hw': ['dynamic_part2.csv', 'dynamic_part3.csv', 'dynamic_part11.csv', 'dynamic_part15.csv', 'dynamic_part16.csv', 'dynamic_part18.csv',
                                               'dynamic_part19.csv', 'dynamic_part24.csv', 'dynamic_part25.csv']},
                     'CARMA1': {'ACC': [29, 30],
                                'CACC': [68, 69, 70, 71, 72]},
                     'CARMA2': [5, 6, 9, 10, 13],
                     'Laval': ['trajectories_segment_1.csv', 'trajectories_segment_2.csv', 'trajectories_segment_3.csv',
                               'trajectories_segment_4.csv', 'trajectories_segment_5.csv', 'trajectories_segment_6.csv'],
                     'Napoli': {'urban': ['25_02_03 prB.csv', '25_02_03 PrC.csv', '30_10_02 PrA_UrbanaCorta.csv', '30_10_02 PrC_UrbanaLunga.csv'],
                                'extraurban': ['30_10_02 PrB_Extraurbana.csv']}
                     }

'''
DESIGN OF AGGREGATED DATASET

Columns:    CODE   MODE   ORIGIN   LENGTH_TIME   LENGTH_DIST   HW_SETTING    ACC/DEC   RT   SS   HW   EC   time   x1   ...

CODE: running slice number
MODE: human, ACC, CACC
CAMPAIGN
DATASET
LENGTH_TIME: time from beginning to end of slice
LENGTH_DIST: distance leading vehicle covered
HW_SETTING: S, M, L, min, max
ACC/DEC: if perturbation is an acc. or deceleration: max for acc., min for dec.
RT: 1 if suitable for RT estimation, else 0
SS: 1 if suitable for SS examination, else 0
HW: 1 if suitable, else 0
EC: running number, data that can be compared
'''

# creating a dictionary to build the dataset from
data = {'RT': {'AstaZero': {'ASta_050719_platoon1.csv': [[400, 430, 'min'], [950, 980, 'min'], [985, 1030, 'min'], [1320, 1360, 'min'], [1690, 1740, 'min']],
                            'ASta_050719_platoon2.csv': [[730, 770, 'min'], [1040, 1080, 'min']],  # 2, 5 and 6 may not work that well
                            'ASta_040719_platoon5.csv': [[260, 320, 'max'], [550, 620, 'max'], [850, 920, 'max']],
                            'ASta_040719_platoon6.csv': [[250, 320, 'max'], [550, 620, 'max']],
                            'ASta_040719_platoon7.csv': [[255, 305, 'max']],
                            'ASta_040719_platoon8.csv': [[260, 320, 'max'], [560, 630, 'max']],
                            'ASta_040719_platoon9.csv': [[595, 640, 'max']]},
               'ZalaZone': {'S': {'dynamic_part1.csv': [[35, 70, 'min'], [160, 190, 'min'], [310, 350, 'min']],  # different speed levels (11 and 8 m/s)
                                  'dynamic_part13.csv': [[260, 290, 'min'], [380, 410, 'min']]},
                            'M': {'dynamic_part8.csv': [[1070, 1100, 'min'], [1240, 1280, 'min']],
                                  'dynamic_part9.csv': [[300, 340, 'min'], [460, 500, 'min'], [660, 700, 'min']]},
                            'L': {'dynamic_part3.csv': [[105, 135, 'min'], [220, 250, 'min']],
                                  'dynamic_part15.csv': [[235, 265, 'min'], [315, 345, 'min'], [390, 430, 'min']]}},
               'CARMA1': {'ACC': [],  # maybe add CARMA1 events, but they are not that much of an enrichment
                          'CACC': []},
               'CARMA2': {'5': [[300, 345, 'max'], [390, 435, 'min']],
                          '6': [[130, 175, 'max'], [220, 265, 'min']],
                          '9': [[270, 325, 'max'], [535, 585, 'min'], [645, 690, 'max']],
                          '10': [[320, 365, 'max'], [590, 635, 'min'], [690, 735, 'max']]}},
        'HW': {'AstaZero': {'human': {'ASta_040719_platoon3.csv': [30, 650]},
                            'acc': {'ASta_040719_platoon9.csv': [40, 310]}},
               'ZalaZone': {'S': {'dynamic_part1.csv': [350, 550], 'dynamic_part13.csv': [0, 170]},  # platoon is stable for these slices
                            'M': {'dynamic_part8.csv': [1100, 1250], 'dynamic_part9.csv': [50, 300]},
                            'L': {'dynamic_part3.csv': [0, 115], 'dynamic_part15.csv': [100, 240]}},
               'CARMA1': {'acc': {'29': [60, 340], '30': [110, 650]},
                          'cacc': {'68': [100, 290], '69': [120, 320], '70': [70, 340], '71': [90, 310], '72': [120, 330]}},
               'CARMA2': {'5': [280, 460], '6': [120, 300], '9': [250, 660], '10': [320, 710]},
               'Laval': {'trajectories_segment_2.csv': [160, 260], 'trajectories_segment_3.csv': [50, 110],
                         'trajectories_segment_4.csv': [20, 160], 'trajectories_segment_5.csv': [20, 210],
                         'trajectories_segment_6.csv': [60, 200]},
               'Napoli': {'25_02_03 PrC.csv': [50, 160], '30_10_02 PrA_UrbanaCorta.csv': [85, 130], '30_10_02 PrB_Extraurbana.csv': [80, 200]}},
        'EC': {'AstaZero': {'human': {'ASta_040719_platoon3.csv': [400, 1240],  # late switching between 2 speed levels
                                      'ASta_040719_platoon10.csv': [40, 1190]},  # quite early switching between 2 speed levels
                            'acc': {'ASta_040719_platoon5.csv': [50, 1200],  # matching platoon10
                                    'ASta_040719_platoon9.csv': [50, 890]}},  # matching platoon3
               'CARMA1': {'acc': {'30': [380, 575]}, # run 30 and 71 can be compared (although acceleration is harder for cacc)
                          'cacc': {'71': [105, 300]}},  # compare run 71 with run 30 and run 9 from CARMA2
               'CARMA2': {'9': [[505, 610], [630, 720]]}},  # the carma2 run 9 slices need to be appended (to match length of CARMA1 run 71)
        }

# initialise dataframe with all columns
'''   CODE(running number)   MODE(human, acc, cacc)   ORIGIN(dataset name and run)   LENGTH_TIME(s)   LENGTH_DIST(m)   HW_ACC(S, M, L, min, max)    
      ACC/DEC   RT(1,0)   SS(1,0)   HW(1,0)   EC(0 or running number with comparable slices)   time   x1   ...   '''

col_names = ['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec',
             'time', 'xL', 'x1', 'x2', 'x3', 'x4', 'vL', 'v1', 'v2', 'v3', 'v4', 'aL', 'a1', 'a2', 'a3', 'a4',
             'ivs1', 'ivs2', 'ivs3', 'ivs4', 'hL1', 'h12', 'h23', 'h34']
agg_data = pd.DataFrame(columns=col_names)
print(agg_data.columns)

number = 0

# add slices to to dataframe
# response time (same slices used for string stability)
for i in data['RT']['AstaZero']:
    for j in data['RT']['AstaZero'][i]:
        d = read_acc(i, 0, 10000)
        d = d[d['time'] <= j[1]]
        d = d[d['time'] > j[0]]
        len_time = d.shape[0]/10
        len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
        acc_dec = ''
        if j[2] == 'min':
            acc_dec = 'dec'
        else:
            acc_dec = 'acc'
        d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
            number, 'acc', 'AstaZero', i, len_time, len_dist, 'min', acc_dec, 1, 1, 0, 0
        agg_data = agg_data.append(d)
        number += 1
for i in data['RT']['ZalaZone']:  # i is headway setting
    for j in data['RT']['ZalaZone'][i]:  # j is dataset name
        for k in data['RT']['ZalaZone'][i][j]:
            d = read_zalazone(j, 0, 10000)
            d = d[d['time'] <= k[1]]
            d = d[d['time'] > k[0]]
            len_time = d.shape[0]/10
            len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
            acc_dec = ''
            if k[2] == 'min':
                acc_dec = 'dec'
            else:
                acc_dec = 'acc'
            d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
                number, 'acc', 'ZalaZone', j, len_time, len_dist, i, acc_dec, 1, 1, 0, 0
            agg_data = agg_data.append(d)
            number += 1
for i in data['RT']['CARMA2']:  # i is run number
    for j in data['RT']['CARMA2'][i]:  # j is event
        d = read_cacc(int(i), 0, 10000)
        d = d[d['time'] <= j[1]]
        d = d[d['time'] > j[0]]
        len_time = d.shape[0] / 10
        len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
        acc_dec = ''
        if j[2] == 'min':
            acc_dec = 'dec'
        else:
            acc_dec = 'acc'
        d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
            number, 'cacc', 'CARMA2', 'run '+i, len_time, len_dist, 0, acc_dec, 1, 1, 0, 0
        agg_data = agg_data.append(d)
        number += 1

# headway
for i in data['HW']['AstaZero']:  # human or acc
    for j in data['HW']['AstaZero'][i]:  # datasets
        # print(i, j)
        d = read_acc(j, data['HW']['AstaZero'][i][j][0], data['HW']['AstaZero'][i][j][1])
        len_time = d.shape[0] / 10
        len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
        if i == 'human':
            hw_set = 0
        else:
            hw_set = 'min'
        d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
            number, i, 'AstaZero', j, len_time, len_dist, hw_set, 0, 0, 0, 1, 0
        agg_data = agg_data.append(d)
        number += 1
for i in data['HW']['ZalaZone']:  # headway S, M or L
    for j in data['HW']['ZalaZone'][i]:  # dataset
        d = read_zalazone(j, data['HW']['ZalaZone'][i][j][0], data['HW']['ZalaZone'][i][j][1])
        len_time = d.shape[0] / 10
        len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
        d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
            number, 'acc', 'ZalaZone', j, len_time, len_dist, i, 0, 0, 0, 1, 0
        agg_data = agg_data.append(d)
        number += 1
for i in data['HW']['CARMA1']:  # acc oder cacc
    for j in data['HW']['CARMA1'][i]:  # runs as str
        d = read_carma1(int(j), data['HW']['CARMA1'][i][j][0], data['HW']['CARMA1'][i][j][1])
        len_time = d.shape[0] / 20
        len_dist = round(d.iloc[-21]['xL'] - d.iloc[20]['xL'], 0)
        d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
            number, i, 'CARMA1', 'run '+j, len_time, len_dist, 0, 0, 0, 0, 1, 0
        agg_data = agg_data.append(d)
        number += 1
for i in data['HW']['CARMA2']:  # run number
    d = read_cacc(int(i), data['HW']['CARMA2'][i][0], data['HW']['CARMA2'][i][1])
    len_time = d.shape[0] / 10
    len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
    d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
        number, 'cacc', 'CARMA2', 'run '+i, len_time, len_dist, 0, 0, 0, 0, 1, 0
    agg_data = agg_data.append(d)
    number += 1
for i in data['HW']['Laval']:
    d = read_laval(i, data['HW']['Laval'][i][0], data['HW']['Laval'][i][1])
    len_time = d.shape[0] / 5
    len_dist = round(d.iloc[-6]['xL'] - d.iloc[5]['xL'], 0)
    d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
        number, 'human', 'Laval', i, len_time, len_dist, 0, 0, 0, 0, 1, 0
    agg_data = agg_data.append(d)
    number += 1
    print(d.head(15))
for i in data['HW']['Napoli']:
    d = read_napoli(i, data['HW']['Napoli'][i][0], data['HW']['Napoli'][i][1])
    len_time = d.shape[0] / 10
    len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
    d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
        number, 'human', 'Napoli', i, len_time, len_dist, 0, 0, 0, 0, 1, 0
    agg_data = agg_data.append(d)
    number += 1
    print(d.head(15))

# energy consumption
for i in data['EC']['AstaZero']:  # human or acc
    for j in data['EC']['AstaZero'][i]:  # dataset
        d = read_acc(j, data['EC']['AstaZero'][i][j][0], data['EC']['AstaZero'][i][j][1])
        len_time = d.shape[0] / 10
        len_dist = round(d.iloc[-11]['xL'] - d.iloc[10]['xL'], 0)
        if j == 'ASta_040719_platoon3.csv' or j == 'ASta_040719_platoon9.csv':
            ec = 'A'
        else:
            ec = 'B'
        if i == 'human':
            hw_set = 0
        else:
            hw_set = 'min'
        d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
            number, i, 'AstaZero', j, len_time, len_dist, hw_set, 0, 0, 0, 0, ec
        agg_data = agg_data.append(d)
        number += 1
for i in data['EC']['CARMA1']:  # acc or cacc
    for j in data['EC']['CARMA1'][i]:  # run
        d = read_carma1(int(j), data['EC']['CARMA1'][i][j][0], data['EC']['CARMA1'][i][j][1])
        len_time = d.shape[0] / 20
        len_dist = round(d.iloc[-21]['xL'] - d.iloc[20]['xL'], 0)
        ec = 'C'
        d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
            number, i, 'CARMA1', 'run '+j, len_time, len_dist, 0, 0, 0, 0, 0, ec
        agg_data = agg_data.append(d)
        number += 1
p1 = read_cacc(9, data['EC']['CARMA2']['9'][0][0], data['EC']['CARMA2']['9'][0][1])
p2 = read_cacc(9, data['EC']['CARMA2']['9'][1][0], data['EC']['CARMA2']['9'][1][1])
len_p1 = round(p1.iloc[-11]['xL'] - p1.iloc[10]['xL'], 0)
len_p2 = round(p2.iloc[-11]['xL'] - p2.iloc[10]['xL'], 0)
d = p1.append(p2)
len_time = d.shape[0] / 10
len_dist = p1+p2
ec = 'C'
d[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec', 'rt', 'ss', 'hw', 'ec']] = \
    number, 'cacc', 'CARMA2', 'run 9', len_time, len_dist, 0, 0, 0, 0, 0, ec
agg_data = agg_data.append(d)
number += 1

print(agg_data['code'].unique())

agg_data = agg_data[['code', 'mode', 'campaign', 'dataset', 'len_time', 'len_dist', 'hw_set', 'acc_dec',
                     'rt', 'ss', 'hw', 'ec', 'time', 'xL', 'x1', 'x2', 'x3', 'x4', 'vL',
                     'v1', 'v2', 'v3', 'v4', 'aL', 'a1', 'a2', 'a3', 'a4', 'ivs1', 'ivs2',
                     'ivs3', 'ivs4', 'hL1', 'h12', 'h23', 'h34']]

agg_data.to_csv('aggregated_data.csv')
