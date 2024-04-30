# create_roles.py
from app import Role, User, db

def create_roles():
    admin = Role(id=1, name='Admin')
    libranian = Role(id=2, name= 'Libranian')
    student = Role(id=3, name='Student')
    faculty = Role(id=4, name='Faculty')
    public = Role(id=5, name='Public')

    db.session.add(admin)
    db.session.add(libranian)
    db.session.add(student)
    db.session.add(faculty)
    db.session.add(public)

    db.session.commit()
    print("Roles created successfully!")
    
create_roles()
