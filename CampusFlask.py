from flask import Flask, render_template, request, flash, redirect, jsonify, session, url_for, send_from_directory
import flask_sqlalchemy, logging, sys, sqlalchemy, collections
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_mail import Mail, Message
import random, string
import queries
from werkzeug.utils import secure_filename
import os
import re


UPLOAD_FOLDER = '/home/CampusStudy/CampusStudy/uploads'
PICTURE_ALLOWED_EXTENSIONS = set(['png','PNG', 'jpg','JPG', 'jpeg','JPEG', 'gif', 'GIF'])
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://CampusStudy:12345@mysql.server/CampusStudy$campus'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = flask_sqlalchemy.SQLAlchemy(app)
db.engine.connect()
app.secret_key = 'super secret key'
app.config.update(DEBUG=True,MAIL_SERVER='smtp.gmail.com',MAIL_PORT=465,MAIL_USE_SSL=True,MAIL_USERNAME = 'campusstudydb@gmail.com',MAIL_PASSWORD = 'DBDream3')
mail=Mail(app)

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/Search')
def search():
    return app.send_static_file('Search.html')

@app.route('/Notification')
def notification():
    return app.send_static_file('Notifications.html')

@app.route('/PostInGroup')
def postInGroup():
    return app.send_static_file('PostGroup.html')

@app.route('/PostInEvent')
def postInEvent():
    return app.send_static_file('PostEvent.html')

@app.route('/myGroups')
def myGroups():
    return app.send_static_file('Groups.html')

@app.route('/myEvents')
def myEvents():
    return app.send_static_file('Events.html')

@app.route('/Groups')
def viewGroups():
    return app.send_static_file('GroupLayout.html')

@app.route('/Group/<int:group_id>')
def group_id(group_id):
    session['groupID'] = str(group_id)
    return redirect('/Groups')

@app.route('/CreateGroupEvent')
def createGroupEvent():
    session['create_group_event'] = True;
    return redirect('/NewEvent')

@app.route('/Events')
def viewEvents():
    return app.send_static_file('EventLayout.html')

@app.route('/Event/<int:event_id>')
def event_id(event_id):
    session['eventID'] = str(event_id)
    return redirect('/Events')

@app.route('/Post')
def viewPost():
    return app.send_static_file('PostView.html')

@app.route('/Post/<int:post_id>')
def post_id(post_id):
    session['postID'] = str(post_id)
    return redirect('/Post')

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
    if str(user_id) == str(session['current_user']):
        return redirect('/Profile')

    session['colleagueID'] = str(user_id)
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
    picture = None

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename2 = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            picture = url_for('uploaded_file',filename=filename2)

        elif not file:
            picture = "http://i.imgur.com/FzaFFbX.png"

        else:
            return "Extension not allowed"

    s=string.lowercase+string.digits
    r = random.sample(s,10)
    msg = Message('Campus Study Team',sender='campusstudydb@gmail.com',recipients=[request.form['inputEmail']])
    msg.body = "This email was sent from the Campus Study Webpage: your confirmation code is "+''.join(r)
    mail.send(msg)

    codeQuery = queries.INSERT_CODE.format(email,''.join(r))
    db.engine.execute(codeQuery)

    query = queries.NEW_USER.format(email,password,name,major,faculty,picture,bio)
    db.engine.execute(query)

    IDQuery = queries.USER_ID.format(email,password)
    IDresult = db.engine.execute(IDQuery)
    ID = ""
    for row in IDresult:
        ID = row[0]

    selfFollowerQuery = queries.FOLLOW.format(str(ID),str(ID))
    db.engine.execute(selfFollowerQuery)

    return redirect('/')


@app.route('/SignIn',methods=['GET','POST'])
def signIn():
    password = request.form['inputPassword']
    email = request.form['inputEmail']

    query = queries.USER_ID.format(email,password)
    result = db.engine.execute(query)

    for row in result:
        session['current_user'] = str(row[0])

    session['create_group_event'] = False;
    session['searchQuery'] = queries.EMPTY_SET
    return app.send_static_file('MainLayout.html')

@app.route('/logout')
def logout_page():

    session['current_user'] = None
    return redirect("/")


