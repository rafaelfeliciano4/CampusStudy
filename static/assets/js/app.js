var App = angular.module('App', []);

App.controller('FeedsCtrl', function($scope, $http) {
  $http.get('json/feeds.json')
       .then(function(res){
          $scope.feeds = res.data;                
        });
});


App.controller('BioCtrl', function($scope, $http) {
  $http.get('json/bio.json')
       .then(function(res){
          $scope.bios = res.data;                
        });
});

App.controller('ColleaguesCtrl', function($scope, $http) {
  $http.get('json/colleagues.json')
       .then(function(res){
          $scope.colleagues = res.data;                
        });
});

App.controller('EventsCtrl', function($scope, $http) {
  $http.get('json/events.json')
       .then(function(res){
          $scope.events = res.data;                
        });
});

App.controller('GroupsCtrl', function($scope, $http) {
  $http.get('json/groups.json')
       .then(function(res){
          $scope.groups = res.data;                
        });
});

App.controller('PersonsCtrl', function($scope, $http) {
  $http.get('json/persons.json')
       .then(function(res){
          $scope.persons = res.data;                
        });
});

App.controller('ProfileCtrl', function($scope, $http) {
  $http.get('json/profile.json')
       .then(function(res){
          $scope.profiles = res.data;                
        });
});

App.controller('NotificationsCtrl', function($scope, $http) {
  $http.get('json/notifications.json')
       .then(function(res){
          $scope.notifications = res.data;                
        });
});

App.controller('FacultyCtrl', function($scope, $http) {
  $http.get('json/faculty.json')
       .then(function(res){
          $scope.faculties = res.data;                
        });
});

App.controller('GroupMembersCtrl', function($scope, $http) {
  $http.get('json/members.json')
       .then(function(res){
          $scope.members = res.data;                
        });
});

App.controller('GroupEventsCtrl', function($scope, $http) {
  $http.get('json/groupEvents.json')
       .then(function(res){
          $scope.groupEvents = res.data;                
        });
});

App.controller('GroupFeedCtrl', function($scope, $http) {
  $http.get('json/groupFeed.json')
       .then(function(res){
          $scope.groupFeed = res.data;                
        });
});

App.controller('GroupDescriptionCtrl', function($scope, $http) {
  $http.get('json/groupDescription.json')
       .then(function(res){
          $scope.groupDesc = res.data;                
        });
});

App.controller('EventDescriptionCtrl', function($scope, $http) {
  $http.get('json/eventDescription.json')
       .then(function(res){
          $scope.eventDesc = res.data;                
        });
});

App.controller('EventMembersCtrl', function($scope, $http) {
  $http.get('json/participants.json')
       .then(function(res){
          $scope.eventMem = res.data;                
        });
});

App.controller('EventFeedCtrl', function($scope, $http) {
  $http.get('json/eventFeed.json')
       .then(function(res){
          $scope.eventFeed = res.data;                
        });
});
