from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from flask_blog.models import Doctor, User

class RegistrationForm(FlaskForm):
    username = StringField('Username', #it can't be empty
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #if the username or email is already taken 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is Taken')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is Taken')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    
    f_name = StringField('Full Name',validators=[DataRequired()])

    phnumber = IntegerField('Phnumber', validators=[DataRequired()])

    gender = StringField('Gender',validators=[DataRequired()])

    age  = IntegerField('Age', validators=[DataRequired()])

    height = IntegerField('Height(cm)',validators=[DataRequired()])

    bpgroup = StringField('Blood Group', validators=[DataRequired()])

    bplvl = IntegerField('Blood Pressure Level', validators=[DataRequired()])

    oxylvl = IntegerField('Oxygen Level', validators=[DataRequired()])

    mproblem = StringField('Medical Issue', validators=[DataRequired()])

    submit = SubmitField('Submit Details')

    def validate_phnumber(self, phnumber):
        user = User.query.filter_by(phnumber=phnumber.data).first()
        if user:
            raise ValidationError('Phone Number is Taken')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', #it can't be empty
                           validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])]) 

    submit = SubmitField('Update Profile')

    #if the username or email is already taken 
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is Taken')
    


class DregistrationForm(FlaskForm):
    username = StringField('Username', #it can't be empty
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #if the username or email is already taken 
    def validate_username(self, username):
        doc = Doctor.query.filter_by(username=username.data).first()
        if doc:
            raise ValidationError('Username is Taken')
    
    def validate_email(self, email):
        doc =Doctor.query.filter_by(email=email.data).first()
        if doc:
            raise ValidationError('Email is Taken')

class DloginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DaccountForm(FlaskForm):
    f_name = StringField('Full Name', validators=[DataRequired()])

    phnumber = IntegerField('Phnumber', validators=[DataRequired()])
 
    specialization = StringField('Specialization', validators=[DataRequired()])

    degree = StringField('Degree', validators=[DataRequired()])

    clinicia = StringField('Clinic Area', validators=[DataRequired()])

    treatedp = StringField('Patients Treated', validators=[DataRequired()])

    def validate_phnumber(self, phnumber):
        user = User.query.filter_by(phnumber=phnumber.data).first()
        if user:
            raise ValidationError('Phone Number is Taken')
    
class DUpdateAccountForm(FlaskForm):
    username = StringField('Username', #it can't be empty
                           validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])]) 

    submit = SubmitField('Update Profile')

    #if the username or email is already taken 
    def validate_username(self, username):
        if username.data != current_user.username:
            doc = Doctor.query.filter_by(username=username.data).first()
            if doc:
                raise ValidationError('Username is Taken')
    
