from flask import Flask, render_template, request, redirect, url_for
from db_server import create_session
from database_setup import Restaurant, MenuItem

session = create_session()
app = Flask(__name__)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        newItem = MenuItem(name=name, restaurant_id=restaurant_id, price=price, description=description)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('create_menu_item.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

@app.route('/')
@app.route('/restaurants/<int:param_restaurant_id>')
def restaurantMenu(param_restaurant_id = 0):
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
