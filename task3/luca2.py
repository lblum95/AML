# Load NeuroKit and other useful packages
import matplotlib
import neurokit2 as nk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jedi.api.refactoring import inline


# Read in data for training and testing
x_train = pd.read_csv("data/X_train.csv", index_col=0, header=0, low_memory=False)
y_train = pd.read_csv("data/y_train.csv", index_col=0, header=0)
x_test = pd.read_csv("data/X_test.csv", index_col=0, header=0, low_memory=False)

#get lengths of signals for each sample

lengths = []
width = x_train.shape[1]

for row in range(x_train.shape[0]):
    temp_width = width
    for item in x_train.loc[row][::-1]:
        if not pd.isna(item) and (isinstance(item, float) or isinstance(item, int)):
            temp_width -= 1
            break

        temp_width -= 1

    lengths.append(temp_width)


plt.rcParams['figure.figsize'] = [8, 5]  # Bigger images

#Copied from https://neurokit2.readthedocs.io/en/latest/examples/ecg_delineate.html

# Retrieve ECG data from data folder (sampling rate= 1000 Hz)
ecg_signal = x_train.loc[0][:lengths[0]+1]
# Extract R-peaks locations
_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=300)

print(rpeaks)

# Visualize R-peaks in ECG signal
plot = nk.events_plot(rpeaks['ECG_R_Peaks'], ecg_signal)

# Zooming into the first 5 R-peaks
plot = nk.events_plot(rpeaks['ECG_R_Peaks'][:5], ecg_signal[:rpeaks['ECG_R_Peaks'][4]])

# Delineate the ECG signal
_, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300)

# Visualize the T-peaks, P-peaks, Q-peaks and S-peaks
plot = nk.events_plot([waves_peak['ECG_T_Peaks'],
                       waves_peak['ECG_P_Peaks'],
                       waves_peak['ECG_Q_Peaks'],
                       waves_peak['ECG_S_Peaks']], ecg_signal)



# Zooming into the first 3 R-peaks, with focus on T_peaks, P-peaks, Q-peaks and S-peaks
plot = nk.events_plot([waves_peak['ECG_T_Peaks'][:3],
                       waves_peak['ECG_P_Peaks'][:3],
                       waves_peak['ECG_Q_Peaks'][:3],
                       waves_peak['ECG_S_Peaks'][:3]], ecg_signal[:rpeaks['ECG_R_Peaks'][3]])




# Delineate the ECG signal and visualizing all peaks of ECG complexes
# “ECG_P_Peaks”, “ECG_Q_Peaks”, “ECG_S_Peaks”, “ECG_T_Peaks”, “ECG_P_Onsets”, “ECG_T_Offsets”

_, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, show=True, show_type='peaks')

# Delineate the ECG signal and visualizing all P-peaks boundaries
signal_peak, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, show=True, show_type='bounds_P')

# Delineate the ECG signal and visualizing all T-peaks boundaries
signal_peak, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, show=True, show_type='bounds_T')




# Delineate the ECG signal
#“ECG_P_Peaks”, “ECG_T_Peaks”, “ECG_P_Onsets”, “ECG_P_Offsets”, “ECG_T_Onsets”, “ECG_T_Offsets”, “ECG_R_Onsets”, “ECG_R_Offsets”
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, method="cwt", show=True, show_type='all')


# Visualize P-peaks and T-peaks
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, method="cwt", show=True, show_type='peaks')

# Visualize T-waves boundaries
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, method="cwt", show=True, show_type='bounds_T')

# Visualize P-waves boundaries
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, method="cwt", show=True, show_type='bounds_P')

# Visualize R-waves boundaries
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=300, method="cwt", show=True, show_type='bounds_R')

#Copied from https://neurokit2.readthedocs.io/en/latest/examples/hrv.html#Compute-HRV-features

# Find peaks
peaks, info = nk.ecg_peaks(ecg_signal, sampling_rate=300)

# Extract clean EDA and SCR features
hrv_time = nk.hrv_time(peaks, sampling_rate=300, show=True)
print(hrv_time)

hrv_freq = nk.hrv_frequency(peaks, sampling_rate=300, show=True)
print(hrv_freq)

hrv_non = nk.hrv_nonlinear(peaks, sampling_rate=300, show=True)
print(hrv_non)

hrv_indices = nk.hrv(peaks, sampling_rate=300, show=True)
print(hrv_indices)

plt.show()