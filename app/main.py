from flask import *
from app.app import app, db
from app.ORM import Feedback, Customers, Goods, Orders, Shopping_cart
from datetime import datetime

def buy(good_id):
    login = session.get('login')
    if login:
        good = list(filter(lambda x: x.id==good_id,Goods.query.all()))[0]
        if good.quantity > 0:
            cust = list(filter(lambda x: x.login==login,Customers.query.all()))[0]
            cart_item=list(filter(lambda x: x.good.id==good_id and x.customer.login==login, Shopping_cart.query.all()))
            if cart_item==[]:
                db.session.add(Shopping_cart(quantity = 1, good = good, customer=cust))
            else:
                cart_item[0].quantity += 1
            good.quantity -= 1
            db.session.commit()
        else:
            flash('Нет на складе', 'warning')
    else:
        flash('Авторизуйтесь, чтобы совершать покупки.','warning')
        return 'redirect_to_sign_in'


@app.route('/')
def main():
    login = session.get('login')
    customer = None
    if login:
        customer=Customers.query.filter_by(login=login).one()
    return render_template('Main.html', customer=customer)

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        login = request.form.get('login')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        if name and surname and login and password:
            try:
                customer = Customers(name=name,surname=surname,login=login, registration_date = datetime.now(), phone_number = phone_number, email = email, total_orders = 0)
                customer.hash_password(password)
                db.session.add(customer)
                db.session.commit()
                session['login'] = login
                return redirect(url_for('main'), code=302)
            except:
                flash('This login is already used', 'warning')
        else:
            flash('Необходимо заполнить все поля, помеченные *', 'warning')
    return render_template('registration.html')

@app.route('/sign_in/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        try:
            if Customers.query.filter_by(login=login).one().validate(password):
                session['login'] = login
                flash(f'Добро пожаловать, {login}', 'success')
                return redirect(url_for('main'), code=301)
            else:
                flash('Wrong login or password', 'warning')
        except:
            flash('Wrong login or password', 'danger')
    return render_template('sign_in.html')

@app.route('/sign_out/')
def logout():
    if session.get('login'):
        session.pop('login')
    return redirect('/', code=302)

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    customer=Customers.query.filter_by(login=login).one()

    if not login:
        return redirect(url_for('main'), code=302)

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        login = request.form.get('login')
        new_password = request.form.get('new_password')
        if name and surname and login:
            try:
                customer.name = request.form.get('name')
                customer.surname = request.form.get('surname')
                customer.login = request.form.get('login')
                if request.form.get('phone_number'):
                    customer.phone_number = request.form.get('phone_number')
                else:
                    customer.phone_number = None
                if request.form.get('email'):
                    customer.email = request.form.get('email')
                else:
                    customer.email = None
                if new_password:
                    customer.hash_password(new_password)
                db.session.commit()
                session['login'] = login
            except:
                flash('This login is already used', 'warning')
        else:
            flash('Необходимо заполнить все поля, помеченные *', 'warning')
    
    return render_template('profile.html',customer=customer)

@app.route('/about_us/', methods=['GET', 'POST'])
def about_us():
    login = session.get('login')
    if request.method == 'POST':
        name = request.form.get('name')
        review = request.form.get('review')
        if name!='' and review!='':
            db.session.add(Feedback(name=name,review=review))
            db.session.commit()
    return render_template('About_us.html',feedback=Feedback.query.all(),login=login)

@app.route('/catalog/', methods=['GET', 'POST'])
def catalog():
    min_price=int(request.args.get('min_price',0))
    max_price=int(request.args.get('max_price',10**9))

    if request.method == 'POST':
        if 'buy' in request.form:
            action = request.form['buy']
            good_id = int(action)
            if buy(good_id):
                return redirect(url_for('sign_in'), code=302)
        elif 'sort' in request.form:
            try:
                min_price = int(request.form.get('min_price', 0))
            except:
                flash('Некорректные данные','warning')
            try:
                max_price = int(request.form.get('max_price', 10**9))
            except:
                flash('Некорректные данные','warning')

    min_price = max(0,min_price)
    max_price= min(max_price,max([i.price.price for i in Goods.query.all()]))

    login = session.get('login')
    goods=[]
    quantity = dict()
    for i in Goods.query.all():
        if min_price<=i.price.price<=max_price:
            goods.append(i)
            cart = list(filter(lambda x: x.customer.login == login and x.good.id == i.id, Shopping_cart.query.all()))
            if not cart == []:
                quantity[i.id] = cart[0].quantity

    return render_template('catalog.html',goods=goods, quantity = quantity, min_price = min_price, max_price = max_price)

@app.route('/product/', methods=['GET', 'POST'])
def product():
    login = session.get('login')
    if request.method == 'POST':
        good_id = int(request.args.get('good_id', 0))
        if buy(good_id):
            return redirect(url_for('sign_in'), code=301)

    good_id=int(request.args.get('good_id',-1))

    cart = list(filter(lambda x: x.customer.login == login and x.good.id == good_id, Shopping_cart.query.all()))
    if cart == []:
        quantity = 0
    else:
        quantity = cart[0].quantity

    return render_template('Product.html', good=list(filter(lambda x: x.id == good_id, Goods.query.all()))[0], quantity = quantity)

@app.route('/shopping_cart/', methods=['GET', 'POST'])
def shopping_cart():
    login = session.get('login')

    if not login:
        return redirect(url_for('main'), code=302)

    if request.method == 'POST':
        action = request.form['action']
        if action == 'make':
            cust = list(filter(lambda x: x.login==login,Customers.query.all()))[0]
            cust.total_orders += 1
            number = cust.id*10**8+cust.total_orders
            for i in list(filter(lambda x: x.customer.login==login,Shopping_cart.query.all())):
                db.session.add(Orders(number_of_order=number, quantity=i.quantity, good=i.good, customer=i.customer, date=datetime.now(), status='collecting', price=i.good.price))
                db.session.delete(i)
                i.good.quantity -= i.quantity
        elif action == 'clear':
            for i in list(filter(lambda x: x.customer.login==login,Shopping_cart.query.all())):
                db.session.delete(i)
        db.session.commit()

    cart=list(filter(lambda x: x.customer.login==login,Shopping_cart.query.all()))
    cart.sort(key = lambda x: x.good.id)
    total = 0
    for i in cart:
        total += i.quantity * i.good.price.price
    return render_template('shopping_cart.html',cart = cart, total = total)

@app.route('/orders/')
def orders():
    login = session.get('login')

    if not login:
        return redirect(url_for('main'), code=302)

    orders_dict = dict()
    total = dict()

    for i in sorted(list(filter(lambda x: x.customer.login==login,Orders.query.all())),key=lambda x:-x.number_of_order):
        if i.number_of_order not in orders_dict:
            orders_dict[i.number_of_order]=[i]
            total[i.number_of_order]=i.price.price*i.quantity
        else:
            orders_dict[i.number_of_order].append(i)
            total[i.number_of_order]+=i.price.price*i.quantity
    for i in orders_dict:
        orders_dict[i].sort(key=lambda x:x.good.id)
    return render_template('orders.html',orders=orders_dict, total=total)

@app.route('/customers_list/')
def customers_list():
    login = session.get('login')
    customer=Customers.query.filter_by(login=login).one()

    if not login or customer.admin == 0:
        return redirect(url_for('main'), code=302)

    customers = Customers.query.all()
    return render_template('customers_list.html',customers=customers)

if __name__ == '__main__':
    app.run(debug=True)
