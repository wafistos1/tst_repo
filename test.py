from flask import Flask
from  main import register_user
from flask_api import status


app = Flask(__name__)

@app.route("/test")
def test():
    result = register_user()
    return result, status.HTTP_201_CREATED


@app.route("/")
def hello_world():
    
    return '''<h5> Welcome to my app Click on <a href="127.0.0.1:5000/test" >Test</a> to resolve Captcha</h3>'''