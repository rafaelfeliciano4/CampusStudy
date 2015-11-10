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

App.controller('EventsCtrl', function($scope, $http) {
 $http.get('/eventsInfo')
       .success(function(data){
          $scope.events = data.eventsInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

App.controller('GroupsCtrl', function($scope, $http) {
 $http.get('/groupsInfo')
       .success(function(data){
          $scope.groups = data.groupsInfo;
       }).error(function(data,status){
           alert(data + "\n\n\n\n\n" + status);
       });
});

