"use strict";
main_app.controller("series", function ($scope, $rootScope, $state, apiService, $log) {
    var libraryScope = $scope.$parent;
    var mainScope = libraryScope.$parent;

    $scope.allSeries = true;
    $scope.loadingData = false;
    $scope.pageChanged = function () {
        getAllSeries();
    };
    $scope.series = [];
    $scope.maxSize = 5;
    $scope.totalItems = 0;
    $scope.currentPage = 1;
    $scope.itemsPerPage = 50;

    function getAllSeries() {
        LoadingData(true);
        apiService.getAllSeries($scope.currentPage, $scope.itemsPerPage).then(function (response) {
            if (response && !response.error) {
                $scope.totalItems = response.totalSeries;
                $scope.series = response.series;
            }
            LoadingData(false);
        });
    }

    $scope.init = function () {
        getAllSeries();
    };
    $scope.init();

    $scope.findBooksOfSerie = function (sid) {
        libraryScope.findBooksInSerie(sid);
    };

    $scope.executeSearch = function () {
        $scope.allSeries = false;
        $scope.series = [];
        if (!$scope.searchParam) return;
        LoadingData(true);
        var promise = apiService.searchForSeries($scope.searchParam);
        promise.then(function (response) {
            if (response && !response.error) {
                $rootScope.safeApply(function () {
                    $scope.series = response.series;
                });
            }
            LoadingData(false);

        }, function (reason) {
            LoadingData(false);
        });
    };

    $scope.clearSearch = function () {
        $rootScope.safeApply(function () {
            $scope.searchParam = '';
            $scope.allSeries = true;
            
        });
        getAllSeries();
    };
    
    function LoadingData(status) {
        $rootScope.safeApply(function () {
            $scope.loadingData = status
        });
    }
});
