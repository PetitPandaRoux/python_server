from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/JSON')
def restaurant_JSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurant_menu_JSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menu_item_JSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItems=[item.serialize])

@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods = ['GET','POST'])
def new_restaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(name = request.form['name'])
        session.add(new_restaurant)
        session.commit()
        flash( new_restaurant.name + " has been created!")
        return redirect(url_for('show_restaurants')) 
# l'argument passee par get est ensuite passee au template
    else :
        return render_template('new-restaurant.html')
 

@app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET','POST'])
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash(restaurant.name + " has been updated!")
        return redirect (url_for('show_restaurants'))
    else :
        return render_template('edit-restaurant.html', restaurant = restaurant, restaurant_id = restaurant.id)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
def delete_restaurant(restaurant_id):
    restaurant_to_delete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant_to_delete)
        session.commit()
        flash(restaurant_to_delete.name + " has been deleted!")
        return redirect (url_for('show_restaurants'))
    else:
        return render_template('delete-restaurant.html', restaurant = restaurant_to_delete, restaurant_id = restaurant_to_delete.id)

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


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods = ['GET','POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'], course = request.form['course'], description = request.form['description'], price = request.form['price'],restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        flash(new_item.name + " has been created!")
        return redirect(url_for('show_menu', restaurant_id = restaurant_id)) 

    else :
        return render_template('new-menu-item.html', restaurant_id = restaurant_id, restaurant = restaurant)
 

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET','POST'])
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.description = request.form['description']
        item.course = request.form['course']
        session.add(item)
        session.commit()
        flash(item.name + "has been updated!")
        return redirect (url_for('show_menu', restaurant_id = restaurant_id))

    else :
        return render_template('edit-menu-item.html', restaurant = restaurant,restaurant_id = restaurant_id, item = item, menu_id = item.id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET','POST'])
def delete_menu_item(restaurant_id, menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash(item_to_delete.name + " has been deleted!")
        return redirect (url_for('show_menu', restaurant_id = restaurant_id))
    else:
        return render_template('delete-menu-item.html', restaurant_id = restaurant_id, menu_id = item_to_delete.id, item = item_to_delete)


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded = False)