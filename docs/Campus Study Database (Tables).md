#Campus Study Database

-- Table structure for table `Attending`

CREATE TABLE `Attending` (
  `userID` int(8) NOT NULL,
  `meetingID` int(8) NOT NULL,
  KEY `uID` (`userID`),
  KEY `mID` (`meetingID`),
  CONSTRAINT `attending_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `attending_ibfk_2` FOREIGN KEY (`meetingID`) REFERENCES `Meeting` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `Belongs`

CREATE TABLE `Belongs` (
  `userID` int(8) NOT NULL,
  `groupID` int(8) NOT NULL,
  KEY `uID` (`userID`),
  KEY `gID` (`groupID`),
  CONSTRAINT `belongs_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `belongs_ibfk_2` FOREIGN KEY (`groupID`) REFERENCES `Groups` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `Colleagues`

CREATE TABLE `Colleagues` (
  `userID` int(8) NOT NULL,
  `colleagueID` int(8) NOT NULL,
  KEY `uID` (`userID`),
  KEY `fID` (`colleagueID`),
  CONSTRAINT `colleagues_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `colleagues_ibfk_2` FOREIGN KEY (`colleagueID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `ColleaguesPost`

CREATE TABLE `ColleaguesPost` (
  `postID` int(8) NOT NULL,
  `colleagueID` int(8) NOT NULL,
  KEY `postID` (`postID`),
  KEY `colleagueID` (`colleagueID`),
  CONSTRAINT `colleaguespost_ibfk_1` FOREIGN KEY (`postID`) REFERENCES `Post` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `colleaguespost_ibfk_2` FOREIGN KEY (`colleagueID`) REFERENCES `Colleagues` (`colleagueID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `ConfirmationCode`

CREATE TABLE `ConfirmationCode` (
  `email` varchar(250) NOT NULL,
  `code` varchar(250) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Table structure for table `Creates`

CREATE TABLE `Creates` (
  `postID` int(8) NOT NULL,
  `notificationID` int(8) NOT NULL,
  KEY `postID` (`postID`,`notificationID`),
  KEY `notificationID` (`notificationID`),
  CONSTRAINT `creates_ibfk_1` FOREIGN KEY (`postID`) REFERENCES `Post` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `creates_ibfk_2` FOREIGN KEY (`notificationID`) REFERENCES `Notifications` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `GroupMeeting`

CREATE TABLE `GroupMeeting` (
  `groupID` int(8) NOT NULL,
  `meetingID` int(8) NOT NULL,
  KEY `fk_meetingID` (`meetingID`),
  KEY `fk_groupID` (`groupID`),
  CONSTRAINT `fk_groupID` FOREIGN KEY (`groupID`) REFERENCES `Groups` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_meetingID` FOREIGN KEY (`meetingID`) REFERENCES `Meeting` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Table structure for table `GroupPost`

CREATE TABLE `GroupPost` (
  `postID` int(8) NOT NULL,
  `groupID` int(8) NOT NULL,
  KEY `postID` (`postID`),
  KEY `groupID` (`groupID`),
  CONSTRAINT `grouppost_ibfk_1` FOREIGN KEY (`postID`) REFERENCES `Post` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `grouppost_ibfk_2` FOREIGN KEY (`groupID`) REFERENCES `Groups` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `Groups`

CREATE TABLE `Groups` (
  `ID` int(8) NOT NULL,
  `tutorID` int(8) NOT NULL,
  `name` varchar(250) NOT NULL,
  `purpose` varchar(250) DEFAULT NULL,
  `faculty` varchar(250) NOT NULL,
  `picture` longblob,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `HasNotification`

CREATE TABLE `HasNotification` (
  `notificationID` int(8) NOT NULL,
  `userID` int(8) NOT NULL,
  KEY `notificationID` (`notificationID`,`userID`),
  KEY `userID` (`userID`),
  CONSTRAINT `hasnotification_ibfk_1` FOREIGN KEY (`notificationID`) REFERENCES `Notifications` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `hasnotification_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `User` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `Meeting`

CREATE TABLE `Meeting` (
  `ID` int(8) NOT NULL,
  `name` varchar(250) NOT NULL,
  `location` varchar(250) NOT NULL,
  `time` varchar(250) NOT NULL,
  `date` varchar(250) NOT NULL,
  `purpose` varchar(250) DEFAULT NULL,
  `faculty` varchar(250) NOT NULL,
  `picture` longblob,
  `admin` varchar(250) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `MeetingPost`

CREATE TABLE `MeetingPost` (
  `postID` int(8) NOT NULL,
  `meetingID` int(8) NOT NULL,
  KEY `postID` (`postID`),
  KEY `meetingID` (`meetingID`),
  CONSTRAINT `meetingpost_ibfk_1` FOREIGN KEY (`postID`) REFERENCES `Post` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `meetingpost_ibfk_2` FOREIGN KEY (`meetingID`) REFERENCES `Meeting` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `Notifications`

CREATE TABLE `Notifications` (
  `ID` int(8) NOT NULL,
  `userID` int(8) NOT NULL,
  `message` varchar(250) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `Post`

CREATE TABLE `Post` (
  `ID` int(8) NOT NULL,
  `userID` int(8) NOT NULL,
  `text` varchar(250) NOT NULL,
  `document` longblob,
  `subject` varchar(250) DEFAULT NULL,
  `date` varchar(250) NOT NULL,
  `time` varchar(250) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `User`

CREATE TABLE `User` (
  `ID` int(8) NOT NULL AUTO_INCREMENT,
  `email` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  `name` varchar(250) NOT NULL,
  `major` varchar(250) NOT NULL,
  `faculty` varchar(250) NOT NULL,
  `profilePic` longblob,
  `bio` varchar(250) DEFAULT NULL,
  `confirmed` varchar(250) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=latin1;
