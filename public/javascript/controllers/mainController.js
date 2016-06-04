"use strict";
main_app.controller("mainController", function ($scope, $rootScope, $location, $state, principal,Notification) {
    $scope.currentUser =  $rootScope.GLOBALS.currentUser;
    
    $scope.getClass = function (path) {
        return ($location.path().substr(0, path.length) === path) ? 'active' : '';
    };

    $scope.isPermissionsForModule = function (moduleName) {
       return principal.isPermissionsForModule(moduleName);
    };

    $scope.login = function () {
        principal.ClearCredentials();

        principal.Login($scope.email, $scope.password, function (response) {
            if (response && !response.error) {
                principal.SetCredentials(response);
                $scope.currentUser =  $rootScope.GLOBALS.currentUser;
                $state.go('home');
            }else if(response && response.error){
                Notification.error(response.error);
            }
        });
    };

    $scope.logout = function () {
        principal.ClearCredentials();
        $scope.currentUser =  $rootScope.GLOBALS.currentUser;
        $state.go('home');
    };

});
