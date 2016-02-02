from app import app
from flask import render_template, request, make_response, flash, redirect
from app.forms import LoginForm, RegisterForm, AddFriendForm
from app.dbmodels import User, Friends
from app import db

@app.route('/', methods = ['GET', 'POST'])
def index():
    login = LoginForm()
    #Check method
    if request.method == 'GET':
        return render_template('template_index.html', form = login)
    else:
        #Check if form data is valid
        if login.validate_on_submit():
            print(login.email.data)
            print(login.passw.data)
            return render_template('template_user.html')
        #Form data was not valid
        else:
            flash('Give proper information to email and password fields!')
            return render_template('template_index.html', form = login)
@app.route('/user/<name>')
def user(name):
    return render_template('template_name.html', uname=name)
    
@app.route('/user', methods=['GET', 'POST'])
def userParams():
    browser = request.headers.get('User-Agent')
    name = request.args.get('name')
    return render_template('template_name.html', uname=name, browser=browser)

@app.route('/register', methods = ['GET', 'POST'])
def registerUser():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('template_register.html', form = form)
    else:
        if form.validate_on_submit():
            user = User(form.email.data, form.passw.data)
            db.session.add(user)
            db.session.commit()
            flash("Name {0} registered succesfully!".format(form.email.data))
            return redirect ("/")
        else:
            flash('Invalid email address or no password given.')
            return render_template('template_register.html')

@app.route('/users',methods=['GET'])
def listUsers():
	user = User.query.all()
	print(user[0].username)

@app.route('/add', methods = ['GET', 'POST'])
def addFriend():
    form = AddFriendForm()
    if request.method == 'GET':
        return render_template('template_friend.html', form = form)
    else:
        if form.validate_on_submit():
            friend = Friends(form.name.data, form.address.data, form.age.data, form.email.data)
            db.session.add(friend)
            db.session.commit()
            flash("Friend named {0} added succesfully!".format(form.name.data))
        else:
            flash('Invalid information given. Please check the friend info.')
            return render_template('template_register.html')

#this is a comment

"""
    this is a 
    multiline comment
"""