"use strict";
main_app.controller("genres", function ($scope, $rootScope, $state, $timeout,  apiService, Notification) {
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

        Notification.info("Please note, this operation can be longer than usual, be patient...");
        $timeout(function(){
            libraryScope.findBooksByGenre(gid);
        },10, true);

    };

    function LoadingData(status) {
        $rootScope.safeApply(function () {
            $scope.loadingData = status
        });
    }
});
