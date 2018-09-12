from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza palazio")
cheesepizza = MenuItem(name = "Chesse Pizza", description ="made with natural ingredient", course = "Entree", price = "8.99", restaurant = myFirstRestaurant)
session.add(myFirstRestaurant)
session.add(cheesepizza)

session.commit()

print(session.query(Restaurant).all())