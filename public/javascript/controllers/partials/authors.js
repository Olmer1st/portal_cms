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
            $scope.loadingData = false;
        });

    };

    $scope.executeSearch = function () {
        $scope.authors = [];
        if (!$scope.searchParam) return;
        $scope.loadingData = true;
        var promise = apiService.searchForAuthor($scope.searchParam);
        promise.then(function (result) {
            if (!result || result.error) {
                $scope.loadingData =false;
                return;
            }
            $rootScope.safeApply(function () {
                $scope.authors = result.rows;
                $scope.loadingData = false
            });

        }, function (reason) {
            $scope.loadingData = false;
        });
    };
});
