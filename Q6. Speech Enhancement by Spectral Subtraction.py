import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -------- Read Clean Speech --------
file_path = "speech.wav"   # Change file name
fs, clean = wavfile.read(file_path)

if len(clean.shape) == 2:
    clean = clean[:, 0]

clean = clean.astype(float)

# -------- Function to Compute SNR --------
def compute_snr(clean, noisy):
    noise = noisy - clean
    return 10 * np.log10(np.sum(clean**2) / np.sum(noise**2))

# -------- a) Add White Noise (SNR = 10 dB) --------
target_snr_db = 10

signal_power = np.mean(clean**2)
noise = np.random.normal(0, 1, len(clean))
noise_power = np.mean(noise**2)

# Scale noise
noise = noise * np.sqrt(signal_power / (noise_power * 10**(target_snr_db/10)))

noisy = clean + noise

snr_before = compute_snr(clean, noisy)
print("SNR before enhancement:", round(snr_before, 2), "dB")

# -------- b) Spectral Subtraction --------
frame_size = 0.02   # 20 ms
frame_shift = 0.01  # 10 ms

frame_length = int(frame_size * fs)
frame_step = int(frame_shift * fs)

signal_length = len(noisy)
num_frames = int(np.ceil((signal_length - frame_length) / frame_step)) + 1

pad_length = (num_frames - 1) * frame_step + frame_length
pad_signal = np.append(noisy, np.zeros(pad_length - signal_length))

frames = np.zeros((num_frames, frame_length))

for i in range(num_frames):
    start = i * frame_step
    frames[i] = pad_signal[start:start+frame_length]

window = np.hamming(frame_length)
enhanced_signal = np.zeros(len(pad_signal))

# Estimate noise spectrum from first few frames
noise_estimate = np.mean(np.abs(np.fft.rfft(frames[:5] * window)), axis=0)

for i in range(num_frames):
    frame = frames[i] * window
    spectrum = np.fft.rfft(frame)
    magnitude = np.abs(spectrum)
    phase = np.angle(spectrum)

    # Spectral subtraction
    clean_magnitude = magnitude - noise_estimate
    clean_magnitude = np.maximum(clean_magnitude, 0)

    clean_spectrum = clean_magnitude * np.exp(1j * phase)
    enhanced_frame = np.fft.irfft(clean_spectrum)

    start = i * frame_step
    enhanced_signal[start:start+frame_length] += enhanced_frame

enhanced_signal = enhanced_signal[:len(clean)]

snr_after = compute_snr(clean, enhanced_signal)
print("SNR after enhancement:", round(snr_after, 2), "dB")

print("SNR Improvement:", round(snr_after - snr_before, 2), "dB")

# -------- Plot Comparison --------
plt.figure(figsize=(10,6))

plt.subplot(3,1,1)
plt.plot(clean)
plt.title("Clean Speech")

plt.subplot(3,1,2)
plt.plot(noisy)
plt.title("Noisy Speech (10 dB)")

plt.subplot(3,1,3)
plt.plot(enhanced_signal)
plt.title("Enhanced Speech (Spectral Subtraction)")

plt.tight_layout()
plt.show()
