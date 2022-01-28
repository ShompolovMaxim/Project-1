from flask import *

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/about_us/')
def about_us():
    return render_template('About_us.html')

@app.route('/catalog/')
def catalog():
    return render_template('Catalog.html')

@app.route('/product1/')
def product1():
    return render_template('Product.html')

if __name__ == '__main__':
    app.run(debug=True)
