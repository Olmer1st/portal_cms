"use strict";
var main_app = angular.module('main_app', [ 'ngCookies','ngAnimate','ngSanitize','ui.router', 'ui.bootstrap']);


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
            .state('library.authors', {
                url: '/authors',
                views:{
                    'leftside':{
                         templateUrl: 'public/partials/templates/authors.html',
                    },
                    'books':{
                         templateUrl: 'public/partials/templates/books.html',
                    }
                }
            })
            .state('library.genres', {
                url: '/genres',
                views:{
                    'leftside':{
                         templateUrl: 'public/partials/templates/genres.html',
                    },
                    'books':{
                         templateUrl: 'public/partials/templates/books.html',
                    }
                }
            })
            .state('library.series', {
                url: '/series',
                views:{
                    'leftside':{
                         templateUrl: 'public/partials/templates/series.html',
                    },
                    'books':{
                         templateUrl: 'public/partials/templates/books.html',
                    }
                }
            })
            .state('library.search', {
                url: '/search',
                views:{
                    'leftside':{
                         templateUrl: 'public/partials/templates/search.html',
                    },
                    'books':{
                         templateUrl: 'public/partials/templates/books.html',
                    }
                }
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
