from Flask import flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return render_template("logout.html")

@app.route('/new')
def new():
    return render_template("new.html")

@app.route('/story/<id>')
def story():
    return render_template("story.html")

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', port=8000)
