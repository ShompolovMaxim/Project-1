from flask import *
from init import app
from ORM import Feedback, Customers, Goods, db



@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
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

@app.route('/about_us/', methods=['GET', 'POST'])
def about_us():
    if request.method == 'POST':
        name = request.form.get('name')
        review = request.form.get('review')
        if name!='' and review!='':
            db.session.add(Feedback(name=name,review=review))
            db.session.commit()
    return render_template('About_us.html',feedback=Feedback.query.all())

@app.route('/catalog/', methods=['GET', 'POST'])
def catalog():
    min_price=int(request.args.get('min_price',0))
    max_price=int(request.args.get('max_price',10**9))
    goods=[]
    for i in Goods.query.all():
        if min_price<=i.price.price<=max_price:
            goods.append(i)
    return render_template('catalog.html',goods=goods)

@app.route('/product/', methods=['GET', 'POST'])
def product():
    good_id=int(request.args.get('good_id',-1))
    goods=Goods.query.all()
    for i in goods:
        if i.id==good_id:
            break
    return render_template('Product.html',good=i)

if __name__ == '__main__':
    app.run(debug=True)
