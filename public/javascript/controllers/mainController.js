"use strict";
main_app.controller("mainController", function ($scope, $rootScope, $location, $state, principal) {
    $scope.currentUser =  $rootScope.GLOBALS.currentUser;
    
    $scope.form = {};
    $scope.getClass = function (path) {
        return ($location.path().substr(0, path.length) === path) ? 'active' : '';
    };

    $scope.isPermissionsForModule = function (moduleName) {
        if(!$scope.currentUser) return false;
        if($scope.currentUser.role == "admin") return true;
        if(!$scope.currentUser.modules || $scope.currentUser.modules.length()==0) return false;
        var module = $scope.currentUser.modules.find(function(item){
            return item.NAME == moduleName;
        });  
        
        return module != null;
    };

    $scope.login = function () {
        principal.ClearCredentials();

        principal.Login($scope.email, $scope.password, function (response) {
            if (response && !response.error) {
                principal.SetCredentials(response);
                $scope.currentUser =  $rootScope.GLOBALS.currentUser;
                $state.go('home');
            }
        });
    };

    $scope.logout = function () {
        principal.ClearCredentials();
        $scope.currentUser =  $rootScope.GLOBALS.currentUser;
        $state.go('home');
    };

});
