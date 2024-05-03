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
from app.forms import loginUser, registerUser, addBook

from sqlalchemy import desc

#landing page 
@myapp_obj.route("/")
def landing():
    return render_template('landing.html')

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
            flash('Successful registration!', category = 'success')
            return redirect(url_for('login'))
          else :
             flash('The username is not available. Please choose another username.',  category ='error')
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
                  return redirect(url_for('publicHome'))  # redirect to general homepage
              
            else :
                flash('Your account need to be approved by admin before accessing',category ='error')
          else :
             flash(f'Invalid password. Try again.',category ='error')
        else: 
             flash(f'Invalid username. Try again or register an account.',category ='error')  

    return render_template('login.html', loginForm=loginForm)

@myapp_obj.route("/logout", methods = ['GET', 'POST'])
@login_required
def logout():
       logout_user()
       return redirect(url_for('landing'))

@myapp_obj.route("/generalHome")
@login_required
def generalHome():
    user = current_user
    username = user.username
    role = user.role
    users = User.query.all()
    return render_template('generalHome.html', username = username, users = users, role=role)


@myapp_obj.route("/publicHome")
@login_required
def publicHome():
    user = current_user
    username = user.username
    role = user.role
    users = User.query.all()
    books = Books.query.filter(Books.current_count >= 0).all()
    return render_template('publicHome.html', username = username, users = users, books = books, role=role)

@myapp_obj.route("/librarianHome")
@login_required
def librarianHome():
    user = current_user
    username = user.username
    role = user.role
    users = User.query.all()
    books = Books.query.all()
    return render_template('librarianHome.html', username = username, users = users, books = books, role=role)

@myapp_obj.route("/adminHome")
@login_required
def adminHome():
    user = current_user
    username = user.username
    role = user.role
    users = User.query.all()
    return render_template('adminHome.html', username = username, users = users, role= role)

@myapp_obj.route("/approve_user/<int:user_id>", methods=["POST"])
def approve_user(user_id):
    if request.method == "POST":
        user = User.query.get(user_id)
        if user and user.approved == False:
            user.approved = True
            user.role = user.registered_role
            db.session.commit()
            flash("User approved successfully!" ,category = 'success')
        else:
            flash("User not found or already approved!" , category ='error')
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
            flash("User deleted successfully!", category = 'success')
          else:
            flash("User not found!", category ='error')
        else:
             flash('You do not have permission to delete users.' , category ='error')
    return redirect(url_for("adminHome"))


@myapp_obj.route("/reject_user/<int:user_id>", methods=["POST"])
def reject_user(user_id):
    if request.method == "POST":
        if current_user.role == 'Admin':
          user = User.query.get(user_id)
          if user and user.approved == False:
            db.session.delete(user)
            db.session.commit()
            flash("User rejected successfully!", category = 'success')
        else:
            flash("User not found or already rejected!", category ='error')
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
                  flash("User role updated successfully!", category = 'success')
              else:
                 flash("New role is the same as the current role",category ='error')
            else:
               flash ('No new roles are provided',category ='error')
          else:
            flash("User not found",category ='error')
        else:
          flash('You do not have permission to change roles.' ,category ='error')
    return redirect(url_for("adminHome"))

#Function to manage books
@myapp_obj.route("/manage_books", methods = ['GET', 'POST'])
@login_required
def manage_books():
    if current_user.role == 'Librarian':
        #books = Books.query.filter_by(recipient_id = current_user.id).all()
        books = Books.query.filter(Books.current_count >= 0).all()
        user = current_user
        username = user.username      
    else:
        flash('You do not have permission to manage books.' ,category ='error')
        if current_user.role == 'Admin':
                  return redirect(url_for('adminHome'))  # redirect to admin homepage
                         
        elif  current_user.role == 'Student' or current_user.role == 'Faculty':
            return redirect(url_for('generalHome'))  # redirect to general homepage
        
        elif current_user.role == 'Public':
            return redirect(url_for('publicHome'))  # redirect to general homepage
    return render_template('manageBooks.html', username = username, books=books)


