from app import app
from flask import render_template, request, make_response, flash, redirect, session
from app.forms import LoginForm, RegisterForm, AddFriendForm, FriendTable
from app.dbmodels import User, Friends
from app import db

@app.route('/', methods = ['GET', 'POST'])
def index():
    login = LoginForm()
    #Check method
    if request.method == 'GET':
        if not('isLogged' in session) or (session['isLogged'] == False):
            return render_template('template_index.html', form = login, isLogged = False)
        else:
            return redirect ("/users")
    else:
        #Check if form data is valid
        if login.validate_on_submit():
            # Check if correct username and password
            user = User.query.filter_by(email = login.email.data).filter_by(password = login.passw.data)
            if user.count() == 1:
                session['username'] = login.email.data
                session['user_id'] = user[0].id
                session['isLogged'] = True
                #return render_template('template_user.html')
                return redirect ("/users")
            else:
                flash('Wrong username or password given!')
                return render_template('template_index.html', form = login, isLogged = False)
            
        #Form data was not valid
        else:
            flash('Give proper information to email and password fields!')
            return render_template('template_index.html', form = login, isLogged = False)
@app.route('/user/<name>')
def user(name):
    return render_template('template_name.html', uname=name)
    
@app.route('/user', methods=['GET', 'POST'])
def userParams():
    name = request.args.get('name')
    return render_template('template_name.html', uname=name)

@app.route('/register', methods = ['GET', 'POST'])
def registerUser():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('template_register.html', form = form, isLogged = False)
    else:
        if form.validate_on_submit():
            user = User(form.email.data, form.passw.data)
            try: 
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                flash('Username already in use!')
                return render_template('template_register.html', form = form, isLogged = False)
            flash("Name {0} registered succesfully!".format(form.email.data))
            return redirect ("/")
        else:
            flash('Invalid email address or no password given.')
            return render_template('template_register.html', isLogged = False)

@app.route('/users',methods=['GET', 'POST'])
def listUsers():
    if not('isLogged' in session) or (session['isLogged'] == False):
        return redirect("/")
    else:
        user = User.query.filter_by(email=session['username']).first()
        userid = user.id
        friends = Friends.query.filter_by(user_id = userid)
        return render_template('template_user.html', friends = friends)
            

@app.route('/add', methods = ['GET', 'POST'])
def addFriend():
    form = AddFriendForm()
    user = User.query.filter_by(email=session['username']).first()
    userid = user.id
    print(userid)
    if request.method == 'GET':
        return render_template('template_friend.html', form = form, isLogged = True)
    else:
        if form.validate_on_submit():
            friend = Friends(form.name.data, form.address.data, form.age.data, userid)
            db.session.add(friend)
            db.session.commit()
            flash("Friend named {0} added succesfully!".format(form.name.data))
            # Tapa 2 lisätä friend listalle
            #user = User.query.get(session['user_id'])
            return redirect('/users')
        else:
            flash('Invalid information given. Please check the friend info.')
            return render_template('template_register.html', isLogged = True)
@app.route('/logout', methods=['GET'])
def logOut():
    session.clear()
    return redirect('/')
#this is a comment

"""
    this is a 
    multiline comment
"""