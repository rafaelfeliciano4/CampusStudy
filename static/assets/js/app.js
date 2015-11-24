var App = angular.module('App', []);

App.controller('ColleaguesCtrl', function($scope, $http) {
  $http.get('/Colleagues')
       .success(function(data){
          $scope.colleagues = data.colleagueInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('cColleaguesCtrl', function($scope, $http) {
  $http.get('/cColleagues')
       .success(function(data){
          $scope.cColleagues = data.cColleaguesInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('ProfileUserCtrl', function($scope, $http) {
 $http.get('/profileUserInfo')
       .success(function(data){
          $scope.profiles = data.userInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});


App.controller('ProfileCtrl', function($scope, $http) {
 $http.get('/profilesInfo')
       .success(function(data){
          $scope.profiles = data.userInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('UserEventsCtrl', function($scope, $http) {
 $http.get('/userEvents')
       .success(function(data){
          $scope.events = data.userEvents;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('UserGroupsCtrl', function($scope, $http) {
 $http.get('/userGroups')
       .success(function(data){
          $scope.groups = data.userGroups;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('EventsInfoCtrl', function($scope, $http) {
 $http.get('/eventsInfo')
       .success(function(data){
          $scope.events = data.eventsInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('GroupsInfoCtrl', function($scope, $http) {
 $http.get('/groupsInfo')
       .success(function(data){
          $scope.groups = data.groupsInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('GroupMembersCtrl', function($scope, $http) {
 $http.get('/groupMembers')
       .success(function(data){
          $scope.gMembers = data.groupMembers;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('EventMembersCtrl', function($scope, $http) {
 $http.get('/eventMembers')
       .success(function(data){
          $scope.eMembers = data.eventMembers;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('EventAdminCtrl', function($scope, $http) {
 $http.get('/eventAdmin')
       .success(function(data){
          $scope.eventAdmin = data.eventAdminInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('AttendingEventCtrl', function($scope, $http) {
 $http.get('/attendingUsers')
       .success(function(data){
          $scope.attending = data.attendingUsers;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('GroupTutorCtrl', function($scope, $http) {
 $http.get('/groupTutor')
       .success(function(data){
          $scope.tutor = data.groupTutorInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('GroupFeedsCtrl', function($scope, $http) {
 $http.get('/GroupFeeds')
       .success(function(data){
          $scope.feeds = data.groupFeeds;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('EventFeedsCtrl', function($scope, $http) {
 $http.get('/EventFeeds')
       .success(function(data){
          $scope.feeds = data.eventFeeds;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('HomeFeedsCtrl', function($scope, $http) {
 $http.get('/HomeFeeds')
       .success(function(data){
          $scope.feeds = data.homeFeeds;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('NotificationsCtrl', function($scope, $http) {
 $http.get('/notificationsData')
       .success(function(data){
          $scope.notifications = data.notificationInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('PostCtrl', function($scope, $http) {
 $http.get('/postData')
       .success(function(data){
          $scope.posts = data.postInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('GroupEventsInfoCtrl', function($scope, $http) {
 $http.get('/groupEvents')
       .success(function(data){
          $scope.gEvents = data.groupEventsInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('SearchCtrl', function($scope, $http) {
 $http.get('/SearchData')
       .success(function(data){
          $scope.search = data.searchInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('ColGroupsCtrl', function($scope, $http) {
 $http.get('/colleagueGroups')
       .success(function(data){
          $scope.cgroups = data.userGroups;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});