@myapp_obj.route("/delete_book/<int:books_id>", methods=["POST"])
@login_required
def delete_book(books_id):
    if request.method == "POST":
        if current_user.role == 'Librarian':
            book = Books.query.get(books_id)
            if book:
                if book.max_count > 0: 
                    book.max_count = book.max_count -1
                    book.current_count = book.current_count -1
                    db.session.commit()
                    flash("One copy of the book deleted successfully!", category = 'success')
                    if book.max_count == 0 :
                        db.session.delete(book)
                        db.session.commit()
                        flash("Copies of book deleted successfully!", category = 'success')   
            else: #no book found in the book table
                flash("Book not found to delete!", category ='error')
        else:
                flash('You do not have permission to delete books.', category ='error')
                if current_user.role == 'Admin':
                  return redirect(url_for('adminHome'))  # redirect to admin homepage
                         
                elif  current_user.role == 'Student' or current_user.role == 'Faculty':
                    return redirect(url_for('generalHome'))  # redirect to general homepage
                
                elif current_user.role == 'Public':
                    return redirect(url_for('publicHome'))  # redirect to general homepage
    return redirect(url_for("manage_books")) 

@myapp_obj.route("/add_book", methods = ['GET', 'POST'])
@login_required
def add_book():
    addBookForm  = addBook()
    if current_user.role == 'Librarian':
        if addBookForm.validate_on_submit():
            new_book = Books(title=addBookForm.title.data, author=addBookForm.author.data, genre=addBookForm.genre.data, max_count=addBookForm.max_count.data, current_count =addBookForm.max_count.data)
            db.session.add(new_book)
            db.session.commit()
            flash('Added book successfully!',category = 'success')
            return redirect(url_for('manage_books'))
    else :
            flash('You do not have permission to add book', category ='error')
            if current_user.role == 'Admin':
                  return redirect(url_for('adminHome'))  # redirect to admin homepage
                         
            elif  current_user.role == 'Student' or current_user.role == 'Faculty':
                return redirect(url_for('generalHome'))  # redirect to general homepage
            
            elif current_user.role == 'Public':
                return redirect(url_for('publicHome'))  # redirect to general homepage
    return render_template('addBooks.html', addBookForm= addBookForm)


#Funciton to view book for users such as Student,Faculty
@myapp_obj.route("/view_book", methods = ['GET', 'POST'])
@login_required
def view_book():        
    books = Books.query.filter(Books.current_count >= 0).all()
    borrowHistory = BorrowHistory.query.filter(BorrowHistory.returned == False).all()
    user = current_user
    username = user.username      
    return render_template('viewBook.html', username = username, books=books, borrowHistory = borrowHistory)
     

@myapp_obj.route("/borrow_book/<int:books_id>", methods=["POST"])
@login_required
def borrow_book(books_id):
    if request.method == "POST":
        if current_user.role == 'Student' or current_user.role == 'Faculty':
            book = Books.query.get(books_id)
            if book:
                if book.current_count > 0:
                    new_borrow = BorrowHistory(user_id=current_user.id, book_id=book.id, borrow_date = datetime.now(), returned = False)
                    book.current_count = book.current_count -1
                    db.session.add(new_borrow)                    
                    db.session.commit()
                    flash("Book borrowed successfully!",category = 'success')
                else: #if all books count are borrowed
                    flash("All copies of this book are currently borrowed.", category ='error')
            else:
                flash("Book not found.")
        else:
            flash("Only students or faculty can borrow books.", category ='error')
    return redirect(url_for("view_book"))


@myapp_obj.route("/return_book/<int:books_id>", methods=["POST"])
@login_required
def return_book(books_id):
    if request.method == "POST":
        if current_user.role == 'Student' or current_user.role == 'Faculty':
            book = Books.query.get(books_id)
            if book:
                    borrow_history = BorrowHistory.query.filter_by(user_id=current_user.id, book_id=book.id, returned =False).first()
                    borrow_history.return_date = datetime.now()  # Set the return date
                    borrow_history.returned = True # set the return status to be true
                    if (book.current_count +1 <= book.max_count):
                        book.current_count = book.current_count + 1
                    db.session.delete(borrow_history)
                    db.session.commit()
                    flash("You returned book successfully!",category = 'success')   
            else: #no book found in the book table
                flash("Book not found to return!", category ='error')
        else:
                flash('You do not have permission to return books.', category ='error')
    return redirect(url_for("view_book")) 

