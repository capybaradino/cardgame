from flask import Flask, render_template, request
import sqlite3
import names
import uuid
app = Flask(__name__)


@app.route('/')
def index():
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    email = request.headers.get("X-Forwarded-Email")
    cur.execute("select nickname from user where email = '" + email + "'")
    username = ''.join(cur.fetchone())
    if(username is None):
        uid = str(uuid.uuid4())
        username = names.get_last_name()
        cur.execute("insert into user values ('" + uid +
                    "','" + email + "','" + username + "')")
        con.commit()

    con.close()

    return render_template('index.html', title='Cardgame', username=username)


@app.route('/chkheaders/')
def chkheaders():
    headers = "<table border=1>"
    for header in request.headers:
        headers += "<tr>"
        headers += "<td>" + header[0] + "</td><td>" + header[1] + "</td>"
        headers += "</tr>"
        #envs += request.headers.get("Host")
    headers += "</table>"
    return render_template('chkheaders.html', title='Check Headers', headers=headers)


@app.route('/chkusers/')
def chkusers():
    headers = "<table border=1>"
    con = sqlite3.connect('user.db')
    cur = con.cursor()

    for row in cur.execute('select * from user'):
        headers += "<tr>"
        for str in row:
            headers += "<td>" + str + "</td>"
        headers += "</tr>"
        #envs += request.headers.get("Host")
    headers += "</table>"

    con.close()

    return render_template('chkheaders.html', title='Check Users', headers=headers)


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', title='flask test', name=name)


# Omajinai
if __name__ == "__main__":
    app.run(debug=True)
