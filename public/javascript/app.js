"use strict";
var main_app = angular.module('main_app', ['ngSanitize','ui.router', 'ui.bootstrap', 'ngCookies']);


main_app.config(function ($locationProvider) {
    $locationProvider.html5Mode(true);
});

main_app.config(function ($stateProvider, $urlRouterProvider) {
    $stateProvider
            .state('home', {
                url: '/home',
                templateUrl: 'public/partials/home.html',
                controller: 'homeController'
            })
            .state('library', {
                url: '/library',
                templateUrl: 'public/partials/library.html',
                controller: 'libraryController'
            })
            .state('login', {
                url: '/login',
                templateUrl: 'public/partials/login.html',
                controller: 'loginController'
            })
            .state('admin', {
                url: '/admin',
                templateUrl: 'public/partials/admin.html',
                controller: 'adminController'
            });

    $urlRouterProvider.otherwise('/home');
});
