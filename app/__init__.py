from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from blueprint.ud.ud_blueprint import ud
from blueprint.login.login_blueprint import login

# Register the needed blueprints
app.register_blueprint(ud)
app.register_blueprint(login)
from app import routers