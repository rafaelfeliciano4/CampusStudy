from flask import Flask, render_template, request, flash, redirect, jsonify, session
import flask_sqlalchemy, logging, sys, sqlalchemy, collections
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_mail import Mail, Message
import random, string
import queries

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://CampusStudy:12345@mysql.server/CampusStudy$campus'
db = flask_sqlalchemy.SQLAlchemy(app)
db.engine.connect()
app.secret_key = 'super secret key'

@app.route('/')
def main():
    return app.send_static_file('index.html')


@app.route('/Groups')
def viewGroups():
    return app.send_static_file('Groups.html')

@app.route('/Events')
def viewEvents():
    return app.send_static_file('Events.html')

@app.route('/Profile')
def viewProfile():
    return app.send_static_file('Profile.html')

@app.route('/Home')
def home():
    return app.send_static_file('MainLayout.html')

@app.route('/User')
def User():
    return app.send_static_file('UserProfile.html')

@app.route('/User/<int:user_id>')
def user_id(user_id):
    session['colleagueID'] = str(user_id)
    #return app.send_static_file('UserProfile.html')
    return redirect('/User')

@app.route('/NewGroup')
def newGroup():
    return app.send_static_file('CreateGroupLayout.html')

@app.route('/NewEvent')
def newEvent():
    return app.send_static_file('CreateEventLayout.html')

@app.route('/CreateProfile')
def showSignUp():
    return app.send_static_file('CreateProfile.html')

@app.route('/editProfile')
def editProfile():
    return app.send_static_file('EditProfile.html')


@app.route('/SignUp',methods=['POST'])
def userSignUp():


    name = request.form['inputName']
    password = request.form['inputPassword']
    verPassword = request.form['inputVerPassword']
    major = request.form['inputMajor']
    faculty = request.form['inputFaculty']
    email = request.form['inputEmail']
    bio = request.form['inputBio']

    query = queries.NEW_USER.format(email,password,name,major,faculty,":)",bio)

    db.engine.execute(query)

    return app.send_static_file('index.html')

@app.route('/SignIn',methods=['GET','POST'])
def signIn():
    password = request.form['inputPassword']
    email = request.form['inputEmail']

    query = queries.USER_ID.format(email,password)
    result = db.engine.execute(query)

    for row in result:
        session['current_user'] = str(row[0])
    #user = User(email,password)
    #login_user(user)

    return app.send_static_file('MainLayout.html')

@app.route('/logout')
def logout_page():

    session['current_user'] = None
    return redirect("/")



app.config.update(DEBUG=True,MAIL_SERVER='smtp.gmail.com',MAIL_PORT=465,MAIL_USE_SSL=True,MAIL_USERNAME = 'campusstudydb@gmail.com',MAIL_PASSWORD = 'DBDream3')
mail=Mail(app)
@app.route('/mail',methods=['POST'])
def index():
    s=string.lowercase+string.digits

    msg = Message('Campus Study Team',sender='campusstudydb@gmail.com',recipients=[request.form['exampleInputEmail1']])
    msg.body = "This email was sent from the Campus Study Webpage: you reset code is "+''.join(random.sample(s,10))
    mail.send(msg)
    return app.send_static_file('index.html')


@app.route('/CreateGroup',methods=['GET','POST'])
def createGroup():

    name = request.form['inputName']
    faculty = request.form['inputFaculty']
    purpose = request.form['inputPurpose']

    query = queries.NEW_GROUP.format(str(session['current_user']),name, purpose, faculty, ":O")

    db.engine.execute(query)

    return app.send_static_file('GroupLayout.html')

@app.route('/CreateEvent',methods=['GET','POST'])
def createEvent():

    name = request.form['inputName']
    faculty = request.form['inputFaculty']
    purpose = request.form['inputPurpose']
    location = request.form['inputLocation']
    month = request.form['inputMonth']
    day = request.form['inputDay']
    year = request.form['inputYear']
    time = request.form['inputTime']

    query = queries.NEW_EVENT.format(name,location,"CURTIME()","CURDATE()", purpose, faculty)

    db.engine.execute(query)

    return app.send_static_file('EventLayout.html')


@app.route('/updateUser',methods=['GET','POST'])
def updateUser():

    name = request.form['inputName']
    #faculty = request.form['inputFaculty']
    major = request.form['inputMajor']
    currentPass = request.form['inputCurPassword']
    password = request.form['inputPassword']
    verPassword = request.form['inputVerPassword']
    bio = request.form['inputBio']
    email = request.form['inputEmail']


    passQuery = queries.USER.format(str(session['current_user']))
    currentPasword = db.engine.execute(passQuery)

    for row in currentPasword:
        if str(row[2]) != currentPass:
            return "Current Password is incorrect."

    if password != verPassword:
        return "Verify passwords fields."

    query = queries.EDIT_PROFILE.format(email,name,major,"Engineering",password,bio,str(session['current_user']))
    db.engine.execute(query)


    return redirect('/Profile')


