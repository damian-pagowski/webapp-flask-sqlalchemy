from flask import Flask
from db_server import create_session
from database_setup import Restaurant, MenuItem

session = create_session()
app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = '<h1>%s</h1><h5>Menu:</h5><ul>' % restaurant.name
    for i in items:
        row = '<li>%s</li>' % i.name
        output += row
    output += "</ul>"
    return output 


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
