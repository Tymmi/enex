'use strict';

var myAngularModule = angular.module('myApp', ['ngRoute']);

myAngularModule.controller('myCtrl', function($scope, myService) {
        var self = this;

        self.data = null;
        myService.getData().then(function (dataResponse) {
            // this callback will be called asynchronously
            // when the response is available
            // $scope.content = response.data;
            // $scope.statuscode = response.status;
            // $scope.statustext = response.satustext;

            //show full data
            //self.data = JSON.stringify(dataResponse, null, 2);
            var changePrice = function (){
                console.log(dataResponse.data.price = "1337");
                self.data.price = ["1337","100","142"];
                $scope.$apply()
            };
            setInterval(changePrice, 1000);



            self.data = dataResponse;
            console.log(dataResponse);
            self.data.buysell = dataResponse.data.buysell;
            self.data.typeID = dataResponse.data.typeID;
            self.data.orderID = dataResponse.data.orderID;
            self.data.stationID = dataResponse.data.stationID;
            self.data.solarsystemID = dataResponse.data.solarsystemID;
            self.data.regionID = dataResponse.data.regionID;
            self.data.price = dataResponse.data.price;
            self.data.volEntered = dataResponse.data.volEntered;
            self.data.volRemaining = dataResponse.data.volRemaining;
            self.data.minVolume = dataResponse.data.minVolume;
            self.data.range = dataResponse.data.range;
            self.data.issued = dataResponse.data.issued;
            self.data.expires = dataResponse.data.expires;
            self.data.created = dataResponse.data.created;




            //alle teil Objekte Variablen wie oben
            console.log("Success------ ENEX TAKES OVER THE WORLD" + JSON.stringify(dataResponse, null, 2))

        })
        });

myAngularModule.config(['$httpProvider' , '$routeProvider', '$locationProvider', function($httpProvider, $routeProvider, $locationProvider) {
  //Enable cross domain calls
  $httpProvider.defaults.useXDomain = true;
  $routeProvider.otherwise({redirectTo: '/view1'});
  $locationProvider.hashPrefix('!');
}]);

myAngularModule.service('myService', function($http) {
    delete $http.defaults.headers.common['X-Requested-With'];
    this.getData = function() {
        return $http({
            method: 'GET',
            url: '../data/trainingData.json',
            params: 'limit=10, sort_by=created:desc',
            withCredentials: true

        })
    }
});