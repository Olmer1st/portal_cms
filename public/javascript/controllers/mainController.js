"use strict";
main_app.controller("mainController", function ($scope, $rootScope, $location) {
    $scope.getClass = function (path) {
        return ($location.path().substr(0, path.length) === path) ? 'active' : '';
    };
});
