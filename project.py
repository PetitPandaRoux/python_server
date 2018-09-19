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
@app.route('/restaurants/')
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
# l'argument est passee par get
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'], course = request.form['course'], description = request.form['description'], price = request.form['price'],restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id)) 
# l'argument passee par get est ensuite passee au template
    else :
        return render_template('new-menu-item.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/editMenu/<int:menu_id>/',methods = ['GET','POST'])
def edit_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
         item.name = request.form['name']
         item.price = request.form['price']
         item.description = request.form['description']
         item.course = request.form['course']
         session.add(item)
         session.commit()
         return redirect ((url_for('restaurant_menu', restaurant_id = restaurant_id)))
    else :
        return render_template('edit-menu-item.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item)

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/',methods = ['GET','POST'])
def delete_menu_item(restaurant_id, menu_id): 
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        return redirect ((url_for('restaurant_menu', restaurant_id = restaurant_id)))
    else:
        return render_template('delete-menu-item.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item_to_delete)

if __name__ == '__main__':
    app.debug = True
app.run(host='0.0.0.0', port=5000)

