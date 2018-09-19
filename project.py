from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def all_restaurants():
    restaurants = session.query(Restaurant).all()
    output = ''
    for restaurant in restaurants :
        output += ''
        output += "<h2>" + restaurant.name + "</h2>"
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        for i in items:
            output += i.name
            output += '<br>'
            output += i.price
            output += '<br>'
            output += i.description
            output += '<br><br>'
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items= items)

@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET','POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'], course = request.form['course'], description = request.form['description'], price = request.form['price'],restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
    else :
        return render_template('new-menu-item.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/editMenu/<int:menu_id>/')
def edit_menu_item(restaurant_id, menu_id):
    return "edit Menu"

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/')
def deleteMenuItem(restaurant_id, menu_id):
    return "delete a menu item"

if __name__ == '__main__':
    app.debug = True
app.run(host='0.0.0.0', port=5000)

