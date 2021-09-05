from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Cardgame')

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

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', title='flask test', name=name)

## Omajinai
if __name__ == "__main__":
    app.run(debug=True)