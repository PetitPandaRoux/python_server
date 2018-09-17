from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import cgi

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Create Session and connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler (BaseHTTPRequestHandler) :

    def do_GET(self):
        try:
     
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

        
                restaurant_list = session.query(Restaurant).all()
                message = ""
                message += "<html><body>"
                message += "<h2><a href = '/restaurants/new'/'>Make a new restaurant</a></h2>"
                for restaurant in restaurant_list:
                    message += restaurant.name
                    message += "</br>"
                    message += "<a href='/restaurants/%s/edit'>Edit </a>" %restaurant.id
                    message += "</br>"
                    message += " " + "<a href='/restaurants/%s/delete'> Delete</a><br><br>" %restaurant.id
                message += "</body></html>"
                self.wfile.write(message)
            
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                message = ""
                message += "<html><body>"
                message += "<h1>Delete " + myRestaurantQuery.name + " name</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'" %myRestaurantQuery.id
                message += '''name="delete-restaurant" placeholder="choose a new name" type="text" ><input type="submit" value="Confirm"> </form>'''
                self.wfile.write(message)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
      
                message = ""
                message += "<html><body>"
                message += "<h1>Edit " + myRestaurantQuery.name + " name</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>"%myRestaurantQuery.id
                message += '''Change restaurant name <input name="edit-restaurant" placeholder="choose a new name" type="text" ><input type="submit" value="Edit"> </form>'''
                self.wfile.write(message)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                message = "<html><body>"
                message += "<h1>Make a new restaurant</h1>"
                message += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>Create new restaurant <input name="add-restaurant" placeholder="choose a name" type="text" ><input type="submit" value="Create"> </form>'''
                message +="</body></html>"
                self.wfile.write(message)
                print (message)
                return

        except IOError:
            self.send_error(404, "File pas trouve %s" %self.path)

    def do_POST(self):
        try :
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                my_restaurant_query = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                session.delete(my_restaurant_query)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', 'http://localhost:8080/restaurants')
                self.end_headers()


            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    edit_restaurant_name = fields.get('edit-restaurant')
                    restaurantIDPath = self.path.split("/")[2]

                    my_restaurant_query = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    my_restaurant_query.name = edit_restaurant_name[0]
                    session.add(my_restaurant_query)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', 'http://localhost:8080/restaurants')
                    self.end_headers()

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    add_restaurant_name = fields.get('add-restaurant')
            
                    new_Restaurant_Name = Restaurant(name = add_restaurant_name[0])
                    session.add(new_Restaurant_Name)
                    session.commit()

                    output = ""
                    output += "<html><body>"
                    output += "<h2> Welcome to the new restaurant: </h2>"
                    output += "<h1> %s </h1>" %add_restaurant_name[0]
                    output += "<h2><a href='/restaurants'>Go back to restaurant list</a></h2>"
                    output += "</html></body>"
                    self.wfile.write(output)
                    print (output)

        except :
            pass



def main() :
    try :
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print ("web server running on port %s" %port)
        server.serve_forever()

    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()