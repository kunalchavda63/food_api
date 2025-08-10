from flask import Blueprint, request, jsonify
from models import db, User

admin_bp = Blueprint("admin", __name__)

def _is_request_admin():
    # Simple check: admin identity via header (for demo). In real apps use JWT.
    admin_email = request.headers.get("X-Admin-Email")
    if not admin_email:
        return False
    user = User.query.filter_by(email=admin_email).first()
    return user is not None and user.role == "admin"

@admin_bp.before_request
def guard():
    if not _is_request_admin():
        return jsonify({"error": "Unauthorized"}), 403

@admin_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]), 200

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json() or {}
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.role = data.get("role", user.role)
    db.session.commit()
    return jsonify({"message": "Updated"}), 200
