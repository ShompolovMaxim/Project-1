from flask import *
from ORM import *

'''class Feedback():

    def __init__(self,name,review):
        self.name=name
        self.review=review'''

#app = Flask(__name__)

feedback=[]

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/about_us/', methods=['GET', 'POST'])
def about_us():
    if request.method == 'POST':
        name = request.form.get('name')
        review = request.form.get('review')
        db.session.add(Feedback(name=name,review=review))
    return render_template('about_us.html',feedback=Feedback.query.all())

@app.route('/catalog/')
def catalog():
    return render_template('catalog.html',goods=Goods.query.all())

@app.route('/product1/', methods=['GET', 'POST'])
def product1():
    good_id=int(request.args.get('good_id',-1))
    goods=Goods.query.all()
    for i in goods:
        if i.id==good_id:
            break
    return render_template('product.html',good=i)

if __name__ == '__main__':
    app.run(debug=True)
