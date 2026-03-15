import numpy as np
import librosa
import io

N_MFCC = 40


def wav_bytes_to_mfcc(wav_bytes: bytes, sr: int = 22050) -> np.ndarray:
    """
    Принимает байты wav-файла.
    Возвращает усреднённый вектор MFCC размером (N_MFCC,).
    """
    y, sr = librosa.load(io.BytesIO(wav_bytes), sr=sr, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    return np.mean(mfcc.T, axis=0).astype(np.float32)


def batch_extract(wav_array: np.ndarray) -> np.ndarray:
    """
    Принимает массив numpy, где каждый элемент — байты wav-файла.
    Возвращает матрицу признаков (N, N_MFCC).
    """
    features = []
    for i, wav in enumerate(wav_array):
        try:
            features.append(wav_bytes_to_mfcc(bytes(wav)))
        except Exception as e:
            print(f"Ошибка в записи {i}: {e}")
            features.append(np.zeros(N_MFCC, dtype=np.float32))
    return np.array(features)
