"use strict";
main_app.controller("libraryController", function ($scope, $rootScope, $location, $state) {
    $scope.leftBar = {
        isOpen: true
    };
    $scope.buttons = [{
        name: "library.authors",
        title: "Authors",
        active: true
    }, {
        name: "library.genres",
        title: "Genres",
        active: false
    }, {
        name: "library.series",
        title: "Series",
        active: false
    }, {
        name: "library.search",
        title: "Search",
        active: false
    }];
    
    $scope.init = function () {
        var defaultButton = $scope.buttons.find(function (item) {
                return item.active;
            }) || $scope.buttons[0];

        $state.go(defaultButton.name);
    };
    $scope.init();

    $scope.executeState = function ($index) {
        $rootScope.safeApply(function () {
            for (var i = 0; i < $scope.buttons.length; i++) {
                if (i != $index) {
                    $scope.buttons[i].active = false;
                }
            }
            $scope.buttons[$index].active = true;
            $state.go($scope.buttons[$index].name);
        });

    };
});
