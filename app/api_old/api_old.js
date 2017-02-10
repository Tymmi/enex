'use strict';

var app = angular.module("api", ['ngRoute'])

    .config(['$scope', function ($routeProvider) {
        $routeProvider.when('/app', {
            templateUrl: 'app/index.html',
            controller: 'httpRequest'
        });
    }])

    .controller('lol', [function ($scope, $http) {
        $http({
            method: "GET",
            url: "http://eve-marketdata.com/api_old/"
        }).then(function successCallback(response) {
            // this callback will be called asynchronously
            // when the response is available
            $scope.content = response.data;
            $scope.statuscode = response.status;
            $scope.statustext = response.satustext;
            console.log("Success------" + JSON.stringify(response))
        }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            $scope.statuscode = errorCallback(response);
            console.log("Error------" + JSON.stringify(response) + " " + status)
        })

    }]);

/*
 var myApp = angular.module('myApp',[]);

 myApp.controller('GreetingController', ['$scope', function($scope) {
 $scope.greeting = 'Hola!';
 }]);
