from flask import Blueprint, request, jsonify
from psycopg2.extras import RealDictCursor
from models.db import get_connection
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

penawaran_bp = Blueprint('penawaran', __name__)

@penawaran_bp.route("/api/penawaran", methods=["GET"])
@jwt_required()
@swag_from('docs/penawaran/list_penawaran.yml')
def list_penawaran():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
            SELECT penawaran.id, barang.nama AS nama_barang, penawaran.jumlah, penawaran.waktu, users.username AS nama_user
            FROM penawaran
            JOIN barang ON barang.id = penawaran.barang_id
            JOIN users ON users.id = penawaran.user_id;
            """)
            return jsonify(cur.fetchall())

@penawaran_bp.route("/api/penawaran", methods=["POST"])
@jwt_required()
@swag_from('docs/penawaran/tambah_penawaran.yml')
def tambah_penawaran():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if not data or "barang_id" not in data or "jumlah" not in data:
        return jsonify({"error": "barang_id dan jumlah harus disediakan"}), 400

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT status FROM barang WHERE id=%s", (data["barang_id"],))
            barang = cur.fetchone()

            if not barang:
                return jsonify({"error": "Barang tidak ditemukan"}), 404
            if barang["status"] == "ditutup":
                return jsonify({"error": "Pelelangan sudah ditutup"}), 400

            cur.execute("""
                INSERT INTO penawaran (barang_id, user_id, jumlah)
                VALUES (%s, %s, %s)
            """, (data["barang_id"], current_user_id, data["jumlah"]))
            conn.commit()
            return jsonify({"message": "Penawaran ditambahkan"}), 201

@penawaran_bp.route("/api/penawaran/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from('docs/penawaran/update_penawaran.yml')
def update_penawaran(id):
    data = request.get_json()

    if not data or "jumlah" not in data:
        return jsonify({"error": "jumlah harus disediakan"}), 400

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE penawaran SET jumlah=%s WHERE id=%s", (data["jumlah"], id))
            conn.commit()
            return jsonify({"message": "Penawaran diperbarui"})

@penawaran_bp.route("/api/penawaran/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from('docs/penawaran/hapus_penawaran_per_id.yml')
def delete_penawaran(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM penawaran WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"message": "Penawaran dihapus"})