@app.route('/profileUserInfo',methods=['GET','POST'])
def userProfile():
    query = queries.USER.format(str(session['colleagueID']))
    querys = db.engine.execute(query)

    profileData = {"userInfo":[]}
    for usr in querys:
        user = {}
        user["name"] = usr['name']
        user["password"] = usr['password']
        user["email"] = usr['email']
        user["major"] = usr['major']
        user["faculty"] = usr['faculty']
        user["bio"] = usr['bio']
        user["ID"] = usr['ID']
        user["confirmed"]=usr['confirmed']
        user["profilePic"]=usr['profilePic']
        profileData["userInfo"].append(user)
    return jsonify(profileData)

@app.route('/profilesInfo',methods=['GET','POST'])
def profilesInfo():
    query = queries.USER.format(str(session['current_user']))

    users = db.engine.execute(query)
    profileData = {"userInfo":[]}
    for usr in users:
        user = {}
        user["name"] = usr['name']
        user["password"] = usr['password']
        user["email"] = usr['email']
        user["major"] = usr['major']
        user["faculty"] = usr['faculty']
        user["bio"] = usr['bio']
        user["ID"] = usr['ID']
        user["confirmed"]=usr['confirmed']
        user["profilePic"]=usr['profilePic']
        profileData["userInfo"].append(user)
    return jsonify(profileData)

@app.route('/Colleagues',methods=['GET','POST'])
def ColleaguesInfo():
    query = queries.COLLEAGUES.format(str(session['current_user']))
    users = db.engine.execute(query)

    colleagueData = {"colleagueInfo":[]}
    for row in users:
        test = {}
        test["name"] = row['name']
        test["password"] = row['password']
        test["email"] = row['email']
        test["major"] = row['major']
        test["faculty"] = row['faculty']
        test["bio"] = row['bio']
        test["ID"] = row['ID']
        test["confirmed"]=row['confirmed']
        test["profilePic"]=row['profilePic']
        colleagueData["colleagueInfo"].append(test)
    return jsonify(colleagueData)

@app.route('/cColleagues',methods=['GET','POST'])
def userColleaguesInfo():
    query = queries.COLLEAGUES.format(str(session['colleagueID']))
    users = db.engine.execute(query)

    cColleagueData = {"cColleaguesInfo":[]}
    for row in users:
        test = {}
        test["name"] = row['name']
        test["password"] = row['password']
        test["email"] = row['email']
        test["major"] = row['major']
        test["faculty"] = row['faculty']
        test["bio"] = row['bio']
        test["ID"] = row['ID']
        test["confirmed"]=row['confirmed']
        test["profilePic"]=row['profilePic']
        cColleagueData["cColleaguesInfo"].append(test)
    return jsonify(cColleagueData)


@app.route('/eventsInfo',methods=['GET','POST'])
def eventsInfo():

    query = queries.USER_EVENTS.format(str(session['current_user']))

    users = db.engine.execute(query)

    eventData = {"eventsInfo":[]}
    for row in users:
        test = {}
        test["name"] = row['name']
        test["location"] = row['location']

        eventData["eventsInfo"].append(test)
    return jsonify(eventData)

@app.route('/groupsInfo',methods=['GET','POST'])
def groupsInfo():
    query = queries.USER_GROUPS.format(str(session['current_user']))

    users = db.engine.execute(query)
    GroupsData = {"groupsInfo":[]}
    for dat in users:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["tutorID"] = dat['tutorID']
        jsonf["name"] = dat['name']
        jsonf["purpose"] = dat['purpose']
        jsonf["faculty"] = dat['faculty']
        #jsonf["picture"] = dat['picture']
        GroupsData["groupsInfo"].append(jsonf)
    return jsonify(GroupsData)

@app.route('/Follow',methods=['GET','POST'])
def follow():
    query = queries.FOLLOW.format(str(session['current_user']),str(session['colleagueID']))
    db.engine.execute(query)

    return redirect('/Profile')

@app.route('/unFollow',methods=['GET','POST'])
def unFollow():
    query = queries.UNFOLLOW.format(str(session['current_user']),str(session['colleagueID']))
    db.engine.execute(query)

    return redirect('/Profile')



