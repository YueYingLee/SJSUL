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
              if valid_user.role == 'Admin':
                  return redirect(url_for('adminHome'))  # redirect to admin homepage
              
              elif valid_user.role == 'Student':
                  return redirect(url_for('generalHome'))  # redirect to general homepage
              
              elif valid_user.role == 'Faculty':
                  return redirect(url_for('generalHome'))  # redirect to general homepage
              
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

@myapp_obj.route("/generalHome")
@login_required
def generalHome():
    user = current_user
    username = user.username
    users = User.query.all()
    return render_template('generalHome.html', username = username, users = users)

@myapp_obj.route("/adminHome")

@login_required
def adminHome():
    user = current_user
    username = user.username
    users = User.query.all()
    return render_template('adminHome.html', username = username, users = users)

@myapp_obj.route("/approve_user/<int:user_id>", methods=["POST"])
def approve_user(user_id):
    if request.method == "POST":
        user = User.query.get(user_id)
        if user and user.approved == False:
            user.approved = True
            user.role = user.registered_role
            db.session.commit()
            flash("User approved successfully!")
        else:
            flash("User not found or already approved!")
    # Redirect back to the admin dashboard
    return redirect(url_for("adminHome"))


@myapp_obj.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if request.method == "POST":
        if current_user.role == 'Admin':
          user = User.query.get(user_id)
          if user:
            user.approved = True
            db.session.delete(user)
            db.session.commit()
            flash("User deleted successfully!")
          else:
            flash("User not found!")
        else:
             flash('You do not have permission to delete users.')
    return redirect(url_for("adminHome"))


@myapp_obj.route("/reject_user/<int:user_id>", methods=["POST"])
def reject_user(user_id):
    if request.method == "POST":
        if current_user.role == 'Admin':
          user = User.query.get(user_id)
          if user and user.approved == False:
            db.session.delete(user)
            db.session.commit()
            flash("User rejected successfully!")
        else:
            flash("User not found or already rejected!")
    return redirect(url_for("adminHome"))