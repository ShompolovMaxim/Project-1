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
    return render_template('catalog.html')

@app.route('/product1/')
def product1():
    return render_template('product.html')

if __name__ == '__main__':
    app.run(debug=True)
