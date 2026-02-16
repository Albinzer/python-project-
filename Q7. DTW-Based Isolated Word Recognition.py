import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import dct
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns

# -------- MFCC Extraction Function --------
def extract_mfcc(file_path, num_ceps=13):
    fs, signal = wavfile.read(file_path)

    if len(signal.shape) == 2:
        signal = signal[:, 0]

    signal = signal.astype(float)

    # Pre-emphasis
    pre_emphasis = 0.97
    signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

    # Framing
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

    # Mel Filterbank
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

# -------- Load Dataset --------
dataset_path = "dataset"
words = os.listdir(dataset_path)

train_data = {}
test_files = []
true_labels = []

for word in words:
    files = os.listdir(os.path.join(dataset_path, word))
    train_files = files[:3]
    test_samples = files[3:]

    train_data[word] = [extract_mfcc(os.path.join(dataset_path, word, f))
                        for f in train_files]

    for f in test_samples:
        test_files.append(os.path.join(dataset_path, word, f))
        true_labels.append(word)

# -------- Classification --------
predicted_labels = []

for test_file in test_files:
    test_mfcc = extract_mfcc(test_file)

    min_dist = float("inf")
    predicted_word = None

    for word in words:
        for train_mfcc in train_data[word]:
            dist = dtw_distance(test_mfcc, train_mfcc)
            if dist < min_dist:
                min_dist = dist
                predicted_word = word

    predicted_labels.append(predicted_word)

# -------- Accuracy --------
acc = accuracy_score(true_labels, predicted_labels)
print("Recognition Accuracy:", round(acc*100,2), "%")

# -------- Confusion Matrix --------
cm = confusion_matrix(true_labels, predicted_labels, labels=words)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=words, yticklabels=words)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()
