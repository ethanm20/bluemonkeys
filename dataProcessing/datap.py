import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from CSIKit.reader import get_reader
from CSIKit.util import csitools
from CSIKit.filters.passband import lowpass
from CSIKit.filters.statistical import running_mean
from CSIKit.util.filters import hampel
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error


def get_pcap_df(pcap_file):
    my_reader = get_reader(pcap_file)
    csi_data = my_reader.read_file(pcap_file)
    csi_matrix, no_frames, no_subcarriers = csitools.get_CSI(csi_data, metric='amplitude')
    csi_matrix_first = csi_matrix [:, :, 0, 0]
    csi_matrix_squeezd = np.squeeze(csi_matrix_first)
    finite_mask = np.isfinite(csi_matrix_squeezd).all(axis=1)
    csi_matrix_squeezd = csi_matrix_squeezd[finite_mask]

    for x in range(len(csi_matrix_squeezd)):
        csi_matrix_squeezd[x] = lowpass(csi_matrix_squeezd[x], 10, 100, 5)
        csi_matrix_squeezd[x] = hampel(csi_matrix_squeezd[x], 10, 3)
        csi_matrix_squeezd[x] = running_mean(csi_matrix_squeezd[x], 10)

    null_subcarriers = [-64, -63, -62, -61, -60, -59, -1, 0, 1, 59, 60, 61, 62, 63]
    pilot_subcarriers = [11, 25, 53, -11, -25, -53]
    removed_subcarriers = null_subcarriers + pilot_subcarriers
    removed_subcarriers.sort(reverse=True)

    for i in removed_subcarriers:
        csi_matrix_squeezd = np.delete(csi_matrix_squeezd, i + 64, 1)

    # get the average value of the subcarriers
    df_csi = pd.DataFrame(csi_matrix_squeezd.mean(axis=1), columns=['csi'])

    # # 13th sub carrier
    # df_csi = pd.DataFrame(csi_matrix_squeezd[:, 13 + 64], columns=['csi'])
    return df_csi

def combine_pcap(path_to_dir, file_prefix, file_suffix):
    files = []
    with os.scandir(path_to_dir) as entries:
        for entry in entries:
           if entry.name.endswith(file_suffix) and entry.name.startswith(file_prefix):
                files.append(entry.name)
    # assumes that the files have some kind of naming order
    files.sort()
    dfs = []
    for pcap_file in files:
        dfs.append(get_pcap_df(path_to_dir + '/' + pcap_file)) 
    if len(dfs) <= 0:
        return
    df_final = dfs.pop(0)
    while len(dfs) > 0:
        df_final = df_final._append(dfs.pop(0), ignore_index=True)
    df_final.to_csv(file_prefix + '_csi' +'.csv')

def get_temp_df(temp_file):
    columns = ['time', 'temp']
    df_temp = pd.read_csv(temp_file, header=None, names=columns)
    return df_temp

def get_df_csv(csi_file, column_names_list):
    df = pd.read_csv(csi_file, header=None, names=column_names_list)
    return df

def csvs_from_csi_temp(path_to_dir, csi_file, temp_file):
    df_temp = get_temp_df(path_to_dir + '/' + temp_file)
    csi_file = path_to_dir + '/' + csi_file
    # assumes the csv file came from the combine_pcap function which
    # returns a csv file with averaged out csi
    df_csi = None
    if (csi_file.endswith('.csv')):
        df_csi = get_df_csv(csi_file, ['csi'])
    else:
        df_csi = get_pcap_df(csi_file)
    return df_csi, df_temp


# combine the csi and temp
def combine_average_df(df_csi, df_temp):
    interval_size = len(df_csi) / len(df_temp)
    df_csi['group'] = df_csi.index // interval_size
    df_avg_csi = df_csi.groupby('group').mean().reset_index()
    if (len(df_avg_csi) > len(df_temp)):
        df_avg_csi = df_avg_csi.head(len(df_temp))
    else:
        df_temp = df_temp.head(len(df_avg_csi))
    df_combined = pd.concat([df_temp.reset_index(drop=True), df_avg_csi], axis=1)
    return df_combined

def train_ml(df_combined, model=None):
    # # # now the machine learning
    x_rf = df_combined[['temp']]
    y_rf = df_combined['csi']
    if model == None:
        model = RandomForestRegressor()
    # model = LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(x_rf, y_rf, test_size=0.5, random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    # kfold training
    kf = KFold(n_splits=5, shuffle=True, random_state=0)

    # Perform K-Fold Cross-Validation
    for train_index, test_index in kf.split(df_combined):
        # Split data
        X_train, X_test = df_combined[['temp']].iloc[train_index], df_combined[['temp']].iloc[test_index]
        Y_train, Y_test = df_combined['csi'].iloc[train_index], df_combined['csi'].iloc[test_index]

        # Train the model
        model.fit(X_train, Y_train)

    return (x_test, y_test, model)

def graph_ml(x_test, y_test, model):
    # machine learning graphing
    plt.scatter(x_test, y_test, color='blue')
    y_pred = model.predict(x_test)
    plt.scatter(x_test, y_pred, color='red')
    plt.legend()
    plt.show()

def get_regression(df_combined):
    # polynomial
    model = np.poly1d(np.polyfit(df_combined['csi'], df_combined['temp'], 3))
    polyline = np.linspace(min(df_combined['csi']), max(df_combined['csi']), 1000)
    print(polyline)
    plt.scatter(df_combined['csi'], df_combined['temp'])
    plt.plot(polyline, model(polyline))
    plt.show()

def train_with_all_files(path_to_dir, prefix=''): 
    files = []
    with os.scandir(path_to_dir) as entries:
        for entry in entries:
            if entry.name.endswith('.csv') or entry.name.endswith('pcap'):
                if (entry.name.startswith(prefix)):
                    print('test', entry.name)
                    files.append(entry.name)
    files.sort()
    new_files = []
    grouped_files = []
    for i in range(len(files)):
        if (i % 2):
            new_files.append(files[i])
            grouped_files.append(new_files)
        else:
            new_files = [files[i]]
    df_combines = []
    for i in grouped_files:
        df_csi, df_temp = csvs_from_csi_temp(path_to_dir, i[1], i[0])
        df_combines.append(combine_average_df(df_csi, df_temp))
    new_df = pd.DataFrame()
    for i in df_combines:
        new_df = pd.concat([new_df, i])
    (x_test, y_test, model) = train_ml(new_df) 
    graph_ml(x_test, y_test, model)

       

if __name__ == "__main__":
    train_with_all_files('../dataCollection', prefix='heated_1-7')