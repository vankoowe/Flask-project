from flask import Flask, render_template, url_for, request
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

@app.route('/')
def register():
    return render_template('register.html')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('register'))

    return render_template('login.html')
#disable cache si cykni predi da polzwash
if __name__ == "__main__":
    app.run(debug=True)