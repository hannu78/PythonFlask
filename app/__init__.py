from flask import Flask

app = Flask(__name__)
# app.config([SERVER_NAME]='localhost:3000')
app.config.from_object('config')
from app import routers