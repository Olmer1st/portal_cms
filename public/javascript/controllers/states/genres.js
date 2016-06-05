"use strict";
main_app.controller("genres", function ($scope, $rootScope, $state, apiService) {
    var libraryScope = $scope.$parent;
    var mainScope = libraryScope.$parent;

    $scope.searchParam = '';
    $scope.genres = [];
    $scope.loadingData = false;

    $scope.clearSearch = function () {
        $rootScope.safeApply(function () {
            $scope.searchParam='';
        });

    };

  function getAllGenres() {
        LoadingData(true);
        apiService.getAllGenres().then(function (response) {
            if (response && !response.error) {
                $scope.genres = response.children;
            }
            LoadingData(false);
        });
    }

    $scope.init = function () {
        getAllGenres();
    };
    $scope.init();

    $scope.findBooksByGenre = function (gid) {
        libraryScope.findBooksByGenre(gid);
    };

    function LoadingData(status) {
        $rootScope.safeApply(function () {
            $scope.loadingData = status
        });
    }
});
