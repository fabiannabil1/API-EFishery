from flask import Blueprint, jsonify

welcome_bp = Blueprint('welcome', __name__)

@welcome_bp.route("/", methods=["GET"])
def welcome():
    """
    Welcome endpoint
    ---
    responses:
      200:
        description: Selamat Datang di API Pelelangan Barang
    """
    return jsonify({"message": "Welcome to the Auth API!"})