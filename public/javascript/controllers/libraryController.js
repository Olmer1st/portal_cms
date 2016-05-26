"use strict";
main_app.controller("libraryController", function($scope, $rootScope, $location) {
 $scope.categories = {
        values: [{
            name: "Releases",
            desc: "Release managment",
            title: "Release managment",
            status: {
                open: false
            }
        }, {
            name: "Maintenance",
            desc: "Maintenance managment",
            title: "Application support",
            status: {
                open: false
            }
        }, {
            name: "Projects",
            desc: "Projects managment",
            title: "Projects managment",
            status: {
                open: false
            }
        }, {
            name: "IT",
            desc: "IT managment",
            title: "IT managment",
            status: {
                open: false
            }
        }],
        isOpen: true

    };


});
