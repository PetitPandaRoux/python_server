from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/')
def new_restaurant():
    return render_template('new-restaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/')
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('edit-restaurant.html', restaurant = restaurant, restaurant_id = restaurant.id)

@app.route('/restaurant/<int:restaurant_id>/delete/')
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('delete-restaurant.html', restaurant = restaurant, restaurant_id = restaurant.id)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    def select_course_type(menus, course_type):
        new_list = []
        for item in menus :
            if item.course == course_type:
                new_list.append(item)
        return new_list
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    appetizers = select_course_type(items,'Appetizer')
    beverages = select_course_type(items,'Beverage')
    entrees = select_course_type(items, 'Entree')
    desserts = select_course_type(items, 'Dessert')

    return render_template('menu.html', restaurant = restaurant, restaurant_id = restaurant_id, appetizers= appetizers, beverages = beverages, entrees = entrees, desserts = desserts)


@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('new-menu-item.html', restaurant_id = restaurant_id, restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    return render_template('edit-menu-item.html', restaurant = restaurant,restaurant_id = restaurant_id, item = item, menu_id = item.id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    return render_template('delete-menu-item.html', restaurant_id = restaurant_id, menu_id = item.id, item = item)


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded = False)