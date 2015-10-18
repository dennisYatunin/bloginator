from flask import Flask, render_template, request, session, redirect, url_for, escape
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
            session['logged_in'] = True
            session['userid'] = userid
            return redirect(url_for('home'))
        else:
            return render_template("login.html", err="Incorrect password or username")

    else:
        return render_template("login.html")



# Pops the session. Then sends the user to a logged out page
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('userid', None)
    return redirect("login")

@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        line = request.form['line']
    return render_template("newstory.html")

<<<<<<< HEAD
# Very similar to log in, just checks whether the two passwords are the same, then adds the user using a utils function
@app.route('/register')
=======
@app.route('/register', methods = ['GET', 'POST'])
>>>>>>> d8891613cecf9f665eb634a629b163bc79ea7a9e
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if (request.form['password2'] != password):
            return """ <h1> Error, passwords are not the same </h1> """
        else:
            print username + " " + password
            utils.addUser(username, password)
            return redirect(url_for('new'))
    else:
        return render_template("register.html")


@app.route('/story')
@app.route('/story/<int:ID>', methods=['GET','POST'])
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
	story = utils.getStory(ID)
	story += newline
    return render_template("story.html", id = ID, story = story)

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "V\xd7\x94<\xb50\xca\n\xf9\xa0@\x17\x06(\x17-\x8f\xf39\x83\xa2\xfcm\x14"
    app.run('0.0.0.0', port=8000)
