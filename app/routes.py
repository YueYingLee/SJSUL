from flask import render_template
from flask import redirect, request, session, url_for
from flask import flash, get_flashed_messages
from app import myapp_obj, db
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from datetime import datetime
from app.models import User, Books, BorrowHistory, Profile
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
              
              elif valid_user.role == 'Librarian':
                  return redirect(url_for('librarianHome'))  # redirect to libranian homepage
              
              elif valid_user.role == 'Student':
                  return redirect(url_for('generalHome'))  # redirect to general homepage
              
              elif valid_user.role == 'Faculty':
                  return redirect(url_for('generalHome'))  # redirect to general homepage
              
              elif valid_user.role == 'Public':
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

@myapp_obj.route("/librarianHome")
@login_required
def librarianHome():
    user = current_user
    username = user.username
    users = User.query.all()
    books = Books.query.all()
    return render_template('librarianHome.html', username = username, users = users, books = books)

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


@myapp_obj.route("/change_user_role/<int:user_id>", methods=["GET", "POST"])
def change_user_role(user_id):
    if request.method == "POST":
        if current_user.role == 'Admin':
          user = User.query.get(user_id)
          if user:
            new_role = request.form.get("new_role")
            if new_role:
              if new_role != user.role:
                  user.role = new_role
                  db.session.commit()
                  flash("User role updated successfully!")
              else:
                 flash("New role is the same as the current role")
            else:
               flash ('No new roles are provided')
          else:
            flash("User not found")
        else:
          flash('You do not have permission to change roles.')
    return redirect(url_for("adminHome"))

#Function to manage books
@myapp_obj.route("/manage_books", methods = ['GET', 'POST'])
@login_required
def manage_books():
    #books = Books.query.filter_by(recipient_id = current_user.id).all()
    books = Books.query.filter(Books.count > 0).all()
    user = current_user
    username = user.username      
    return render_template('manageBooks.html', username = username, books=books)



@myapp_obj.route("/delete_book/<int:books_id>", methods=["POST"])
def delete_book(books_id):
    if request.method == "POST":
        if current_user.role == 'Librarian':
            book = Books.query.get(books_id)
            if book:
                if book.count > 0: 
                    book.count = book.count -1
                    db.session.commit()
                    flash("One copy of the book deleted successfully!")
                    if book.count == 0 :
                        db.session.delete(book)
                        db.session.commit()
                        flash("Copies of book deleted successfully!")   
            else: #no book found in the book table
                flash("Book not found to delete!")
        else:
                flash('You do not have permission to delete books.')
    return redirect(url_for("manage_books")) 

@myapp_obj.route("/add_book/<int:books_id>", methods=["POST"])
def add_book(books_id):
    if request.method == "POST":
        if current_user.role == 'Librarian':
            book = Books.query.get(books_id)
            if book:
                if book.count > 0: 
                    book.count = book.count -1
                    db.session.commit()
                    flash("One copy of the book deleted successfully!")
                else: 
                    db.session.delete(book)
                    db.session.commit()
                    flash("Copies of book deleted successfully!")   
            else: #no book found in the book table
                flash("Book not found to delete!")
        else:
                flash('You do not have permission to add books.')
    return redirect(url_for("manage_books")) 

