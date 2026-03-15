import numpy as np
import librosa
from config import SAMPLE_RATE, N_MFCC, MAX_PAD_LEN


def extract_features(file_path: str) -> np.ndarray:
    audio, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)

    if mfcc.shape[1] < MAX_PAD_LEN:
        pad_width = MAX_PAD_LEN - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode="constant")
    else:
        mfcc = mfcc[:, :MAX_PAD_LEN]

    return mfcc[..., np.newaxis]  # (N_MFCC, MAX_PAD_LEN, 1)
