import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# ---------- Read WAV File ----------
file_path = "speech.wav"   # Replace with your file name
sampling_rate, data = wavfile.read(file_path)

# If stereo, convert to mono
if len(data.shape) == 2:
    data = data[:, 0]

# ---------- Basic Information ----------
num_samples = len(data)
duration = num_samples / sampling_rate
max_amp = np.max(data)
min_amp = np.min(data)

print("Sampling Rate:", sampling_rate, "Hz")
print("Number of Samples:", num_samples)
print("Duration:", duration, "seconds")
print("Maximum Amplitude:", max_amp)
print("Minimum Amplitude:", min_amp)

# # ---------- Time Axis ----------
# time = np.linspace(0, duration, num_samples)

# # ---------- Plot Waveform ----------
# plt.figure()
# plt.plot(time, data)
# plt.title("Speech Signal - Time Domain")
# plt.xlabel("Time (seconds)")
# plt.ylabel("Amplitude")
# plt.grid()
# plt.show()

# # ---------- FFT ----------
# fft_values = np.fft.fft(data)
# fft_magnitude = np.abs(fft_values)

# # Frequency axis
# freq = np.fft.fftfreq(num_samples, 1/sampling_rate)

# # Take only positive frequencies
# positive_freq = freq[:num_samples//2]
# positive_magnitude = fft_magnitude[:num_samples//2]

# # ---------- Plot Magnitude Spectrum ----------
# plt.figure()
# plt.plot(positive_freq, positive_magnitude)
# plt.title("Magnitude Spectrum (FFT)")
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Magnitude")
# plt.grid()
# plt.show()
