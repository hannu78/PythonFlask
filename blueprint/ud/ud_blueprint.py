from flask import Blueprint, session, redirect, render_template, request, make_response, flash
from app import forms, db, templates
from app.dbmodels import User, Friends
from werkzeug import secure_filename

# 1st argument is the name of the blueprint, 2nd is always __name__,
# 3rd argument tells the location of blueprint's templates and 4th
# is url_prefix
ud = Blueprint('ud', __name__, template_folder = 'templates', url_prefix = ('/app/'))

#/app/delete
@ud.route('delete/<int:id>')
def delete(id):
    # pass doesn't do anything, it just continues
    # pass
    friend = Friends.query.get(id)
    db.session.delete(friend)
    db.session.commit()
    user = User.query.get(session['user_id'])
    return render_template('template_user.html',isLogged=True,friends=user.friends)

@ud.route('update')
def update():
    #pass
    return "Update"

@ud.route('add', methods = ['GET', 'POST'])
def addFriend():
    form = forms.AddFriendForm()

    if request.method == 'GET':
        return render_template('template_friend.html', form = form, isLogged = True)
    else:
        if form.validate_on_submit():
            friend = Friends(form.name.data, form.address.data, form.age.data, session['user_id'])
            if form.upload_file.data:
                filename = secure_filename(form.upload_file.data.filename)
                form.upload_file.data.save('app/static/images/' + filename)
                friend.filename = '/static/images/' + filename
            db.session.add(friend)
            db.session.commit()
            flash("Friend named {0} added succesfully!".format(form.name.data))
            # Tapa 2 lisätä friend listalle
            user = User.query.get(session['user_id'])
            return render_template('template_user.html', isLogged=True, friends=user.friends)
        else:
            flash('Invalid information given. Please check the friend info.')
            return render_template('template_register.html', isLogged = True)
@ud.route('users',methods=['GET', 'POST'])
def listUsers():
    if not('isLogged' in session) or (session['isLogged'] == False):
        return redirect("/")
    else:
        user = User.query.filter_by(email=session['username']).first()
        userid = user.id
        friends = Friends.query.filter_by(user_id = userid).paginate(1,10,False)
        return render_template('template_user.html',isLogged=True, friends = friends)

def before_request():
    if not 'isLogged' in session:
        return redirect('/')
# .before_request method runs the given function before letting any request to be run in routes
ud.before_request(before_request)