@app.route('/mail',methods=['POST'])
def index():
    s=string.lowercase+string.digits
    r = random.sample(s,10)
    msg = Message('Campus Study Team',sender='campusstudydb@gmail.com',recipients=[request.form['exampleInputEmail1']])
    msg.body = "This email was sent from the Campus Study Webpage: your reset code is "+''.join(r)
    mail.send(msg)
    return app.send_static_file('index.html')


@app.route('/CreateGroup',methods=['GET','POST'])
def createGroup():

    name = request.form['inputName']
    faculty = request.form['inputFaculty']
    purpose = request.form['inputPurpose']
    picture = None

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename2 = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            picture = url_for('uploaded_file',filename=filename2)

        elif not file:
            picture = "http://i.imgur.com/FzaFFbX.png"

        else:
            return "Extension not allowed"

    #Get group ID
    group_ID_result = db.engine.execute(queries.GROUP_ID)
    groupID = None
    for row in group_ID_result:
        groupID = row[0]

    query = queries.NEW_GROUP.format(str(session['current_user']),name, purpose, faculty, picture, groupID)
    db.engine.execute(query)
    session['groupID'] = groupID

    belongsQry = queries.INSERT_BELONGS.format(str(session['current_user']),str(groupID))
    db.engine.execute(belongsQry)

    #Add colleagues to group
    colleaguesQuery = queries.COLLEAGUES.format(str(session['current_user']))
    colleagues = db.engine.execute(colleaguesQuery)

    colleaguesList = []
    for colleague in colleagues:
        colleaguesList.append(colleague[0])

    colleagueBelongs = None
    for colleagueID in colleaguesList:
        colleagueBelongs = queries.INSERT_BELONGS.format(colleagueID,str(groupID))
        db.engine.execute(colleagueBelongs)

    return redirect('/Groups')

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
    picture = None

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename2 = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            picture = url_for('uploaded_file',filename=filename2)

        elif not file:
            picture = "http://i.imgur.com/FzaFFbX.png"

        else:
            return "Extension not allowed"

    #Get event ID
    event_ID_result = db.engine.execute(queries.EVENT_ID)
    eventID = None
    for row in event_ID_result:
        eventID = row[0]

    date = month+"/"+day+"/"+year

    query = queries.NEW_EVENT.format(name, location, time, date, purpose, faculty, picture, str(session['current_user']),eventID)
    db.engine.execute(query)

    session['eventID'] = eventID
    attendingQry = queries.INSERT_ATTENDING.format(str(session['current_user']),str(eventID))
    db.engine.execute(attendingQry)

    #Add all colleagues to group event
    if session['create_group_event']:
        belongsQuery = queries.USER_BELONGS.format(str(session['groupID']))
        belongs = db.engine.execute(belongsQuery)

        collaguesIDList = []
        for colleague in belongs:
            collaguesIDList.append(colleague[0])

        attendingCollaguesQry = None
        for collaguesID in collaguesIDList:
            attendingCollaguesQry = queries.INSERT_ATTENDING.format(collaguesID,str(eventID))
            db.engine.execute(attendingCollaguesQry)

        groupEventQuery = queries.INSERT_GROUP_MEETING.format(str(session['groupID']),str(session['eventID']))
        db.engine.execute(groupEventQuery)

    session['create_group_event'] = False

    #Add colleagues to event
    colleaguesQuery = queries.COLLEAGUES.format(str(session['current_user']))
    colleagues = db.engine.execute(colleaguesQuery)

    colleaguesList = []
    for colleague in colleagues:
        colleaguesList.append(colleague[0])

    colleagueAttending = None
    for colleagueID in colleaguesList:
        colleagueAttending = queries.INSERT_ATTENDING.format(colleagueID,str(eventID))
        db.engine.execute(colleagueAttending)

    return redirect('/Events')


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
    picture = None

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename2 = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            picture = url_for('uploaded_file',filename=filename2)

        elif not file:
            picQuery = queries.PROFILE_PIC.format(str(session['current_user']))
            picResult = db.engine.execute(picQuery)
            for row in picResult:
                picture = row[0]
        else:
            return "Extension not allowed"

    passQuery = queries.USER.format(str(session['current_user']))
    currentPasword = db.engine.execute(passQuery)

    for row in currentPasword:
        if str(row[2]) != currentPass:
            return "Current Password is incorrect."

    if password != verPassword:
        return "Verify passwords fields."

    query = queries.EDIT_PROFILE.format(email,name,major,"Engineering",password,bio,str(session['current_user']),picture, str(session['current_user']))
    db.engine.execute(query)

    return redirect('/Profile')

