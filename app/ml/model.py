import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from config import MODEL_PATH, N_MFCC, MAX_PAD_LEN, NUM_CLASSES, EPOCHS, BATCH_SIZE


def build_model() -> keras.Model:
    inputs = keras.Input(shape=(N_MFCC, MAX_PAD_LEN, 1))

    x = keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(inputs)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dense(128, activation="relu")(x)
    x = keras.layers.Dropout(0.3)(x)
    outputs = keras.layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_model(X: np.ndarray, y: np.ndarray) -> keras.Model:
    model = build_model()
    model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2)
    model.save(MODEL_PATH)
    return model


def load_model() -> keras.Model:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Модель не найдена: {MODEL_PATH}")
    return keras.models.load_model(MODEL_PATH)


def predict(model: keras.Model, features: np.ndarray) -> tuple[int, float]:
    features = features[np.newaxis, ...]  # добавляем batch dimension
    probs = model.predict(features, verbose=0)[0]
    class_id = int(np.argmax(probs))
    confidence = float(probs[class_id])
    return class_id, confidence
