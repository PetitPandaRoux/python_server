from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
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

if __name__ == '__main__':
    app.debug = True
app.run(host='0.0.0.0', port=5000)

