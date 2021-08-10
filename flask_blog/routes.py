import os
import secrets
from PIL import Image
from flask import  render_template, url_for, flash, redirect
from flask.globals import request
from flask_wtf import form
from flask_blog import app, db, bcrypt
from flask_blog.forms import  DUpdateAccountForm,DaccountForm, DregistrationForm, RegistrationForm,DloginForm, LoginForm, AccountForm , UpdateAccountForm
from flask_blog.models import User, Doctor
from flask_login import login_user, current_user

import nltk
#nltk.download('popular')
#nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('model.h5')
import json
import random

from googletrans import Translator
translator = Translator()

data_file = open('data.json').read()
intents = json.loads(data_file,strict=False)
#intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    #if sentence=="1":
    sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

app.static_folder = 'static'

@app.route("/chatbot")
def chatbot():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/homeH")
def homeH():
    return render_template('homeH.html')

@app.route("/homeM")
def homeM():
    return render_template('homeM.html')


@app.route("/register", methods=['GET','POST'])
def register():
    form =  RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created','success')#success green prompt
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route("/registerH", methods=['GET','POST'])
def registerH():
    form =  RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created','success')#success green prompt
        return redirect(url_for('loginH'))
    return render_template('registerH.html',form=form)

@app.route("/registerM", methods=['GET','POST'])
def registerM():
    form =  RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created','success')#success green prompt
        return redirect(url_for('loginM'))
    return render_template('registerM.html',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    form =  LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember = form.remember.data)
            return redirect(url_for('details'))
        else:
            flash('Login Unsuccessful Check username and passsword','danger')    
    return render_template('login.html',form=form)

@app.route("/loginH",methods=['GET','POST'])
def loginH():
    form =  LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('detailsH'))
        else:
            flash('Login Unsuccessful Check username and passsword','danger')    
    return render_template('loginH.html',form=form)

@app.route("/loginM",methods=['GET','POST'])
def loginM():
    form =  LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('detailsM'))
        else:
            flash('Login Unsuccessful Check username and passsword','danger')    
    return render_template('loginM.html',form=form)


@app.route("/details", methods=['GET','POST'])
def details():
    form  = AccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = current_user.email).first()
        user.f_name = form.f_name.data
        user.phnumber = form.phnumber.data
        user.gender = form.gender.data
        user.age = form.age.data
        user.height = form.height.data
        user.bpgroup = form.bpgroup.data
        user.bplvl = form.bplvl.data
        user.oxylvl = form.oxylvl.data
        user.mproblem = form.mproblem.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('after_login'))
    return render_template('details.html',form=form)
 
@app.route("/detailsH", methods=['GET','POST'])
def detailsH():
    form  = AccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = current_user.email).first()
        user.f_name = form.f_name.data
        user.phnumber = form.phnumber.data
        user.height = form.height.data
        user.gender = form.gender.data
        user.bpgroup = form.bpgroup.data
        user.age = form.age.data
        user.bplvl = form.bplvl.data
        user.oxylvl = form.oxylvl.data
        user.mproblem = form.mproblem.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('emrp'))
    return render_template('detailsH.html',form=form)

@app.route("/detailsM", methods=['GET','POST'])
def detailsM():
    form  = AccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = current_user.email).first()
        user.f_name = form.f_name.data
        user.phnumber = form.phnumber.data
        user.height = form.height.data
        user.gender = form.gender.data
        user.bpgroup = form.bpgroup.data
        user.age = form.age.data
        user.bplvl = form.bplvl.data
        user.oxylvl = form.oxylvl.data
        user.mproblem = form.mproblem.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('emrp'))
    return render_template('detailsM.html',form=form)


@app.route("/dp1")
def dp1():
    doc = Doctor.query.get(1)
    return render_template('doctor_profile1.html',doc = doc)

@app.route("/dp2")
def dp2():
    doc = Doctor.query.get(2)
    return render_template('doctor_profile2.html',doc = doc)

@app.route("/dp3")
def dp3():
    doc = Doctor.query.get(3)
    return render_template('doctor_profile3.html',doc = doc)

@app.route("/dpa1")
def dpa1():
    doc = Doctor.query.get(1)
    return render_template('dpa1.html',doc=doc)

@app.route("/dpa2")
def dpa2():
    doc = Doctor.query.get(2)
    return render_template('dpa2.html',doc = doc)

@app.route("/dpa3")
def dpa3():
    doc = Doctor.query.get(3)
    return render_template('dpa3.html',doc = doc)

@app.route("/drdetails", methods=['GET','POST'])
def drdetails():
    form  = DaccountForm()
    if form.validate_on_submit():
        doc = Doctor.query.filter_by(email = current_user.email).first()
        doc.f_name = form.f_name.data
        doc.phnumber = form.phnumber.data
        doc.specialization = form.specialization.data
        doc.degree = form.degree.data
        doc.clinicia = form.clinicia.data
        doc.treatedp = form.treatedp.data
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('EMRD'))
    return render_template('drdetails.html',form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext =os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
      
@app.route("/EMR", methods = ['GET','POST'])
def EMR():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('EMR'))
    if request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('EMR.html', image_file = image_file, form=form)

@app.route("/dregister",methods=['GET','POST'])
def dregister():
    form =  DregistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        doc = Doctor(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(doc)
        db.session.commit()
        flash(f'Your account has been created','success')#success green prompt
        return redirect(url_for('dlogin'))
    return render_template('dregister.html',form=form)


@app.route("/dlogin",methods=['GET','POST'])
def dlogin():
    form =  DloginForm()
    if form.validate_on_submit():
        doc = Doctor.query.filter_by(email = form.email.data).first()
        if doc and bcrypt.check_password_hash(doc.password,form.password.data):
            return redirect(url_for('drdetails'))
        else:
            flash('Login Unsuccessful Check username and passsword','danger')    
    return render_template('dlogin.html',form=form)

@app.route("/emrp", methods = ['GET','POST'])
def emrp():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('emrp'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('emrp.html', image_file = image_file, form=form)
 
@app.route("/after_login")
def after_login():
    doc = Doctor.query.all()
    return render_template('After_login.html', doct = doc)

@app.route("/EMRD", methods = ['GET','POST'])
def EMRD():
    form = DUpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('EMRD'))
    if request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('EMRD.html', image_file = image_file, form=form)



