from flask import Flask,render_template,request,flash,session,redirect,url_for
#from Chat import Anonymous
import sqlite3
connection = sqlite3.connect('chattopiadb.db')
cursor = connection.cursor()
#cursor.execute('CREATE TABLE user (userID INTEGER PRIMARY KEY, username varchar(20) NOT NULL, password varchar(20) NOT NULL, picture varchar(255) NOT NULL)')

purchases = []

app = Flask(__name__)
app.secret_key = 'SECRET KEY'

#session["USERNAME"] = None

def MakeComments():
    comments = []
    connection = sqlite3.connect('chattopiadb.db')
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM chat")
    count = cursor.fetchone()[0] + 1
    for i in range(1,count):
        cursor.execute("SELECT chat FROM chat WHERE chatID = ?", [i])
        comment = cursor.fetchone()[0]
        comments.append(comment)
        cursor.execute("SELECT user FROM chat WHERE chatID = ?", [i])
        pid = cursor.fetchone()[0]
        cursor.execute("SELECT username FROM user WHERE userID = ?", [pid])
        person = cursor.fetchone()[0]
        comments.append("Sent By: " + person)
    return comments

def GetPurchases():
    connection = sqlite3.connect('chattopiadb.db')
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM chat")
    count = cursor.fetchone()[0]
    for i in range(1,count):
        cursor.execute("SELECT user FROM purchases WHERE purchasesID = ?", [i])
        pid = cursor.fetchone()[0]
        cursor.execute("SELECT username FROM user WHERE userID = ?", [pid])
        person = cursor.fetchone()[0]

@app.route('/chat')
def chat():
    comments = MakeComments()
    return render_template('Chat.html',comments=comments)

@app.route('/chat', methods=['GET', 'POST'])
def chat_post():
    connection = sqlite3.connect('chattopiadb.db')
    cursor = connection.cursor()
    comment = request.form["chatbar"]
    if comment.lower() == "/logout":
        return redirect(url_for('login'))
    elif comment.lower() == "/shop":
        return redirect(url_for('shop'))
    else:
        cursor.execute("SELECT userID FROM user WHERE username = ?", [session["USERNAME"]])
        cursor.execute('INSERT INTO chat(chat, user) VALUES(?,?)', (comment, cursor.fetchone()[0]))
        connection.commit()
        comments = MakeComments()
        return render_template('Chat.html',comments=comments)

@app.route('/shop', methods=['GET', 'POST'])
def shop_post():
    return render_template('Shop.html')

@app.route('/shop')
def shop():
    return render_template('Shop.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_post():
    return render_template('Checkout.html')

@app.route('/checkout')
def checkout():
    return render_template('Checkout.html')

@app.route('/register')
def register():
    return render_template('Register.html')

@app.route('/register', methods=['GET', 'POST'])
def register_post():
    connection = sqlite3.connect('chattopiadb.db')
    cursor = connection.cursor()
    usern = request.form['user']
    passw = request.form['pass']
    cpassw = request.form['cpass']
    if len(usern) >= 3 and len(usern) <= 20:
        if passw == cpassw:
            taken = False
            cursor.execute("SELECT * FROM user WHERE username = ?", [usern])
            if cursor.fetchone() == None:
                cursor.execute('INSERT INTO user(username, password) VALUES(?,?)', (usern, passw))
                connection.commit()
                return redirect(url_for('login'))
            else:
                flash("Username is taken")
                return render_template('Register.html')
        else:
            flash("Passwords don't match")
            return render_template('Register.html')
    else:
        flash("Username is too long or short")
        return render_template('Register.html')

@app.route('/')
@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_post():
    connection = sqlite3.connect('chattopiadb.db')
    cursor = connection.cursor()
    usern = request.form['user']
    passw = request.form['pass']
    cursor.execute("SELECT * FROM user WHERE username = ?", [usern])
    if cursor.fetchone() != None:
        cursor.execute("SELECT password FROM user WHERE username = ?", [usern])
        if cursor.fetchone()[0] == passw:
            session["USERNAME"] = usern
            return redirect(url_for('chat'))
    flash("Incorrect username or password")
    return render_template('Login.html')

if __name__ == '__main__':
    app.run(debug=True)