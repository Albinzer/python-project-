import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -------- Read Speech File --------
file_path = "speech.wav"   # Change file name
fs, signal = wavfile.read(file_path)

# Convert to mono if stereo
if len(signal.shape) == 2:
    signal = signal[:, 0]

# -------- Framing Parameters --------
frame_size = 0.025   # 25 ms
frame_shift = 0.010  # 10 ms

frame_length = int(frame_size * fs)
frame_step = int(frame_shift * fs)

signal_length = len(signal)
num_frames = int(np.ceil((signal_length - frame_length) / frame_step)) + 1

# -------- Zero Padding --------
pad_length = (num_frames - 1) * frame_step + frame_length
pad_signal = np.append(signal, np.zeros(pad_length - signal_length))

# -------- Framing --------
frames = np.zeros((num_frames, frame_length))
for i in range(num_frames):
    start = i * frame_step
    end = start + frame_length
    frames[i] = pad_signal[start:end]

# -------- Apply Hamming Window --------
window = np.hamming(frame_length)
windowed_frames = frames * window

# -------- STFT using rFFT --------
stft_matrix = np.fft.rfft(windowed_frames, axis=1)
magnitude = np.abs(stft_matrix)

# -------- Convert to dB --------
magnitude_db = 20 * np.log10(magnitude + 1e-10)  # Avoid log(0)

# -------- Time and Frequency Axes --------
time_axis = np.arange(num_frames) * frame_shift
freq_axis = np.fft.rfftfreq(frame_length, 1/fs)

# -------- Plot Spectrogram --------
plt.figure(figsize=(10,6))
plt.pcolormesh(time_axis, freq_axis, magnitude_db.T, shading='gouraud')
plt.title("Spectrogram (STFT)")
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Magnitude (dB)")
plt.tight_layout()
plt.show()
