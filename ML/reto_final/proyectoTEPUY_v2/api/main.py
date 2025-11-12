from flask import Flask

app = Flask(__name__)

@app.route("/") #endpoint
def hello_world():
    return "API <p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(port=8055,debug=True)
