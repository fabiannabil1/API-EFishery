from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from psycopg2.extras import RealDictCursor
from models.db import get_connection
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/api/login", methods=["POST"])
@swag_from('docs/auth/login.yml')
def login():
    data = request.json
    nomor_hp = data.get("nomor_hp")
    password = data.get("password")

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, password_hash FROM users WHERE nomor_hp=%s", (nomor_hp,))
            user = cur.fetchone()

    if not user:
        return jsonify({"error": "nomor_hp atau password salah"}), 401

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "nomor_hp atau password salah"}), 401

    # access_token = create_access_token(identity=user["id"])
    access_token = create_access_token(identity=str(user["id"]))
    return jsonify(access_token=access_token)

@auth_bp.route("/api/register", methods=["POST"])
@swag_from('docs/auth/register.yml')
def register():
    data = request.json
    print(data)
    nomor_hp = data.get("nomor_hp")
    password = data.get("password")
    address = data.get("address")
    name = data.get("name")
    role = data.get("role", "biasa")

    if not nomor_hp or not password:
        return jsonify({"error": "nomor_hp dan password harus diisi"}), 400

    hashed_password = generate_password_hash(password)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE nomor_hp=%s", (nomor_hp,))
            if cur.fetchone():
                return jsonify({"error": "Nomor HP telah terdaftar"}), 409

            cur.execute("INSERT INTO users (nomor_hp, password_hash,alamat,role,nama_lengkap) VALUES (%s, %s, %s, %s, %s)", (nomor_hp, hashed_password,address, role, name))
            conn.commit()

    return jsonify({"message": "Registrasi berhasil"}), 201
