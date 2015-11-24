
NEW_USER="insert into User (email,password,name,major,faculty,profilePic,bio) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')"
NEW_GROUP="insert into Groups (ID,tutorID,name,purpose,faculty,picture) VALUES('{5}','{0}','{1}','{2}','{3}','{4}')"
NEW_EVENT="insert into Meeting (ID,name,location,time,date,purpose,faculty,picture,admin) VALUES('{8}','{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')"
USER_ID="select ID from User WHERE email='{0}' and password='{1}'"
USER_OBJ="select email, password from User WHERE ID='{0}'"
USER="SELECT * FROM User WHERE ID='{0}'"
EDIT_PROFILE="Update User SET email='{0}',name='{1}',major='{2}',faculty='{3}',password='{4}',bio='{5}',profilePic='{7}' WHERE ID='{6}'"
USER_ATTENDING="SELECT * FROM User WHERE ID in (SELECT userID FROM Attending WHERE meetingID='{0}')"
USER_BELONGS="SELECT * FROM User WHERE ID in (SELECT userID FROM Belongs WHERE groupID='{0}')"
EVENT="SELECT * FROM Meeting WHERE ID='{0}'"
GROUP="SELECT * FROM Groups WHERE ID='{0}'"
COLLEAGUES="SELECT * FROM User WHERE ID in (SELECT colleagueID FROM Colleagues WHERE userID='{0}' and colleagueID != userID)"
FOLLOWERS = "SELECT * FROM User WHERE ID in (SELECT userID FROM Colleagues WHERE colleagueID='{0}')"
FOLLOW="INSERT INTO Colleagues VALUES ('{0}','{1}')"
UNFOLLOW="DELETE FROM Colleagues WHERE userID='{0}' and colleagueID='{1}'"
USER_EVENTS="SELECT * FROM Meeting WHERE ID in (SELECT meetingID FROM Attending WHERE userID='{0}')"
USER_GROUPS="SELECT * FROM Groups WHERE ID in (SELECT groupID from Belongs WHERE userID='{0}')"
PROFILE_PIC = "SELECT profilePic FROM User WHERE ID='{0}'"
USER_NAME_PIC="SELECT name, profilePic FROM User WHERE ID='{0}'"
USER_NOTIFICATIONS="SELECT * FROM Notifications where ID in (SELECT notificationID From HasNotification WHERE userID='{0}')"
POST_INFO = "SELECT p.ID as ID, p.userID as userID, p.text as text, p.document as document, p.subject as subject, p.date as date, p.time as time, u.name as username FROM Post as p, User as u WHERE p.ID = '{0}' AND p.userID = u.ID"
INSERT_ATTENDING = "INSERT INTO Attending VALUES ('{0}','{1}')"
INSERT_BELONGS = "INSERT INTO Belongs VALUES('{0}','{1}')"
INSERT_CODE = "INSERT INTO ConfirmationCode VALUES('{0}','{1}')"
GROUP_EVENT = "SELECT * FROM Meeting WHERE ID in (SELECT meetingID FROM GroupMeeting WHERE groupID = '{0}')"
INSERT_GROUP_MEETING = "INSERT INTO GroupMeeting VALUES('{0}','{1}')"
EMPTY_SET = "SELECT 1 FROM Dual WHERE false"
GET_EMAIL="SELECT email FROM User"
GET_PASS="SELECT password FROM User WHERE email='{0}'"
GET_ATTENDING="SELECT userID FROM Attending"
GET_BELONGS="SELECT userID FROM Belongs"
GET_CONFIRMED="SELECT confirmed FROM User WHERE email='{0}'"
CONFIRM_USR="UPDATE User SET confirmed = 1  WHERE email='{0}' "
DELETE_CONFIRM="DELETE FROM ConfirmationCode WHERE email='{0}'"
GET_CODE="SELECT code FROM ConfirmationCode WHERE email='{0}'"
#Post in group Queries
POST_ID = "SELECT CASE WHEN (SELECT MAX(ID) FROM Post) IS NULL THEN 1 ELSE (SELECT MAX(ID) FROM Post)+1 END"
POST = "INSERT INTO Post VALUES('{0}','{1}','{2}','{3}','{4}',CURDATE(),CURTIME())"
GROUP_POST = "INSERT INTO GroupPost VALUES('{0}','{1}')"
NOTIFICATION_ID = "SELECT CASE WHEN (SELECT MAX(ID) FROM Notifications) IS NULL THEN 1 ELSE (SELECT MAX(ID) FROM Notifications)+1 END"
NOTIFICATION = "INSERT INTO Notifications VALUES('{0}','{1}','{2}')"
CREATES = "INSERT INTO Creates VALUES ('{0}','{1}')"
HAS_NOTIFICATION = "INSERT INTO HasNotification VALUES('{0}','{1}')"
EVENT_ID = "SELECT CASE WHEN (SELECT MAX(ID) FROM Meeting) IS NULL THEN 1 ELSE (SELECT MAX(ID) FROM Meeting)+1 END"
GROUP_ID = "SELECT CASE WHEN (SELECT MAX(ID) FROM Groups) IS NULL THEN 1 ELSE (SELECT MAX(ID) FROM Groups)+1 END"
LEAVE_GROUP="DELETE FROM Belongs WHERE userID='{0}' and groupID='{1}'"
LEAVE_EVENT="DELETE FROM Attending WHERE userID='{0}' and meetingID='{1}'"
RESET_PASS = "UPDATE User SET password='{0}' WHERE email='{1}'"
#Post in event Queries
MEETING_POST = "INSERT INTO MeetingPost VALUES('{0}','{1}')"

