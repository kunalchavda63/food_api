from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User
from config import Config
from route_enum import Routes
from constants import Methods
from admin_routes import admin_bp

# Admin credentials (hardcoded for this demo)
ADMIN_EMAIL = "shlokyadav0803@gmail.com"
ADMIN_PASSWORD = "12345"   # will be hashed automatically

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

# Auto-create admin account if not exist
with app.app_context():
    existing = User.query.filter_by(email=ADMIN_EMAIL).first()
    if not existing:
        hashed = bcrypt.generate_password_hash(ADMIN_PASSWORD).decode("utf-8")
        admin_user = User(name="shlok", email=ADMIN_EMAIL, password=hashed, role="admin")
        db.session.add(admin_user)
        db.session.commit()
        print(f"[setup] Created admin: {ADMIN_EMAIL}")

app.register_blueprint(admin_bp, url_prefix="/admin")


@app.route(Routes.Root, methods=[Methods.GET])
def hello():
    return jsonify({"message": "Hello, Flask is working!"}), 200


@app.route(Routes.SIGNUP, methods=[Methods.POST])
def signup():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Prevent anyone from signing up as the admin email
    if email.lower() == ADMIN_EMAIL.lower():
        return jsonify({"error": "Cannot signup using admin email"}), 403

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    # assign role: if password is "shlok" then admin else user
    role = "admin" if password == "shlok" else "user"

    new_user = User(name=name, email=email, password=hashed_pw, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": new_user.id, "role": new_user.role}), 201


@app.route(Routes.LOGIN, methods=[Methods.POST])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Missing Email Or Password"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login Successful", "user_id": user.id, "role": user.role, "name": user.name}), 200
    else:
        return jsonify({"error": "Invalid Password"}), 401


@app.route(Routes.USERS, methods=[Methods.POST])
def all_users_public():
    # public listing (non-admin) - returns paginated users
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)

    users = [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in pagination.items]
    return jsonify({"users": users, "total": pagination.total, "page": pagination.page, "pages": pagination.pages}), 200


@app.route(Routes.DELETE_USER, methods=[Methods.DELETE])
def delete_user_public():
    data = request.get_json(silent=True) or {}
    user_id = data.get("id")
    if not user_id:
        return jsonify({"error": "User Id is required"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User with ID {user_id} deleted Successfully"}), 200


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
