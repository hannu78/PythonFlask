from flask import Flask
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
# app.config([SERVER_NAME]='localhost:3000')
app.config.from_object('config')
bootstrap = Bootstrap(app)
from app import routers