#View Notifications
VIEW_NOTIFICATIONS = "SELECT message FROM Notifications WHERE ID IN (SELECT notificationID FROM HasNotification WHERE userID = '{0}')"

#Group Feeds
GROUP_FEEDS = "SELECT p.ID,p.userID,p.text,p.subject,p.date,u.name,u.profilePic From Post as p, User as u WHERE p.ID in (SELECT postID from GroupPost,Groups WHERE groupID='{0}') and p.userID = u.ID"
#Event Feeds
EVENT_FEEDS = "SELECT p.ID,p.userID,p.text,p.subject,p.date,u.name,u.profilePic From Post as p, User as u WHERE p.ID in (SELECT postID from MeetingPost,Meeting WHERE meetingID='{0}') and p.userID = u.ID"
#Post for colleagues
COLLEAGUES_POST = "INSERT INTO ColleaguesPost VALUES('{0}','{1}')"

#MainPost
FEED_MAIN = "Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID,'Event' as type from MeetingPost as mp, Meeting as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name,User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.meetingID = m.ID \
UNION \
Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID, 'Group' as type from GroupPost as mp, Groups as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name, User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.groupID = m.ID UNION \
SELECT notificationID, postID, subject,username,picture,message, uID as ID,name,uID, type FROM (select distinct(n.ID) as notificationID, p.postID, p.name as username,p.name as name, n.message as message, p.subject as subject, p.profilePic as picture, p.uID as uID,'User' as type from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID, text,document,date,time,subject,User.profilePic as profilePic,User.ID as uID ,name FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as A WHERE notificationID  \
NOT IN \
(SELECT notificationID FROM (Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID,'Event' as type from MeetingPost as mp, Meeting as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name,User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.meetingID = m.ID \
UNION \
Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID, 'Group' as type from GroupPost as mp, Groups as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name, User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.groupID = m.ID ) as B)"

FEED_NOTIFICATION = "Select * From (Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID,'Event' as type from MeetingPost as mp, Meeting as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name,User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.meetingID = m.ID \
UNION \
Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID, 'Group' as type from GroupPost as mp, Groups as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name, User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.groupID = m.ID UNION \
SELECT notificationID, postID, subject,username,picture,message, uID as ID,name,uID, type FROM (select distinct(n.ID) as notificationID, p.postID, p.name as username,p.name as name, n.message as message, p.subject as subject, p.profilePic as picture, p.uID as uID,'User' as type from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID, text,document,date,time,subject,User.profilePic as profilePic,User.ID as uID ,name FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as A WHERE notificationID NOT IN \
(SELECT notificationID FROM (Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID,'Event' as type from MeetingPost as mp, Meeting as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name,User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.meetingID = m.ID \
UNION \
Select p.notificationID as notificationID, p.postID as postID, p.subject as subject, p.username as username, p.profilePic as picture, p.message as message, m.ID as ID, m.name as name,p.uID as uID, 'Group' as type from GroupPost as mp, Groups as m, (select distinct(n.ID) as notificationID, n.message as message, p.profilePic as profilePic, p.postID, p.name as username, p.text as text, p.document as document, p.date as date, p.time as time, p.subject as subject, p.uID as uID from Notifications as n, HasNotification as h, Creates as c, (select Post.ID as postID,User.profilePic,text,document,date,time,subject,name, User.ID as uID FROM User,Post where Post.userID = User.ID) as p, User as u where u.ID='{0}' and h.userID='{0}' and n.ID = h.notificationID and c.notificationID = n.ID and c.postID = p.postID) as p where mp.postID = p.postID and mp.groupID = m.ID ) as B)) as T WHERE T.uID != {0}"