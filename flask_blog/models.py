from sqlalchemy.orm import backref
from flask_blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))

req = db.Table('req', 
    db.Column('userid', db.Integer, db.ForeignKey('user.id')),
    db.Column('doctorid', db.Integer, db.ForeignKey('doctor.id'))
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password  = db.Column(db.String(60),nullable=False)
    f_name = db.Column(db.String(60),unique = False, nullable =True)
    image_file = db.Column(db.String(20), nullable=False, default='Anish_VIIT.jpg')
    phnumber = db.Column(db.Integer,unique=True, nullable=True)
    gender = db.Column(db.String(20),unique=False, nullable=True)
    age =  db.Column(db.Integer,unique=False, nullable=True)
    height = db.Column(db.Integer,unique=False, nullable=True)
    bpgroup =  db.Column(db.String(3),nullable=True)
    bplvl =  db.Column(db.Integer,nullable=True)
    oxylvl =  db.Column(db.Integer,nullable=True)
    mproblem =  db.Column(db.String(60),nullable=True)
    send = db.relationship('Doctor', secondary=req, backref=db.backref('request', lazy='dynamic'))
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}','{self.f_name}','{self.image_file}','{self.phnumber}','{self.gender}','{self.age}','{self.height}','{self.bpgroup}' '{self.oxylvl}','{self.mproblem})"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password  = db.Column(db.String(60),nullable=False)
    f_name = db.Column(db.String(60),unique = False, nullable =True)
    image_file = db.Column(db.String(20), nullable=False, default='doctor-croped.png')
    phnumber = db.Column(db.Integer,unique=True, nullable=True)
    specialization = db.Column(db.String(20),unique = False, nullable = True)
    degree = db.Column(db.String(20),unique = False, nullable = True)
    clinica= db.Column(db.String(80),unique = False, nullable = True)
    treatedp = db.Column(db.Integer,unique = False, nullable = True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}','{self.f_name}','{self.image_file}','{self.phnumber}','{self.specialization}','{self.degree}','{self.clinica}','{self.treatedp}')"

