from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import Required, Email

class LoginForm(Form):
    email = StringField('Enter your email', validators = [Required(), Email()])
    passw = PasswordField('Enter password', validators = [Required()])
    submit = SubmitField('Login')

class RegisterForm(Form):
    email = StringField('Enter your email', validators = [Required(), Email()])
    passw = PasswordField('Enter password', validators = [Required()])
    submit = SubmitField('Register')
    
class AddFriendForm(Form):
    name = StringField('Enter name', validators = [Required()])
    address = StringField('Enter address', validators = [Required()])
    age = IntegerField('Enter age', validators = [Required()])
    upload_file = FileField('Upload Image')
    submit = SubmitField('Register')

from flask_table import Table, Col

# Declare your table
class FriendTable(Table):
    classes = "table table-bordered table-hover"
    name = Col('Name')
    address = Col('Address')
    age = Col('Age')