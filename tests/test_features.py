import sys; sys.path.insert(0, '.')
import numpy as np
import soundfile as sf
import io
from backend.features import wav_bytes_to_mfcc, N_MFCC


def _make_dummy_wav(duration=1.0, sr=22050):
    """Создаёт синтетический wav-файл для тестов"""
    samples = np.random.randn(int(sr * duration)).astype(np.float32)
    buf = io.BytesIO()
    sf.write(buf, samples, sr, format='WAV')
    return buf.getvalue()


def test_mfcc_shape():
    wav = _make_dummy_wav()
    features = wav_bytes_to_mfcc(wav)
    assert features.shape == (N_MFCC,)


def test_mfcc_is_float32():
    wav = _make_dummy_wav()
    features = wav_bytes_to_mfcc(wav)
    assert features.dtype == np.float32


def test_mfcc_no_nan():
    wav = _make_dummy_wav()
    features = wav_bytes_to_mfcc(wav)
    assert not np.any(np.isnan(features))
