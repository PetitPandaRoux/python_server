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

# NECESSARY SESSION
#engine = create_engine('sqlite:///restaurantmenu.db')
#Base.metadata.bind = engine
#DBSession = sessionmaker(bind = engine)
#session = DBSession()

# CREATE DOC
# newRestaurant = Restaurant(name = "Pizza palazio")
# session.add(newRestaurant)
# session.commit()
#
# UPDATE DOC
#
# cible = session.query(restaurant).filter_by(name='').one()
# cible.price = newPrice
# session.add(cible)
# session.commit()
