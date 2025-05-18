from flask import Blueprint, request, jsonify
from psycopg2.extras import RealDictCursor
from models.db import get_connection
from flasgger import swag_from
from flask_jwt_extended import jwt_required, get_jwt_identity

barang_bp = Blueprint('barang', __name__)

@barang_bp.route("/api/barang", methods=["GET"])
@jwt_required()
@swag_from('docs/item/list_barang.yml')
def list_barang():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM barang")
            result = cur.fetchall()
            return jsonify(result)

@barang_bp.route("/api/barang", methods=["POST"])
@jwt_required()
@swag_from('docs/item/tambah_barang.yml')
def tambah_barang():
    data = request.json
    current_user_id = get_jwt_identity()  # Mendapatkan user ID dari token
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO barang (user_id, nama, deskripsi, harga_awal, status)
                VALUES (%s, %s, %s, %s, 'dibuka') RETURNING id
            """, (current_user_id, data["nama"], data["deskripsi"], data["harga_awal"]))
            conn.commit()
            return jsonify({"message": "Barang ditambahkan"}), 201

@barang_bp.route("/api/barang/<int:id>", methods=["PUT"])
@jwt_required()
@swag_from('docs/item/update_barang.yml')
def update_barang(id):
    data = request.json
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE barang SET nama=%s, deskripsi=%s, harga_awal=%s WHERE id=%s
            """, (data["nama"], data["deskripsi"], data["harga_awal"], id))
            conn.commit()
            return jsonify({"message": "Barang diperbarui"})

@barang_bp.route("/api/barang/<int:id>", methods=["DELETE"])
@jwt_required()
@swag_from('docs/item/hapus_barang_per_id.yml')
def delete_barang(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM barang WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"message": "Barang dihapus"})

@barang_bp.route("/api/barang/<int:id>/tutup", methods=["POST"])
@jwt_required()
@swag_from('docs/item/tutup_lelang.yml')
def tutup_lelang(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE barang SET status='ditutup' WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"message": "Lelang ditutup"})

@barang_bp.route("/api/barang/<int:id>/penawaran_tertinggi", methods=["GET"])
@jwt_required()
@swag_from('docs/item/penawaran_tertinggi.yml')
def penawaran_tertinggi(id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM penawaran
                WHERE barang_id = %s
                ORDER BY jumlah DESC
                LIMIT 1
            """, (id,))
            row = cur.fetchone()
            if row:
                return jsonify(row)
            else:
                return jsonify({"message": "Belum ada penawaran"})
