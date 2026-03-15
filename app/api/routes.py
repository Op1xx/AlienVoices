import os
from flask import Blueprint, request, jsonify
from app.auth.auth import authenticate_user, register_user
from app.database.models import get_connection
from app.ml.preprocessor import extract_features
from app.ml.model import load_model, predict
from config import DATA_RAW_PATH

bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if register_user(data["username"], data["password"]):
        return jsonify({"message": "Пользователь зарегистрирован"}), 201
    return jsonify({"error": "Пользователь уже существует"}), 409


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if authenticate_user(data["username"], data["password"]):
        return jsonify({"message": "Успешный вход"})
    return jsonify({"error": "Неверные учётные данные"}), 401


@bp.route("/classify", methods=["POST"])
def classify():
    if "file" not in request.files:
        return jsonify({"error": "Файл не передан"}), 400

    file = request.files["file"]
    save_path = os.path.join(DATA_RAW_PATH, file.filename)
    file.save(save_path)

    model = load_model()
    features = extract_features(save_path)
    class_id, confidence = predict(model, features)

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO voice_samples (filename, alien_class, confidence) VALUES (?, ?, ?)",
            (file.filename, str(class_id), confidence),
        )

    return jsonify({"class_id": class_id, "confidence": confidence})


@bp.route("/samples", methods=["GET"])
def get_samples():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM voice_samples ORDER BY created_at DESC").fetchall()
    return jsonify([dict(r) for r in rows])
