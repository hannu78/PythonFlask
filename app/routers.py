from app import app
from flask import render_template, request, make_response
from app.forms import LoginForm

@app.route('/', methods = ['GET', 'POST'])
def index():
    login = LoginForm()
    return render_template('template_index.html', form = login)

@app.route('/user/<name>')
def user(name):
    return render_template('template_name.html', uname=name)
    
@app.route('/user', methods=['GET', 'POST'])
def userParams():
    browser = request.headers.get('User-Agent')
    name = request.args.get('name')
    return render_template('template_name.html', uname=name, browser=browser)

print("This isn't included in index() function")

#this is a comment

"""
    this is a 
    multiline comment
"""