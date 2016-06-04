"use strict";
main_app.controller("series", function ($scope, $rootScope, $state, apiService,$log) {
    
    $scope.loadingData = false;
    $scope.pageChanged = function () {
        getAllSeries();
    };
    $scope.series = [];
    $scope.maxSize = 5;
    $scope.totalItems = 0;
    $scope.currentPage = 1;
    $scope.itemsPerPage = 50;

    function getAllSeries(){
        $scope.loadingData = true;
        apiService.getAllSeries($scope.currentPage, $scope.itemsPerPage).then(function (response) {
            if(response && !response.error){
                 $scope.totalItems = response.totalSeries;
                 $scope.series = response.series;
            }
             $scope.loadingData = false;
        });
    }

    $scope.init = function () {
       getAllSeries();
    };
    $scope.init();

});
