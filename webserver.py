from flask import Flask, render_template, request, redirect, url_for, flash
from db_server import create_session
# from database_setup import Restaurant, MenuItem
from database_setup import Base, Restaurant, MenuItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.pool import StaticPool

# session = create_session()
engine = create_engine('sqlite:///restaurantmenu.db',
                       connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        newItem = MenuItem(name=name, restaurant_id=restaurant_id,
                           price=price, description=description)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('create_menu_item.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    newItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        newItem.name = name
        newItem.description = description
        newItem.price = price

        session.add(newItem)
        session.commit()
        flash("Menu Item Updated!")

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', item=newItem, restaurant_id=restaurant_id, menu_id=menu_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id)
    if request.method == 'POST':
        item.delete()
        flash("Menu Item Removed!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('delete.html', item=item, restaurant_id=restaurant_id, menu_id=menu_id)


@app.route('/')
@app.route('/restaurants/<int:param_restaurant_id>')
def restaurantMenu(param_restaurant_id=0):
    restaurant = None
    if param_restaurant_id is not 0:
        restaurant = session.query(Restaurant).filter_by(
            id=param_restaurant_id).one()
    else:
        restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


if __name__ == '__main__':
    app.secret_key = 'P@ssW0rd'
    app.debug = True
    app.run(host='localhost', port=5000)
