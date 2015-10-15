import sqlite3
conn = sqlite3.connect("blog.db")
c = conn.cursor()


#takes in username and pw (plaintext for now) and returns boolean
#if credentials are valid
def auth(user, pw):    
    q = "SELECT * FROM users where username = ? and pw = ? "
    result = c.execute(q, (user, pw) )
    return len(result) != 0