@app.route('/uploadedFiles/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

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


@app.route('/userEvents',methods=['GET','POST'])
def userEvents():

    query = queries.USER_EVENTS.format(str(session['current_user']))
    users = db.engine.execute(query)
    eventData = {"userEvents":[]}
    for row in users:
        test = {}
        test["name"] = row['name']
        test["location"] = row['location']
        test["ID"] = row['ID']
        test["time"] = row['time']
        test["date"] = row['date']
        test["purpose"] = row['purpose']
        test["faculty"] = row['faculty']
        test["picture"] = row['picture']
        test["admin"] = row['admin']
        eventData["userEvents"].append(test)
    return jsonify(eventData)

@app.route('/groupEvents',methods=['GET','POST'])
def groupEvents():

    query = queries.GROUP_EVENT.format(str(session['groupID']))
    users = db.engine.execute(query)
    eventData = {"groupEventsInfo":[]}
    for row in users:
        test = {}
        test["name"] = row['name']
        test["location"] = row['location']
        test["ID"] = row['ID']
        test["time"] = row['time']
        test["date"] = row['date']
        test["purpose"] = row['purpose']
        test["faculty"] = row['faculty']
        test["picture"] = row['picture']
        test["admin"] = row['admin']
        eventData["groupEventsInfo"].append(test)
    return jsonify(eventData)

@app.route('/userGroups',methods=['GET','POST'])
def userGroups():

    query = queries.USER_GROUPS.format(str(session['current_user']))
    users = db.engine.execute(query)
    GroupsData = {"userGroups":[]}
    for dat in users:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        #jsonf["tutorID"] = dat['tutorID']
        jsonf["name"] = dat['name']
        #jsonf["purpose"] = dat['purpose']
        jsonf["faculty"] = dat['faculty']
        #jsonf["picture"] = dat['picture']
        GroupsData["userGroups"].append(jsonf)
    return jsonify(GroupsData)

@app.route('/eventsInfo',methods=['GET','POST'])
def eventsInfo():
    query = queries.EVENT.format(str(session['eventID']))
    users = db.engine.execute(query)
    eventData = {"eventsInfo":[]}

    for row in users:
        test = {}
        test["name"] = row['name']
        test["location"] = row['location']
        test["ID"] = row['ID']
        test["time"] = row['time']
        test["date"] = row['date']
        test["purpose"] = row['purpose']
        test["faculty"] = row['faculty']
        test["picture"] = row['picture']
        test["admin"] = row['admin']
        eventData["eventsInfo"].append(test)

    return jsonify(eventData)

@app.route('/groupsInfo',methods=['GET','POST'])
def groupsInfo():

    query = queries.GROUP.format(str(session['groupID']))
    users = db.engine.execute(query)
    GroupsData = {"groupsInfo":[]}
    for dat in users:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["tutorID"] = dat['tutorID']
        jsonf["name"] = dat['name']
        jsonf["purpose"] = dat['purpose']
        jsonf["faculty"] = dat['faculty']
        jsonf["picture"] = dat['picture']
        GroupsData["groupsInfo"].append(jsonf)
    return jsonify(GroupsData)

@app.route('/eventAdmin',methods=['GET','POST'])
def eventAdmin():

    adminQuery = queries.EVENT.format(str(session['eventID']))
    admin = db.engine.execute(adminQuery)
    userID = None

    for row in admin:
        userID = row['admin']

    query = queries.USER.format(str(userID))
    user = db.engine.execute(query)
    eventData = {"eventAdminInfo":[]}
    for dat in user:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["profilePic"]=dat['profilePic']
        jsonf["name"] = dat['name']
        eventData["eventAdminInfo"].append(jsonf)
    return jsonify(eventData)

@app.route('/attendingUsers',methods=['GET','POST'])
def attendingUsers():
    query = queries.USER_ATTENDING.format(str(session['eventID']))
    users = db.engine.execute(query)
    eventData = {"attendingUsers":[]}

    for row in users:
        test = {}
        test["name"] = row['name']
        test["ID"] = row['ID']
        eventData["attendingUsers"].append(test)

    return jsonify(eventData)

@app.route('/groupMembers',methods=['GET','POST'])
def groupMembers():
    query = queries.USER_BELONGS.format(str(session['groupID']))
    users = db.engine.execute(query)
    eventData = {"groupMembers":[]}

    for row in users:
        test = {}
        test["name"] = row['name']
        test["ID"] = row['ID']
        eventData["groupMembers"].append(test)
    return jsonify(eventData)

@app.route('/groupTutor',methods=['GET','POST'])
def groupTutor():

    adminQuery = queries.GROUP.format(str(session['groupID']))
    admin = db.engine.execute(adminQuery)
    userID = None

    for row in admin:
        userID = row['tutorID']

    query = queries.USER.format(str(userID))
    user = db.engine.execute(query)
    eventData = {"groupTutorInfo":[]}
    for dat in user:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["profilePic"]=dat['profilePic']
        jsonf["name"] = dat['name']
        eventData["groupTutorInfo"].append(jsonf)
    return jsonify(eventData)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in PICTURE_ALLOWED_EXTENSIONS

@app.route('/GroupPost',methods=['GET','POST'])
def groupPost():

    subject = request.form['inputSubject']
    text = request.form['inputText']
    document = None

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename2 = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            document = url_for('uploaded_file',filename=filename2)

        elif not file:
            document = " "

        else:
            return "Extension not allowed"

    #Get post ID
    post_ID_result = db.engine.execute(queries.POST_ID)
    postID = None
    for row in post_ID_result:
        postID = row[0]

    #Insert values to Post table
    postQuery = queries.POST.format(str(postID), str(session['current_user']), text, document, subject)
    db.engine.execute(postQuery)

    #Insert values to GroupPost table
    groupPostQry = queries.GROUP_POST.format(str(postID), str(session['groupID']))
    db.engine.execute(groupPostQry)

    #Get notification ID
    notification_ID_result = db.engine.execute(queries.NOTIFICATION_ID)
    notificationID = None
    for row in notification_ID_result:
        notificationID = row[0]

    #Insert values to notification table
    notificationQuery = queries.NOTIFICATION.format(str(notificationID), session['current_user'], "New post from group:")
    db.engine.execute(notificationQuery)

    #Insert values to creates table
    createsQry = queries.CREATES.format(str(postID), str(notificationID))
    db.engine.execute(createsQry)

    #Get users form group
    userBelongsQry = queries.USER_BELONGS.format(str(session['groupID']))
    userBelongs = db.engine.execute(userBelongsQry)

    #Send notification to each user from group
    hasNotificationQueries = []
    hasNotificationQry = None

    for row in userBelongs:
        hasNotificationQry = queries.HAS_NOTIFICATION.format(str(notificationID), str(row[0]))
        hasNotificationQueries.append(hasNotificationQry)

    for insertQry in hasNotificationQueries:
        db.engine.execute(insertQry)

    return redirect('/Groups')

@app.route('/EventPost',methods=['GET','POST'])
def eventPost():

    subject = request.form['inputSubject']
    text = request.form['inputText']
    document = None

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename2 = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            document = url_for('uploaded_file',filename=filename2)

        elif not file:
            document = " "

        else:
            return "Extension not allowed"

    #Get post ID
    post_ID_result = db.engine.execute(queries.POST_ID)
    postID = None
    for row in post_ID_result:
        postID = row[0]

    #Insert values to Post table
    postQuery = queries.POST.format(str(postID), str(session['current_user']), text, document, subject)
    db.engine.execute(postQuery)

    #Insert values to GroupPost table
    groupPostQry = queries.MEETING_POST.format(str(postID), str(session['eventID']))
    db.engine.execute(groupPostQry)

    #Get notification ID
    notification_ID_result = db.engine.execute(queries.NOTIFICATION_ID)
    notificationID = None
    for row in notification_ID_result:
        notificationID = row[0]

    #Insert values to notification table
    notificationQuery = queries.NOTIFICATION.format(str(notificationID), session['current_user'], "New post from event:")
    db.engine.execute(notificationQuery)

    #Insert values to creates table
    createsQry = queries.CREATES.format(str(postID), str(notificationID))
    db.engine.execute(createsQry)

    #Get users form group
    userAttendingQry = queries.USER_ATTENDING.format(str(session['eventID']))
    userAttending = db.engine.execute(userAttendingQry)

    #Send notification to each user from event
    hasNotificationQueries = []
    hasNotificationQry = None

    for row in userAttending:
        hasNotificationQry = queries.HAS_NOTIFICATION.format(str(notificationID), str(row[0]))
        hasNotificationQueries.append(hasNotificationQry)

    for insertQry in hasNotificationQueries:
        db.engine.execute(insertQry)

    return redirect('/Events')

@app.route('/MainPost',methods=['GET','POST'])
def mainPost():

    subject = request.form['inputSubject']
    text = request.form['inputText']
    document = None

    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):

            filename2 = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            document = url_for('uploaded_file',filename=filename2)

        elif not file:
            document = " "

        else:
            return "Extension not allowed"

    #Get post ID
    post_ID_result = db.engine.execute(queries.POST_ID)
    postID = None
    for row in post_ID_result:
        postID = row[0]

    #Insert values to Post table
    postQuery = queries.POST.format(str(postID), str(session['current_user']), text, document, subject)
    db.engine.execute(postQuery)

    #Insert values to ColleaguesPost table
    groupPostQry = queries.COLLEAGUES_POST.format(str(postID), str(session['current_user']))
    db.engine.execute(groupPostQry)


    #Get notification ID
    notification_ID_result = db.engine.execute(queries.NOTIFICATION_ID)
    notificationID = None
    for row in notification_ID_result:
        notificationID = row[0]

    #Insert values to notification table
    notificationQuery = queries.NOTIFICATION.format(str(notificationID), session['current_user'], "New post from colleague:")
    db.engine.execute(notificationQuery)

    #Insert values to creates table
    createsQry = queries.CREATES.format(str(postID), str(notificationID))
    db.engine.execute(createsQry)

    #Get followers
    followersQry = queries.FOLLOWERS.format(str(session['current_user']))
    followers = db.engine.execute(followersQry)

    #Send notification to each user from event
    hasNotificationQueries = []
    hasNotificationQry = None

    for row in followers:
        hasNotificationQry = queries.HAS_NOTIFICATION.format(str(notificationID), str(row[0]))
        hasNotificationQueries.append(hasNotificationQry)

    for insertQry in hasNotificationQueries:
        db.engine.execute(insertQry)

    return redirect('/Home')

