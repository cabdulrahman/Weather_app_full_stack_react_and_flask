from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from datetime import timedelta
import requests

from Models import db, User, City, FavoriteCity


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "0f9ddede21bf4d8936af9ae65af3d978"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

API_KEY = "0f9ddede21bf4d8936af9ae65af3d978"




@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'City not found'}), 404

    data = response.json()
    return jsonify({
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description']
    })


@app.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user": user.to_dict()}), 201


@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    token = create_access_token(identity=user.id)
    return jsonify({"token": token, "user": user.to_dict()}), 200


@app.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@app.route('/favorites', methods=["GET"])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites = [f.to_dict() for f in user.favorites]
    return jsonify(favorites), 200


@app.route('/favorites', methods=["POST"])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()
    city_name = data.get("city")

    if not city_name:
        return jsonify({"error": "City name required"}), 400

    city = City.query.filter_by(name=city_name).first()
    if not city:
        city = City(name=city_name)
        db.session.add(city)
        db.session.commit()

    existing = FavoriteCity.query.filter_by(user_id=user_id, city_id=city.id).first()
    if existing:
        return jsonify({"error": "City already in favorites"}), 409

    favorite = FavoriteCity(user_id=user_id, city_id=city.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.to_dict()), 201

@app.route('/favorites/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_favorite(id):
    user_id = get_jwt_identity()
    favorite = FavoriteCity.query.get(id)

    if not favorite or favorite.user_id != user_id:
        return jsonify({"error": "Favorite not found or not yours"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed"}), 200


@app.route('/favorites/<int:id>', methods=["PATCH"])
@jwt_required()
def update_favorite(id):
    user_id = get_jwt_identity()
    favorite = FavoriteCity.query.get(id)

    if not favorite or favorite.user_id != user_id:
        return jsonify({"error": "Favorite not found"}), 404

   
    return jsonify(favorite.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)