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
                message += "<p><a href = '/restaurants/new'/'>Make a new restaurant</a></p>"
                for restaurant in restaurant_list:
                    message += restaurant.name
                    message += "</br>"
                    message += "<a href='#'>Edit</a>"
                    message += "<a href='#'> Delete</a><br><br>" 
                message += "</body></html>"
                self.wfile.write(message)

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
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

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