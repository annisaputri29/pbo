# flask imports
from flask import Flask, render_template, session, redirect, request, flash
from flaskext.mysql import MySQL
import secrets  

secret_key = secrets.token_hex(16)  # Generates a random 32-character hex string  

# models definitions
from models.user import User
from models.menu_item import MenuItem
from models.order import Order
from models.rating import Rating
from models.db import DB

# app bulding
app = Flask(__name__, template_folder='views')
app.secret_key = secret_key  # Replace with your generated secret key  
mysql = MySQL()
db = DB(mysql, app)

@app.route('/')  
def index():
    if 'login' not in session or not session['login']:  
        return redirect('/auth/login')

    menu_with_ratings = {}
    # current user
    current_user = User(
        session['full_name'], 
        session['email'], 
        session['username'], 
        session['password'], 
        session['role']
        )
    # fetch menu
    all_menu = db.fetch_all('menu_items')
    current_menu = [MenuItem(menu[0], menu[1], menu[2], menu[3], menu[4], menu[5]) for menu in all_menu]

    # fetch ratings for each menu
    for menu in current_menu:
        avg_rating = db.fetch_mean('ratings', 'rating', 'menu_id', menu.item_id)
        if avg_rating[0] is not None:
            menu_with_ratings[menu] = avg_rating[0]
        else:
            menu_with_ratings[menu] = 'No ratings yet'

    return render_template('index.html', current_user=current_user, menu_with_ratings=menu_with_ratings) 

@app.route('/auth/login', methods=['POST', 'GET'])  
def login():
    if request.method == 'GET':
        return render_template('login.html')  
    if request.method == 'POST':

        user = db.login(request.form['username'], request.form['password'], session)

        if user is not None:
            return redirect('/')  # Redirect to the index page 
        else:
            return redirect('/auth/login') 

@app.route('/auth/register', methods=['POST', 'GET'])  
def register():
    if request.method == 'GET':
        return render_template('register.html')  
    if request.method == 'POST':
        # instantiate new user
        new_user = User(
            request.form['full_name'],
            request.form['email'],
            request.form['username'],
            request.form['password'],
            request.form['role']
        )

        # hash password
        new_user.hash()

        # save to db
        new_user.save(db.db)

        return redirect('/auth/login')

@app.route('/auth/logout')  
def logout():
    # clear session
    session.clear()
    return redirect('/auth/login')  # Redirect to the index page 

@app.route('/order/menu/<item_id>', methods=['POST', 'GET'])  
def order(item_id):
    # fetch item
    fetch = db.fetch_one('menu_items', item_id)

    menu_item = MenuItem(
        fetch[0],
        fetch[1],
        fetch[2],
        fetch[3],
        fetch[4],
        fetch[5]
    )

    if request.method == 'GET':

        return render_template('order.html', menu_item=menu_item)
    
    if request.method == 'POST':
        qty = request.form.get('quantity', type=int)

        if menu_item.check_stock(qty):
            menu_item.update_stock(db.db, item_id, menu_item.stock - qty)

            # instantiate new order
            new_order = Order(
                None,
                session['user_id'],
                item_id,
                qty,
                float(request.form.get('totalPrice').replace('Rp', '').replace('.', '')),
                request.form.get('deliveryAddress'),
                None,
                None
            )

            # save order
            new_order.save(db.db)

            return redirect('/')
        else:
            flash('Insufficient stock. Please order a smaller quantity.', 'danger')  
            return redirect(f'/order/menu/{item_id}') 
    
@app.route('/orders', methods=['GET'])  
def get_orders():
    if request.method == 'GET':
        # current user
        current_user = User(
            session['full_name'], 
            session['email'], 
            session['username'], 
            session['password'], 
            session['role']
            )

        if session['role'] == 'user':
            order_menu_items = {}

            # fetch item
            fetch = db.fetch_all_filtered('orders', 'customer_id', session['user_id'])

            all_orders = [Order(order[0], order[1], order[2], order[3], order[4], order[5], order[6], order[7]) for order in fetch]
            
            for order in all_orders:
                order_menu_items[order] = db.fetch_one('menu_items', order.menu_id)

            return render_template('get_orders.html', order_menu_items=order_menu_items, current_user=current_user)
        
        # admin
        if session['role'] == 'admin':
            # fetch item
            fetch = db.fetch_all('orders')

            all_orders = [Order(order[0], order[1], order[2], order[3], order[4], order[5], order[6], order[7]) for order in fetch]

            return render_template('get_orders.html', all_orders=all_orders, current_user=current_user)

@app.route('/order/<order_id>/update', methods=['POST'])  
def update_order(order_id):
    if request.method == 'POST':
        # get order
        fetch = db.fetch_one('orders', order_id)
        order = Order(
            fetch[0],
            fetch[1],
            fetch[2],
            fetch[3],
            fetch[4],
            fetch[5],
            fetch[6],
            fetch[7]
        )

        # update status
        order.update_status(db.db)

        return redirect('/orders')

@app.route('/menu/add', methods=['POST', 'GET'])  
def add_menu():
    if request.method == 'GET':
        return render_template('add_menu.html')  
    if request.method == 'POST':
        # instantiate new menu item
        new_item = MenuItem(
            None,
            request.form['foodName'],
            request.form['price'],
            request.form['description'],
            request.form['imageLink'],
            request.form['stock']
        )

        # save to db
        new_item.save(db.db)

        return redirect('/')

@app.route('/menu/delete/<menu_id>', methods=['GET'])  
def delete_menu(menu_id):
    
    try:
        db.delete_one('menu_items', menu_id)
    except Exception as e:
        print(e)
    return redirect('/')

@app.route('/menu/update/<menu_id>', methods=['GET', 'POST'])  
def update_menu(menu_id):
    

    if request.method == 'GET':
        # fetch item
        fetch = db.fetch_one('menu_items', menu_id)

        menu_item = MenuItem(
            fetch[0],
            fetch[1],
            fetch[2],
            fetch[3],
            fetch[4],
            fetch[5]
        )

        return render_template('update_menu.html', menu=menu_item)
    if request.method == 'POST':
        # instantiate updated menu item
        updated_item = MenuItem(
            menu_id,
            request.form['foodName'],
            request.form['price'],
            request.form['description'],
            request.form['imageLink'],
            request.form['stock']
        )

        # save to db
        updated_item.update(db.db, updated_item.item_id)

        return redirect('/')
    
@app.route('/menu/<menu_id>/rating', methods=['GET', 'POST'])  
def give_rating(menu_id):
    # fetch from db
    fetch = db.fetch_one('menu_items', menu_id)

    # instantiate new MenuItem object
    menu = MenuItem(
        fetch[0],
        fetch[1],
        fetch[2],
        fetch[3],
        fetch[4],
        fetch[5]
    )
    if request.method == 'GET':
        return render_template('ratings.html', menu=menu)
    
    if request.method == 'POST':
        rating = request.form.get('rating')  # This retrieves the selected rating value  
        comment = request.form.get('comment')  # This retrieves the comment text  

        rating = Rating(
            session['user_id'],
            menu_id,
            rating, 
            comment
        )

        # save to db
        rating.save(db.db)

        return redirect('/orders')

# run flask
if __name__=='__main__': 
   app.run(debug=True) 