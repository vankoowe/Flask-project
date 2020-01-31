from flask import Flask, render_template, url_for, request, redirect
from user import User
from offer import Offer
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        email = request.form['email']
        values = (
            None,
            email,
            User.hash_password(request.form['password']),
            request.form['name'],
            request.form['address'],
            request.form['phone_number']
        )
        User(*values).create()

        return redirect("offers/{}/".format(User.get_user_by_email(email)))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['email'],
            User.hash_password(request.form['password'])
        )

        return redirect("offers/{}/".format(User.get_user_by_email(request.form['email'])))

@app.route('/offers/new_offer/<int:id>/', methods=['GET', 'POST'])
def new_offer(id):
    if request.method == 'GET':
        return render_template('new_offer.html', User = User.get_user(id))
    elif request.method == "POST":
        values = (
            None,
            request.form['title'],
            request.form['description'],
            request.form['price'],
            id
        )
        Offer(*values).create()

        return redirect('/offers/{}/'.format(id))

@app.route('/<int:id>/delete/', methods=['POST'])
def delete(id):
    offer = Offer.find(id)
    name = User.get_user(offer.seller_id)
    offer.delete()
    return render_template('offers.html', User = name, offers = Offer.all())

@app.route('/offers/<int:id>/', methods=['GET', 'POST'])
def offers1(id):
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('offers.html', User = User.get_user(id), offers = Offer.all())

@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('offers.html', User = None, offers = Offer.all())

#disable cache si cykni predi da polzwash
if __name__ == "__main__":
    app.run(debug=True)