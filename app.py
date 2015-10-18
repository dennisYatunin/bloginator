from flask import Flask, render_template, request, session, redirect, url_for
import utils

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

## Checks the username and password with the utils function auth()
    
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        userid = utils.auth(username, password)

        if userid != -1:
            session['username'] = username
            session['password'] = password
            session['userid'] = userid
            return redirect(url_for('home'))
        else:
            return render_template("login.html", err="Incorrect password or username")

    else:
        return render_template("login.html")


# Pops the session. Then sends the user to a logged out page
@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template("logout.html")


@app.route('/new', methods='POST')
def new():
    title = request.form['title']
    line = request.form['line']
    return render_template("newstory.html")

# Very similar to log in, just checks whether the two passwords are the same, then adds the user using a utils function
@app.route('/register')
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if (request.form['password2'] != password):
            return """ <h1> Error, passwords are not the same </h1> """
        else:
            utils.addUser(username, password)
            return redirect(url_for('new'))
    else:
        return render_template("register.html")


@app.route('/story')
@app.route('/story/<ID>', methods=['GET','POST'])
def story(ID = None):
    story = ""
    if ID == None: #or if id does not exist?
	story= "ERROR not a valid story"
    else:
	newline = ""
	if request.method == 'POST':
	    newline = request.form['line']
	    #sanitize newline
	    #run method to add line to database
	#run method to get story based on id
	#temp until those things exist
	story = "Mary had a little lamb. "
	story += newline
    return render_template("story.html", id = ID, story = story)

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "???"
    app.run('0.0.0.0', port=8000)
