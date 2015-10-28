Campus Study Queries

 Create profile
Insert into User (email, password, name, major, faculty, profilePic, bio) Values(email, pass, name, major, faculty, picture, bio)

Edit profile
Update User set email=Email, password=pass, name=name, major=major, faculty=faculty, profilePicture=picture, bio=bio

View colleagues
Select * From User where ID in (Select colleaguesID From Colleagues where userID=user)

Attending to meeting
Select * From User where ID in (Select userID From Attending where meetingID=meeting)

Belongs to group
Select * From User where ID in (Select userID From Belongs where groupID=group)

Post in group
Insert into Post values((Select (CASE when (Select Max(ID) From Post) is NULL then -1 ELSE (Select Max(ID) From Post) END) from dual), user, text, doc, subject, image, date, time)

Insert into GroupPost values(postID, groupID)

Insert into Notification values((Select (CASE when (Select Max(ID) From Notifications) is NULL then -1 ELSE (Select Max(ID) From Notifications) END) from dual), user, message)

Insert into Creates values(postID, notificationID)

** Insert into HasNotification(notificationID, (Select ID From User where ID in (Select userID From Belongs where groupID=group)))



Post in Meeting
Insert into Post values((Select (CASE when (Select Max(ID) From Post) is NULL then -1 ELSE (Select Max(ID) From Post) END) from dual), user, text, doc, subject, image, date, time)

Insert into MeetingPost values(postID, meetingID)

Insert into Notification values((Select (CASE when (Select Max(ID) From Notifications) is NULL then -1 ELSE (Select Max(ID) From Notifications) END) from dual), user, message)

Insert into Creates values(postID, notificationID)

** Insert into HasNotification(notificationID, (Select ID From User where ID in (Select userID From Attending where meetingID=meeting)))

Feeds
Select * From Post where ID in (Select PostID From Colleagues natural join ColleaguesPost 
where userID=user)

Create group
Insert into Groups (tutorID, name, purpose, faculty) values(userID, name, purpose, faculty)

Create Meeting
Insert into Meeting (name, location, time, date, purpose, faculty) values(name, loc, time, date, purpose, faculty)

Add user to group
Insert into Belongs values(userId, groupID)

Add user to meeting
Insert into Attending values(userID, meetingID)

Leave group
Delete from Belongs where userID=user and groupID=group

Leave meeting
Delete from Attending where userID=user and meetingID=meeting


Add colleagues
Insert into colleagues values(userID, colleaguesID)

View Notifications
Select userID, message From Notifications where ID in (Select notificationID From HasNotifications where userID=user)

Delete colleagues
Delete From Colleagues where userID=user and colleagueID=colleague

Delete notifications
Delete From HasNotification where userID=user and notificationID=notification

Validate user
Select ID From User where email=email and password=pass
