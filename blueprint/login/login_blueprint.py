from flask import Blueprint, session, redirect, render_template, request, make_response, flash
from flask.ext.bcrypt import check_password_hash
from app import forms, db, templates
from app.dbmodels import User, Friends
from app.forms import LoginForm, RegisterForm

login = Blueprint('login', __name__, template_folder = 'templates')

@login.route('/', methods = ['GET', 'POST'])
def index(page=1):
    login = LoginForm()
    #Check method
    if request.method == 'GET':
        if not('isLogged' in session) or (session['isLogged'] == False):
            return render_template('template_index.html', form = login, isLogged = False)
        else:
            return redirect ("/app/users")
    else:
        #Check if form data is valid
        if login.validate_on_submit():
            # Check if correct username
            user = User.query.filter_by(email = login.email.data)
            if (user.count() == 1) and (check_password_hash(user[0].password, login.passw.data)):
                session['username'] = login.email.data
                session['user_id'] = user[0].id
                session['isLogged'] = True
                #tapa 1
                friends = Friends.query.filter_by(user_id=user[0].id).paginate(page,10,False)
                return render_template('template_user.html', isLogged=True, friends=friends)
                #return redirect ("/users")
            else:
                flash('Wrong username or password given!')
                return render_template('template_index.html', form = login, isLogged = False)
            
        #Form data was not valid
        else:
            flash('Give proper information to email and password fields!')
            return render_template('template_index.html', form = login, isLogged = False)

@login.route('/register', methods = ['GET', 'POST'])
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

@login.route('/logout', methods=['GET'])
def logOut():
    session.clear()
    return redirect('/')