@app.route('/GroupFeeds',methods=['GET','POST'])
def groupFeeds():

    feedQuery = queries.GROUP_FEEDS.format(str(session['groupID']))
    feeds = db.engine.execute(feedQuery)

    feedData = {"groupFeeds":[]}
    for dat in feeds:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["userID"]=dat['userID']
        jsonf["text"] = dat['text']
        jsonf["subject"] = dat['subject']
        jsonf["date"] = dat['date']
        jsonf["name"] = dat['name']
        feedData["groupFeeds"].append(jsonf)
    return jsonify(feedData)

@app.route('/EventFeeds',methods=['GET','POST'])
def eventFeeds():

    feedQuery = queries.EVENT_FEEDS.format(str(session['eventID']))
    feeds = db.engine.execute(feedQuery)

    feedData = {"eventFeeds":[]}
    for dat in feeds:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["userID"]=dat['userID']
        jsonf["text"] = dat['text']
        jsonf["subject"] = dat['subject']
        jsonf["date"] = dat['date']
        jsonf["name"] = dat['name']
        feedData["eventFeeds"].append(jsonf)
    return jsonify(feedData)

@app.route('/HomeFeeds',methods=['GET','POST'])
def homeFeeds():

    feedQuery = queries.FEED_MAIN.format(str(session['current_user']))
    feeds = db.engine.execute(feedQuery)

    feedData = {"homeFeeds":[]}
    for dat in feeds:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["postID"]=dat['postID']
        jsonf["picture"] = dat['picture']
        jsonf["subject"] = dat['subject']
        jsonf["type"] = dat['type']
        jsonf["username"] = dat['username']
        jsonf["uID"] = dat['uID']

        feedData["homeFeeds"].append(jsonf)
    return jsonify(feedData)

