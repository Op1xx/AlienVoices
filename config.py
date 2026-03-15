import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "data", "alienvoices.db")
MODEL_PATH = os.path.join(BASE_DIR, "models", "classifier.keras")
DATA_RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = False

SECRET_KEY = "change-me-in-production"

SAMPLE_RATE = 22050
N_MFCC = 40
MAX_PAD_LEN = 174

NUM_CLASSES = 5  # количество видов инопланетян
EPOCHS = 50
BATCH_SIZE = 32
