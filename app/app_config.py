from flask import Flask
from app.urls import blueprint
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



def register_blueprint():
    app.register_blueprint(blueprint, url_prefix='')