@app.route('/notificationsData',methods=['GET','POST'])
def notificationInfo():

    notificationQuery = queries.FEED_NOTIFICATION.format(str(session['current_user']))
    notifications = db.engine.execute(notificationQuery)

    notificationData = {"notificationInfo":[]}
    for dat in notifications:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["name"] = dat['name']
        jsonf["picture"] = dat['picture']
        jsonf["postID"] = dat['postID']
        jsonf["subject"] = dat['subject']
        jsonf["type"]=dat['type']
        jsonf["message"] = dat['message']
        notificationData["notificationInfo"].append(jsonf)
    return jsonify(notificationData)

@app.route('/postData',methods=['GET','POST'])
def postData():

    postQuery = queries.POST_INFO.format(str(session['postID']))
    post = db.engine.execute(postQuery)

    postData = {"postInfo":[]}
    for dat in post:
        jsonf = {}
        jsonf["ID"] = dat['ID']
        jsonf["userID"] = dat['userID']
        jsonf["text"] = dat['text']
        jsonf["document"] = dat['document']
        jsonf["date"] = dat['date']
        jsonf["time"]=dat['time']
        jsonf["subject"] = dat['subject']
        jsonf["username"] = dat['username']
        postData["postInfo"].append(jsonf)
    return jsonify(postData)

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

