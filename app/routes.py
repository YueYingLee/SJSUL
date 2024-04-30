from flask import render_template
from flask import redirect, request, session, url_for
from flask import flash, get_flashed_messages
from app import myapp_obj, db
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from datetime import datetime
from app.models import User, Role, Profile, Books, user_roles
from app.forms import LoginForm, registerUser

from sqlalchemy import desc


@myapp_obj.route("/")
@myapp_obj.route("/register", methods =['GET', 'POST'])
def register():
        registerForm  = registerUser()
        if registerForm.validate_on_submit():
          same_Username = User.query.filter_by(username = registerForm.username.data).first()
          if same_Username == None:
            user = User(username= registerForm.username.data)
            user.set_password(registerForm.password.data) 
            db.session.add(user)
            db.session.commit()
            selected_role = registerForm.role.data
            print(f"Selected role: {selected_role}")
            role = Role.query.filter_by(name=selected_role).first()
            if role:
              print(f"Role found: {role}")
              user_role = user_roles(user_id=user.id, role_id=role.id)
            else:
              print("Role not found")
           
            db.session.add(user_role)
            db.session.commit()
            flash('Sucessful registration')
            #return redirect('/login')
          else :
             flash('The username is not available. Please choose another username.')
        return render_template('register.html', registerForm=registerForm)



@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        valid_user = User.query.filter_by(username = form.username.data).first()
        if valid_user != None:
          if valid_user.check_password(form.password.data)== True:
             login_user(valid_user)
             return redirect(url_for('homepage'))
          else :
             flash(f'Invalid password. Try again.')
        else: 
             flash(f'Invalid username. Try again or register an account.')  

    return render_template('login.html', form=form)

@myapp_obj.route("/logout", methods = ['GET', 'POST'])
@login_required
def logout():
       logout_user()
       return redirect(url_for('login'))



