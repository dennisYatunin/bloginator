from flask import Flask, render_template, request, session, redirect, url_for
import utils

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    storyList = utils.getAllStories()
    return render_template("home.html", storyList=storyList)

# Checks the username and password with the utils function auth()
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        username = utils.auth(username, password)
        if username != -1:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template("login.html",err="Incorrect password or username")
    else:
        return render_template("login.html")


# Pops the session. Then sends the user to a logged out page
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect("login")


@app.route('/new', methods=['GET', 'POST'])
def new():
    title = ""
    line = ""
    if request.method == 'POST' and session['logged_in']:
        title = request.form['title']
        line = request.form['line']
        storyId = utils.newStory(session["username"], title)
        utils.newLine(storyId, session['username'], line)
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
        password2 = request.form['password2']
        email = request.form["email"]
        error = utils.registrationError(username, password, password2)
        if error:
            return render_template("register.html", err=error)
        else:
            print username + " " + password
            addedUser = utils.addUser(username, password, email) #could user be added
            if (not addedUser): #user already existed in the database.
                return render_template("register.html", err="Error, user already exists")
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
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
            utils.newLine(ID, session['username'], newline)
        story = utils.getStoryLines(ID)
    return render_template("story.html", id=ID, story=story)


@app.route('/editLine')
@app.route('/editLine/<storyID>/<lineID>', methods=['GET', 'POST'])
def editLine(storyID=None, lineID=None):
    if request.method == 'GET' and storyID is not None and lineID is not None and session["logged_in"]:
        #Retrivies the comment and provides a form to edit
        return render_template("editLine.html", comment=utils.getLine(lineID))
    elif request.method == 'POST' and storyID is not None and lineID is not None:
        #Edits the line
        utils.editLine(session["username"],lineID,request.form['line'])
        return redirect(url_for("story", ID=storyID))
    else:
        return redirect(url_for("home"))

@app.route('/deleteLine')
@app.route('/deleteLine/<storyID>/<lineID>')
def deleteLine(storyID=None, lineID=None):
    if storyID is not None and lineID is not None and session["logged_in"]:
        #Checks if the story belongs to the user and deletes it
        if (utils.removeLine(session['username'],lineID)):
            return redirect(url_for("story", ID=storyID))
        else:
            return redirect(url_for("story", ID=storyID)) #render_template("story.html", ID=storyID, error="Failure to delete line!")
    else:
        return redirect(url_for("home"))

@app.route('/deleteStory')
@app.route('/deleteStory/<storyID>')
def deleteStory(storyID=None):
    if storyID is not None and session["logged_in"]:
        if utils.removeStory(session['username'], storyID):
            return redirect(url_for("home"))
        else:
            return render_template("home.html", error="Failure to delete story!")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.secret_key = utils.secret_key
    app.run('0.0.0.0', port=8000)
