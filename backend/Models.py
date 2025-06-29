from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    favorites = db.relationship("FavoriteCity", back_populates="user", cascade="all, delete")

    def to_dict(self):
     return {
        "id": self.id,
        "username": self.username,
        "favorites": [f.to_dict() for f in self.favorites]
    }


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    favorites = db.relationship("FavoriteCity", back_populates="city", cascade="all, delete")

    def to_dict(self):
     return {
        "id": self.id,
        "name": self.name
    }

class FavoriteCity(db.Model):
    __tablename__ = 'favorite_cities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))

    user = db.relationship("User", back_populates="favorites")
    city = db.relationship("City", back_populates="favorites")

    def to_dict(self):
     return {
        "id": self.id,
        "city": self.city.to_dict(),
        "user_id": self.user_id
    }