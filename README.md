# SJSUL
CMPE 132 Project developed by Yue Ying Lee 

## Introduction 
This is a fictitious library, a simple web-based system which perform primary user enrollment, authentication, and authorization functions. The Role-Based Acccess Control (RBAC) model is used during the design of the project. It runs on Flask and SQLAlchemy. 

## List of roles and their accesses
1. Admin 
- Approve and reject user 
- Change user's role 
- Delete user  
- View all users and search users
- View all books and search books
- Add and delete books 

2. Librarian
- View all books and search books
- Add and delete books 

3. Student 
- View all books and search books
- Borrow and return books 
- Check their current borrows

4. Faculty
- View all books and search books
- Borrow and return books 
- Check their current borrows

5. Public 
- View books 
- Search books

## Instructions to run the project 
1. Clone this project in your Linux terminal `git clone https://github.com/YueYingLee/SJSUL.git`
2. Navigate to the folder
  `cd SJSUL`
3.  Create a virtual environment named as venv.
`python3 -m venv venv`
4. Activate the virtual environment 
`source venv/bin/activate`
5. Download the dependencies needed 
`pip3 install -r dependencies.txt`
6. Run the application after installation of dependencies
`python3 run.py`
7. Deactivate the virtual environment once you are done 
`deactivate`
