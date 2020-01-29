from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template('register.html')
    
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('register'))

    return render_template('login.html')
#disable cache si cykni predi da polzwash
if __name__ == "__main__":
    app.run(debug=True)