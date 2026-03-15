import numpy as np
import json
import os
import tensorflow as tf
from backend.features import batch_extract

MODEL_PATH = 'ml/model.h5'
LABEL_MAP_PATH = 'ml/label_map.json'

_model = None
_label_map = None


def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model


def get_label_map():
    global _label_map
    if _label_map is None:
        with open(LABEL_MAP_PATH) as f:
            _label_map = json.load(f)
    return _label_map


def predict_npz(npz_bytes: bytes) -> dict:
    """
    Принимает байты .npz файла с массивами test_x и test_y.
    Возвращает словарь с accuracy, loss, предсказаниями и метками.
    """
    import io
    data = np.load(io.BytesIO(npz_bytes), allow_pickle=True)
    test_x = data['test_x']
    test_y = data['test_y'].astype(np.int32)

    X = batch_extract(test_x)
    model = get_model()

    probs = model.predict(X)               # (N, num_classes)
    preds = np.argmax(probs, axis=1)       # (N,)
    confidence = np.max(probs, axis=1)     # (N,) — уверенность по каждой записи

    correct = (preds == test_y)
    accuracy = float(np.mean(correct))

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy()
    loss = float(loss_fn(test_y, probs).numpy())

    label_map = get_label_map()

    return {
        'accuracy': round(accuracy, 4),
        'loss': round(loss, 4),
        'predictions': preds.tolist(),
        'true_labels': test_y.tolist(),
        'confidence': confidence.tolist(),
        'correct': correct.tolist(),
        'label_map': label_map,
        'num_records': len(test_x)
    }
