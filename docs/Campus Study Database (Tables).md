#Campus Study Database

####Table structure for table `Attending`

CREATE TABLE `Attending` (
  `userID` varchar(8) NOT NULL,
  `meetingID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `Belongs`

CREATE TABLE `Belongs` (
  `userID` varchar(8) NOT NULL,
  `groupID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `Category`

CREATE TABLE `Category` (
  `ID` varchar(8) NOT NULL,
  `faculty` char(50) NOT NULL,
  `courseName` char(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `Colleagues`

CREATE TABLE `Colleagues` (
  `userID` varchar(8) NOT NULL,
  `colleagueID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `ColleaguesPost`

CREATE TABLE `ColleaguesPost` (
  `postID` varchar(8) NOT NULL,
  `colleagueID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;





####Table structure for table `Creates`

CREATE TABLE `Creates` (
  `postID` varchar(8) NOT NULL,
  `notificationID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `GroupCategory`

CREATE TABLE `GroupCategory` (
  `groupID` varchar(8) NOT NULL,
  `categoryID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `GroupPost`

CREATE TABLE `GroupPost` (
  `postID` varchar(8) NOT NULL,
  `groupID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `Groups`

CREATE TABLE `Groups` (
  `ID` varchar(8) NOT NULL,
  `tutorID` varchar(8) NOT NULL,
  `name` char(30) NOT NULL,
  `courseName` char(30) DEFAULT NULL,
  `section` varchar(10) NOT NULL,
  `faculty` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `HasNotification`

CREATE TABLE `HasNotification` (
  `notificationID` varchar(8) NOT NULL,
  `userID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




####Table structure for table `Meeting`

CREATE TABLE `Meeting` (
  `ID` varchar(8) NOT NULL,
  `name` varchar(30) NOT NULL,
  `location` varchar(30) NOT NULL,
  `time` time NOT NULL,
  `date` date NOT NULL,
  `courseName` char(30) DEFAULT NULL,
  `faculty` char(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `MeetingCategory`

CREATE TABLE `MeetingCategory` (
  `meetingID` varchar(8) NOT NULL,
  `categoryID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `MeetingPost`

CREATE TABLE `MeetingPost` (
  `postID` varchar(8) NOT NULL,
  `meetingID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `Notifications`

CREATE TABLE `Notifications` (
  `ID` varchar(8) NOT NULL,
  `userID` varchar(8) DEFAULT NULL,
  `message` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



####Table structure for table `Post`

CREATE TABLE `Post` (
  `ID` varchar(8) NOT NULL,
  `userID` varchar(8) DEFAULT NULL,
  `text` varchar(1000) NOT NULL,
  `document` longblob NOT NULL,
  `subject` varchar(40) NOT NULL,
  `image` longblob NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `User`

CREATE TABLE `User` (
  `ID` varchar(8) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `name` char(50) NOT NULL,
  `major` char(50) NOT NULL,
  `faculty` char(50) NOT NULL,
  `profilePic` longblob,
  `bio` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


####Table structure for table `UserFaculty`

CREATE TABLE `UserFaculty` (
  `userID` varchar(8) NOT NULL,
  `categoryID` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

