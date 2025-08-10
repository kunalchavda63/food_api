from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User
from config import Config
from route_enum import Routes
from constants import Methods

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()


@app.route(Routes.Root, methods=[Methods.GET])
def hello():
    return jsonify({"message": "Hello, Flask is working!"}), 200


@app.route(Routes.SIGNUP, methods=[Methods.POST])
def signup():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(name=name, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201


@app.route(Routes.LOGIN, methods=[Methods.POST])
def login():
    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Missing Email Or Password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login Successful", "user_id": user.id}), 200
    else:
        return jsonify({"error": "invalid Password"}), 401


@app.route(Routes.USERS, methods=[Methods.POST])
def all_users():
    data = request.get_json(silent=True) or {}
    page = data.get("page", 1)
    per_page = data.get("per_page", 10)
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)

    users_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in pagination.items

    ]

    return jsonify({
        "users": users_list,
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages

    }), 200


if __name__ == "__main__":
    app.run(debug=True)
