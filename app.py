from flask import Flask, render_template, request, session, redirect, url_for
import utils

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        button = request.form['button']
        userid = utils.auth(username, password)
        if button == "cancel":
            return redirect(url_for('home'))

        if userid != -1:
            session['username'] = username
            session['password'] = password
            session['userid'] = userid
            return redirect(url_for('home'))
        else:
            error = "Bad username or password"
            return render_template("login.html", err = error)


    # if request.method = 'POST':
    #     user = request.form['username']
    #     pswd = request.form['password']
    #     if(util.auth(user,pswd)){
    #         session['loggedin']= True

    # return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("logout.html")



@app.route('/new', method='POST')
def new():
    title = request.form['title']
    line = request.form['line']
    return render_template("newstory.html")

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
