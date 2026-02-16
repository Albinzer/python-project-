import numpy as np
import os
from scipy.io import wavfile
from scipy.fftpack import dct
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# -------- MFCC Extraction --------
def extract_mfcc(file_path, num_ceps=13):
    fs, signal = wavfile.read(file_path)

    if len(signal.shape) == 2:
        signal = signal[:, 0]

    signal = signal.astype(float)

    # Pre-emphasis
    signal = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])

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

# -------- Compute Embedding --------
def compute_embedding(mfcc):
    delta = np.diff(mfcc, axis=0)
    mean_mfcc = np.mean(mfcc, axis=0)
    mean_delta = np.mean(delta, axis=0)
    embedding = np.concatenate((mean_mfcc, mean_delta))
    return embedding

# -------- Load Dataset --------
dataset_path = "dataset_speaker"
X = []
y = []

for speaker in os.listdir(dataset_path):
    speaker_path = os.path.join(dataset_path, speaker)

    for file in os.listdir(speaker_path):
        file_path = os.path.join(speaker_path, file)
        mfcc = extract_mfcc(file_path)
        embedding = compute_embedding(mfcc)

        X.append(embedding)
        y.append(speaker)

X = np.array(X)

# -------- Train/Test Split --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# -------- Train Classifier (KNN) --------
clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train, y_train)

# -------- Evaluation --------
y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", round(accuracy*100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
