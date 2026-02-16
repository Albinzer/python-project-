import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.fftpack import dct
import os
from scipy.io import wavfile

fs = 16000   # Sampling rate
duration = 2  # seconds

# -------- Record Function --------
def record_audio(filename):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print("Saved:", filename)

# -------- MFCC Extraction --------
def extract_mfcc(signal, fs, num_ceps=13):
    signal = signal.flatten()
    signal = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])

    frame_size = 0.025
    frame_stride = 0.010

    frame_length = int(frame_size * fs)
    frame_step = int(frame_stride * fs)

    signal_length = len(signal)
    num_frames = int(np.ceil((signal_length - frame_length) / frame_step)) + 1

    pad_length = (num_frames - 1) * frame_step + frame_length
    pad_signal = np.append(signal, np.zeros(pad_length - signal_length))

    frames = np.zeros((num_frames, frame_length))

    for i in range(num_frames):
        start = i * frame_step
        frames[i] = pad_signal[start:start+frame_length]

    frames *= np.hamming(frame_length)

    NFFT = 512
    mag_frames = np.abs(np.fft.rfft(frames, NFFT))
    pow_frames = (1.0 / NFFT) * (mag_frames ** 2)

    nfilt = 26
    low_mel = 0
    high_mel = 2595 * np.log10(1 + (fs/2)/700)
    mel_points = np.linspace(low_mel, high_mel, nfilt+2)
    hz_points = 700 * (10**(mel_points/2595) - 1)
    bins = np.floor((NFFT+1) * hz_points / fs)

    fbank = np.zeros((nfilt, int(NFFT/2 + 1)))

    for m in range(1, nfilt+1):
        f_m_minus = int(bins[m-1])
        f_m = int(bins[m])
        f_m_plus = int(bins[m+1])

        for k in range(f_m_minus, f_m):
            fbank[m-1,k] = (k-bins[m-1])/(bins[m]-bins[m-1])
        for k in range(f_m, f_m_plus):
            fbank[m-1,k] = (bins[m+1]-k)/(bins[m+1]-bins[m])

    filter_banks = np.dot(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks==0, np.finfo(float).eps, filter_banks)

    log_fbank = np.log(filter_banks)
    mfcc = dct(log_fbank, type=2, axis=1, norm='ortho')[:, :num_ceps]

    return mfcc

# -------- DTW Distance --------
def dtw_distance(x, y):
    n, m = len(x), len(y)
    dtw = np.full((n+1, m+1), np.inf)
    dtw[0,0] = 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = np.linalg.norm(x[i-1] - y[j-1])
            dtw[i,j] = cost + min(dtw[i-1,j],
                                  dtw[i,j-1],
                                  dtw[i-1,j-1])
    return dtw[n,m]

# -------- Step 1: Record Templates --------
if not os.path.exists("start.wav"):
    record_audio("start.wav")
if not os.path.exists("stop.wav"):
    record_audio("stop.wav")

# Load templates
_, start_signal = wavfile.read("start.wav")
_, stop_signal = wavfile.read("stop.wav")

start_mfcc = extract_mfcc(start_signal, fs)
stop_mfcc = extract_mfcc(stop_signal, fs)

# -------- Step 2: Record Test Command --------
record_audio("test.wav")
_, test_signal = wavfile.read("test.wav")
test_mfcc = extract_mfcc(test_signal, fs)

# -------- Step 3: Classification --------
dist_start = dtw_distance(test_mfcc, start_mfcc)
dist_stop = dtw_distance(test_mfcc, stop_mfcc)

if dist_start < dist_stop:
    prediction = "START"
else:
    prediction = "STOP"

print("Predicted Command:", prediction)
