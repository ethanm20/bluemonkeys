import numpy as np
import pandas as pd
from hampel import hampel
import scipy.signal as signal
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import seaborn as sns
import scipy.stats as stats
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

columns = ['time', 'temp', 'rh']
df = pd.read_csv('./sample_temps.csv', header=None, names=columns)
# apply hample filter
# imputation = true replaces outliers with median value
filtered_cols = hampel(df['rh'], window_size=5, n=3, imputation=True)
# create a mask and only keep values that are equal so we get rid of the outliers
mask = (df['rh'] == filtered_cols)
filtered_df = df[mask]

# lowpass filter

fs = 1000
cutoff = 10
nyquist = 0.5 * fs
order = 4
normal_cutoff = cutoff / nyquist

b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
filtered_signal = signal.filtfilt(b, a, df['rh'])
df['rh'] = filtered_signal



# # now the machine learning
x_rf = df[['rh']]
y_rf = df[['temp']]

# model = RandomForestRegressor()
# model = LinearRegression()
# x_train, x_test, y_train, y_test = train_test_split(x_rf, y_rf, test_size=0.5, random_state=42)
# model.fit(x_train, y_train)
# y_pred = model.predict(x_test)

# polynomial
model = np.poly1d(np.polyfit(df['rh'], df['temp'], 3))
polyline = np.linspace(min(df['rh']), max(df['rh']), 1000)
# print(polyline)
plt.scatter(df['rh'], df['temp'])
plt.plot(polyline, model(polyline))
plt.show()


print(model)
print(r2_score(df['rh'], df['temp']))
