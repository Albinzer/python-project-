import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

# -------- Read Speech File --------
file_path = "speech.wav"
fs, signal = wavfile.read(file_path)

if len(signal.shape) == 2:
    signal = signal[:, 0]

signal = signal.astype(float)

# -------- Framing Parameters --------
frame_size = 0.025   # 25 ms
frame_shift = 0.010  # 10 ms

frame_length = int(frame_size * fs)
frame_step = int(frame_shift * fs)

signal_length = len(signal)
num_frames = int(np.ceil((signal_length - frame_length) / frame_step)) + 1

pad_length = (num_frames - 1) * frame_step + frame_length
pad_signal = np.append(signal, np.zeros(pad_length - signal_length))

frames = np.zeros((num_frames, frame_length))

for i in range(num_frames):
    start = i * frame_step
    frames[i] = pad_signal[start:start+frame_length]

# -------- a) Compute Short-Time Energy --------
energy = np.sum(frames**2, axis=1)

# -------- Compute Zero Crossing Rate --------
zcr = np.zeros(num_frames)

for i in range(num_frames):
    frame = frames[i]
    zcr[i] = np.sum(np.abs(np.diff(np.sign(frame)))) / (2 * frame_length)

# -------- Thresholds --------
energy_threshold = 0.1 * np.max(energy)
zcr_threshold = 0.1 * np.max(zcr)

# -------- b) Detect Speech Regions --------
speech_frames = np.logical_and(energy > energy_threshold,
                               zcr > zcr_threshold)

time_axis = np.arange(num_frames) * frame_shift

# -------- Plot --------
plt.figure(figsize=(12,6))

plt.subplot(3,1,1)
plt.plot(np.arange(len(signal))/fs, signal)
plt.title("Original Speech Signal")

plt.subplot(3,1,2)
plt.plot(time_axis, energy)
plt.axhline(energy_threshold, color='r')
plt.title("Short-Time Energy")

plt.subplot(3,1,3)
plt.plot(time_axis, speech_frames.astype(int))
plt.title("Detected Speech Regions (1 = Speech, 0 = Silence)")

plt.tight_layout()
plt.show()

# -------- c) Save Detected Speech Segments --------
output_folder = "vad_segments"
os.makedirs(output_folder, exist_ok=True)

segment_count = 0
in_segment = False

for i in range(num_frames):
    if speech_frames[i] and not in_segment:
        start_frame = i
        in_segment = True

    if not speech_frames[i] and in_segment:
        end_frame = i
        in_segment = False

        start_sample = start_frame * frame_step
        end_sample = end_frame * frame_step + frame_length

        segment = pad_signal[start_sample:end_sample]
        segment = segment.astype(np.int16)

        wavfile.write(f"{output_folder}/segment_{segment_count}.wav",
                      fs, segment)

        segment_count += 1

print("Total speech segments saved:", segment_count)
