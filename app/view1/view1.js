'use strict';

angular.module('myApp', [])

.controller('myCtrl', function($scope, dataService) {

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
    })

.config(['$routeProvider', function($routeProvider, $httpProvider) {
  $routeProvider.when('/view1', {
    templateUrl: 'view1/view1.html',
    controller: 'myCtrl'
  });
  //Enable cross domain calls
  $httpProvider.defaults.useXDomain = true;
}])

.service('myCtrl', function($http) {
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
