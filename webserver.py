from flask import Flask, render_template
from db_server import create_session
from database_setup import Restaurant, MenuItem

session = create_session()
app = Flask(__name__)


@app.route('/restaurants/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

@app.route('/')
@app.route('/restaurants/<int:param_restaurant_id>')
def restaurants(param_restaurant_id = 0):
    restaurant = None 
    if param_restaurant_id is not 0:
        restaurant = session.query(Restaurant).filter_by(id=param_restaurant_id).one()
    else:
        restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
