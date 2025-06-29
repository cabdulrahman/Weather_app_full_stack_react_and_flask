from app import app
from Models import db, User, City, FavoriteCity


with app.app_context():
    print(" Seeding database...")

   
    FavoriteCity.query.delete()
    City.query.delete()
    User.query.delete()

    
    user1 = User(username="hibby")
    user2 = User(username="abdi")

    db.session.add_all([user1, user2])
    db.session.commit()

   
    nairobi = City(name="Nairobi")
    mombasa = City(name="Mombasa")
    new_york = City(name="New York")
    london = City(name="London")

    db.session.add_all([nairobi, mombasa, new_york, london])
    db.session.commit()

   
    fav1 = FavoriteCity(user_id=user1.id, city_id=nairobi.id)
    fav2 = FavoriteCity(user_id=user1.id, city_id=london.id)
    fav3 = FavoriteCity(user_id=user2.id, city_id=new_york.id)

    db.session.add_all([fav1, fav2, fav3])
    db.session.commit()

    print("Done seeding!")