from flask import Flask, render_template, request, session, redirect, url_for
import utils

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    valid_stories = utils.getAllIds()
    storyDict = {}
    for i in valid_stories:
        storyDict[i] = utils.getTitle(i)
    return render_template("home.html", storyDict=storyDict)

# Checks the username and password with the utils function auth()
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


@app.route('/new', methods=['GET', 'POST'])
def new():
    title = ""
    line = ""
    if request.method == 'POST' and session['logged_in']:
        title = request.form['title']
        line = request.form['line']
        storyId = utils.newStory(title)
        utils.newLine(storyId, session['userid'], line)
        return redirect(url_for("home"))
    else:
        return render_template("newStory.html")


# Very similar to log in, just checks whether the two passwords are the same
# then adds the user using a utils function
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if (request.form['password2'] != password):
            return render_template("register.html", err="Error, passwords are not the same")
        else:
            print username + " " + password
            addedUser = utils.addUser(username, password)
            if (not addedUser):  # user already existed in the database.
                return render_template("register.html", err="User already exists")
            return redirect(url_for('new'))
    else:
        return render_template("register.html")


@app.route('/story')
@app.route('/story/<ID>', methods=['GET', 'POST'])
def story(ID=None):
    story = ""
    if ID is None:  # or if id does not exist?
        story = "ERROR not a valid story"
    else:
        newline = ""
        if (request.method == 'POST' and session['logged_in']):
            newline = request.form['line']
            utils.newLine(ID, session['userid'], newline)
        story = utils.getStory(ID)
    return render_template("story.html", id=ID, story=story)


@app.route('/editLine')
@app.route('/editLine/<storyID>/<lineID>', methods=['GET', 'POST'])
def editLine(storyID=None, lineID=None):
    return render_template("editLine.html", comment="123")


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "test"  # "V\xd7\x94<\xb50\xca\n\xf9\xa0@\x17\x06(\x17-\x8f\xf39\x83\xa2\xfcm\x14"
    app.run('0.0.0.0', port=8000)
