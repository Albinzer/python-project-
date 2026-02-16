import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -------- Read Speech File --------
file_path = "speech.wav"   # Change file name
fs, signal = wavfile.read(file_path)

if len(signal.shape) == 2:
    signal = signal[:, 0]

signal = signal.astype(float)

# -------- Framing Parameters --------
frame_size = 0.03     # 30 ms (better for pitch)
frame_shift = 0.01    # 10 ms

frame_length = int(frame_size * fs)
frame_step = int(frame_shift * fs)

signal_length = len(signal)
num_frames = int(np.ceil((signal_length - frame_length) / frame_step)) + 1

pad_length = (num_frames - 1) * frame_step + frame_length
pad_signal = np.append(signal, np.zeros(pad_length - signal_length))

frames = np.zeros((num_frames, frame_length))

for i in range(num_frames):
    start = i * frame_step
    end = start + frame_length
    frames[i] = pad_signal[start:end]

# -------- Energy for Voiced/Unvoiced --------
energy = np.sum(frames**2, axis=1)
energy_threshold = 0.01 * np.max(energy)

# -------- Pitch Estimation --------
pitch = np.zeros(num_frames)

min_f0 = 80     # Minimum pitch (Hz)
max_f0 = 400    # Maximum pitch (Hz)

min_lag = int(fs / max_f0)
max_lag = int(fs / min_f0)

for i in range(num_frames):
    if energy[i] > energy_threshold:   # Voiced frame
        
        frame = frames[i]
        autocorr = np.correlate(frame, frame, mode='full')
        autocorr = autocorr[len(autocorr)//2:]  # Keep positive lags
        
        autocorr[:min_lag] = 0  # Ignore small lags
        
        peak_lag = np.argmax(autocorr[min_lag:max_lag]) + min_lag
        
        pitch[i] = fs / peak_lag
    else:
        pitch[i] = 0  # Unvoiced

# -------- Time Axis --------
time_axis = np.arange(num_frames) * frame_shift

# -------- Plot Pitch Contour --------
plt.figure(figsize=(10,5))
plt.plot(time_axis, pitch)
plt.title("Pitch Contour (F0 vs Time)")
plt.xlabel("Time (seconds)")
plt.ylabel("Fundamental Frequency (Hz)")
plt.ylim(0, 500)
plt.grid()
plt.show()
