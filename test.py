from flask import Flask
from  main import register_user


app = Flask(__name__)

@app.route("/")
def hello_world():
    result = register_user()
    return result