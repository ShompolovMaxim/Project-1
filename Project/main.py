from flask import *

app = Flask(__name__)

feedback=[]

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/about_us/')
def about_us():
    if request.method == 'POST':
        review = request.form.get('review')
        feedback.appnend(review)
        print(feedback)
    return render_template('about_us.html')

@app.route('/catalog/')
def catalog():
    return render_template('catalog.html')

@app.route('/product1/')
def product1():
    return render_template('product.html')

if __name__ == '__main__':
    app.run(debug=True)