@app.route('/SearchQuery',methods=['GET','POST'])
def searchQuery():
    search = request.form['inputSearch']
    category = request.form.get('checkC')
    event = request.form.get('checkE')
    user = request.form.get('checkU')
    group = request.form.get('checkG')

    query = ""
    if category != None:
        query += facultySearch(search) + " UNION "

    if user != None:
        query += userSearch(search) + " UNION "

    if event != None:
        query += eventSearch(search) + " UNION "

    if group != None:
        query += groupSearch(search) + " UNION "

    if not query:
        session['searchQuery'] = queries.EMPTY_SET

    else:
        session['searchQuery'] = query[0:len(query)-6]

    return redirect('/Search')

@app.route('/SearchData',methods=['GET','POST'])
def searchData():
    result = db.engine.execute(session['searchQuery'])
    searchData = {"searchInfo":[]}

    for row in result:
        data = {}
        data["name"] = row['name']
        data["ID"] = row['ID']
        data["picture"] = row['picture']
        data["type"] = row['type']
        searchData["searchInfo"].append(data)

    session['searchQuery'] = queries.EMPTY_SET
    return jsonify(searchData)

def userSearch(stringInput):

    src = re.sub("[^\w]", " ",  stringInput).split()
    result = []
    for s in src:
        result.append("%%"+s+"%%")
    #like with each word
    like = []
    for e in result:
        if len(like)==0:
            like.append("name like " +'"%s"'%e)
        else:
            like.append(" or name like " +'"%s"'%e)
    #query with 'like'
    query = "SELECT ID, name, 'User' as type, profilePic as picture FROM User WHERE "
    for l in like:
        query += l
    return query

def groupSearch(stringInput):

    src = re.sub("[^\w]", " ",  stringInput).split()
    result = []
    for s in src:
        result.append("%%"+s+"%%")
    #like with each word
    like2 = []
    for e in result:
        if len(like2)==0:
            like2.append("name like " +'"%s"'%e +" or purpose like"+'"%s"'%e)
        else:
            like2.append(" or name like " +'"%s"'%e +" or purpose like"+'"%s"'%e)
    query2 = "SELECT ID, name, 'Group' as type, picture FROM Groups WHERE "
    for l in like2:
        query2 += l

    return query2

def eventSearch(stringInput):
    src = re.sub("[^\w]", " ",  stringInput).split()
    result = []
    for s in src:
        result.append("%%"+s+"%%")
    #like with each word
    like3 = []
    for e in result:
        if len(like3)==0:
            like3.append("name like " +'"%s"'%e +" or purpose like"+'"%s"'%e)
        else:
            like3.append(" or name like " +'"%s"'%e +" or purpose like"+'"%s"'%e)
    query3 = "SELECT ID, name, 'Event' as type, picture FROM Meeting WHERE "
    for l in like3:
        query3 += l
    return query3

def facultySearch(stringInput):
    src = re.sub("[^\w]", " ",  stringInput).split()
    result = []
    for s in src:
        result.append("%%"+s+"%%")
    like = []
    for e in result:
        if len(like)==0:
            like.append("faculty like " +'"%s"'%e)
        else:
            like.append(" or faculty like " +'"%s"'%e)
    query = "SELECT ID, name, 'User' as type, profilePic as picture FROM User WHERE "
    query2 = "SELECT ID, name, 'Group' as type, picture FROM Groups WHERE "
    query3 = "SELECT ID, name, 'Event' as type, picture FROM Meeting WHERE "

    for l in like:
        query += l
        query2 += l
        query3 += l

    fullQuery = query +" UNION "+query2 +" UNION "+ query3

    return fullQuery


