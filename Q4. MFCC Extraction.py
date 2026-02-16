import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import dct

# -------- Read Speech File --------
file_path = "speech.wav"   # Change file name
fs, signal = wavfile.read(file_path)

if len(signal.shape) == 2:
    signal = signal[:, 0]

signal = signal.astype(float)

# -------- 1. Pre-emphasis --------
pre_emphasis = 0.97
emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

# -------- 2. Framing --------
frame_size = 0.025
frame_stride = 0.010

frame_length = int(frame_size * fs)
frame_step = int(frame_stride * fs)

signal_length = len(emphasized_signal)
num_frames = int(np.ceil((signal_length - frame_length) / frame_step)) + 1

pad_length = (num_frames - 1) * frame_step + frame_length
pad_signal = np.append(emphasized_signal, np.zeros(pad_length - signal_length))

frames = np.zeros((num_frames, frame_length))

for i in range(num_frames):
    start = i * frame_step
    end = start + frame_length
    frames[i] = pad_signal[start:end]

# -------- 3. Hamming Window --------
frames *= np.hamming(frame_length)

# -------- 4. FFT and Power Spectrum --------
NFFT = 512
mag_frames = np.absolute(np.fft.rfft(frames, NFFT))
pow_frames = (1.0 / NFFT) * (mag_frames ** 2)

# -------- 5. Mel Filterbank --------
nfilt = 26

low_freq_mel = 0
high_freq_mel = 2595 * np.log10(1 + (fs / 2) / 700)

mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)
hz_points = 700 * (10**(mel_points / 2595) - 1)
bin = np.floor((NFFT + 1) * hz_points / fs)

fbank = np.zeros((nfilt, int(NFFT / 2 + 1)))

for m in range(1, nfilt + 1):
    f_m_minus = int(bin[m - 1])
    f_m = int(bin[m])
    f_m_plus = int(bin[m + 1])

    for k in range(f_m_minus, f_m):
        fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
    for k in range(f_m, f_m_plus):
        fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])

filter_banks = np.dot(pow_frames, fbank.T)
filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)

# -------- 6. Log --------
log_fbank = np.log(filter_banks)

# -------- 7. DCT → 13 MFCCs --------
num_ceps = 13
mfcc = dct(log_fbank, type=2, axis=1, norm='ortho')[:, :num_ceps]

print("MFCC shape:", mfcc.shape)

# -------- Plot MFCC Heatmap --------
plt.figure(figsize=(10,6))
plt.imshow(mfcc.T, aspect='auto', origin='lower')
plt.title("MFCC (13 Coefficients)")
plt.xlabel("Frame Index")
plt.ylabel("MFCC Coefficient Index")
plt.colorbar(label="Amplitude")
plt.tight_layout()
plt.show()
