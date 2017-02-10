'use strict';

angular.module('myApp.view1', ['ngRoute'])

.config(['$routeProvider', function($routeProvider, $httpProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'angularJSCtrl'
  });
  //Enable cross domain calls
  $httpProvider.defaults.useXDomain = true;
}])

.service('dataService', function($http) {
    delete $http.defaults.headers.common['X-Requested-With'];
    this.getData = function() {
        return $http({
            method: 'GET',
            url: 'http://eve-marketdata.com/api/',
            data: JSON.stringify(response),
            params: 'limit=10, sort_by=created:desc',
            withCredentials: true,
            headers: {'Authorization': 'Basic bashe64usename:password'}
        });
    }
})


.controller('angularJSCtrl', function($scope, dataService) {

      $scope.data = null;
      dataService.getData().then(function (dataResponse) {
        // this callback will be called asynchronously
        // when the response is available
       // $scope.content = response.data;
       // $scope.statuscode = response.status;
       // $scope.statustext = response.satustext;
          $scope.data = dataResponse;
        console.log("Success------" + JSON.stringify(dataResponse))
    })
});


    , function (response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        //$scope.statuscode = errorCallback(response);
        console.log("Error------" + JSON.stringify(response) + " " + status)
    })
})
/*
var myApp = angular.module('myApp',[]);

myApp.service('dataService', function($http) {
    delete $http.defaults.headers.common['X-Requested-With'];
    this.getData = function() {
        // $http() returns a $promise that we can add handlers with .then()
        return $http({
            method: 'GET',
            url: 'https://www.example.com/api/v1/page',
            params: 'limit=10, sort_by=created:desc',
            headers: {'Authorization': 'Token token=xxxxYYYYZzzz'}
        });
    }
});

myApp.controller('AngularJSCtrl', function($scope, dataService) {
    $scope.data = null;
    dataService.getData().then(function(dataResponse) {
        $scope.data = dataResponse;
    });
});