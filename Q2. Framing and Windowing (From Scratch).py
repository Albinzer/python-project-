import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -------- Read Speech File --------
file_path = "speech.wav"   # Change file name
fs, signal = wavfile.read(file_path)

# If stereo → convert to mono
if len(signal.shape) == 2:
    signal = signal[:, 0]

# -------- Convert ms to samples --------
frame_size = 0.025   # 25 ms
frame_shift = 0.010  # 10 ms

frame_length = int(frame_size * fs)
frame_step = int(frame_shift * fs)

signal_length = len(signal)

# -------- Calculate number of frames --------
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

print("Total number of frames:", num_frames)

# -------- Apply Hamming Window --------
hamming_window = np.hamming(frame_length)
windowed_frames = frames * hamming_window

# -------- Plot Two Sample Frames --------
plt.figure(figsize=(10,5))

# Before window
plt.subplot(2,1,1)
plt.plot(frames[10])
plt.title("Frame Before Windowing")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

# After window
plt.subplot(2,1,2)
plt.plot(windowed_frames[10])
plt.title("Frame After Hamming Window")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()
