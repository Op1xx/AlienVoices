import sys; sys.path.insert(0, '.')
import numpy as np
import io
import pytest
from unittest.mock import patch, MagicMock
from backend.features import batch_extract, N_MFCC


def _make_npz_bytes(n=5, num_classes=3):
    """Создаёт синтетический .npz с фиктивными данными"""
    # Заглушка: test_x — массив нулевых байтов (batch_extract перехватим моком)
    test_x = np.zeros(n, dtype=object)
    test_y = np.array([i % num_classes for i in range(n)], dtype=np.int32)
    buf = io.BytesIO()
    np.savez(buf, test_x=test_x, test_y=test_y)
    return buf.getvalue()


def test_batch_extract_shape():
    """batch_extract должен вернуть (N, N_MFCC) даже при ошибках в записях"""
    dummy = np.zeros(4, dtype=object)
    result = batch_extract(dummy)
    assert result.shape == (4, N_MFCC)


def test_batch_extract_zeros_on_error():
    """При невалидных байтах должны возвращаться нули, не бросать исключение"""
    dummy = np.array([b'not_a_wav', b'garbage'], dtype=object)
    result = batch_extract(dummy)
    assert result.shape == (2, N_MFCC)
    assert np.all(result == 0)
