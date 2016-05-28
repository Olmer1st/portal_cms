"use strict";
main_app.controller("authors", function ($scope, $rootScope, $state, apiService) {
    var libraryScope = $scope.$parent;
    var mainScope = libraryScope.$parent;
    
    $scope.searchParam = '';
    $scope.authors = [];
    $scope.loadingData = false;

    $scope.clearSearch = function () {
        $rootScope.safeApply(function () {
            $scope.searchParam = '';
        });

    };

    $scope.executeSearch = function () {
        $scope.authors = [];
        if (!$scope.searchParam) return;
        LoadingData(true);
        var promise = apiService.searchForAuthor($scope.searchParam);
        promise.then(function (result) {
            if (result && !result.error) {
                $rootScope.safeApply(function () {
                    $scope.authors = result.rows;
                });
            }
            LoadingData(false);

        }, function (reason) {
            LoadingData(false);
        });
    };
    $scope.findBooksOfAuthor = function (aid) {
        libraryScope.findBooksOfAuthor(aid);
    };

    function LoadingData(status) {
        $rootScope.safeApply(function () {
            $scope.loadingData = status
        });
    }
});
