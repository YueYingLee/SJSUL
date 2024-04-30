from flask import render_template
from flask import redirect, request, session, url_for
from flask import flash, get_flashed_messages
from app import myapp_obj, db
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from datetime import datetime
from app.models import User, Profile, Books #, Role, user_roles
from app.forms import loginUser, registerUser

from sqlalchemy import desc


@myapp_obj.route("/")
@myapp_obj.route("/register", methods =['GET', 'POST'])
def register():
        registerForm  = registerUser()
        if registerForm.validate_on_submit():
          same_Username = User.query.filter_by(username = registerForm.username.data).first()
          if same_Username == None:
            user = User(username= registerForm.username.data, role ='Public', registered_role = registerForm.role.data, approved = False)
            user.set_password(registerForm.password.data) 
            db.session.add(user)
            db.session.commit()
            flash('Successful registration!')
            return redirect(url_for('login'))
          else :
             flash('The username is not available. Please choose another username.')
        return render_template('register.html', registerForm=registerForm)


@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    loginForm = loginUser()
    if loginForm.validate_on_submit():
        valid_user = User.query.filter_by(username = loginForm.username.data).first()
        if valid_user != None:
          if valid_user.check_password(loginForm.password.data)== True:
            if valid_user.approved:
              login_user(valid_user)
              return redirect(url_for('homepage'))
            else :
                flash('Your account need to be approved by admin before accessing')
          else :
             flash(f'Invalid password. Try again.')
        else: 
             flash(f'Invalid username. Try again or register an account.')  

    return render_template('login.html', loginForm=loginForm)

@myapp_obj.route("/logout", methods = ['GET', 'POST'])
@login_required
def logout():
       logout_user()
       return redirect(url_for('login'))

@myapp_obj.route("/homepage")
@login_required
def homepage():
    user = current_user
    user_fullname = user.fullname
    return render_template('homepage.html', user_fullname = user_fullname)

