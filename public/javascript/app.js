"use strict";
var main_app = angular.module('main_app', ['ngCookies', 'ngAnimate', 'ngSanitize', 'ui.router', 'ui.bootstrap']);


main_app.config(function ($locationProvider) {
    $locationProvider.html5Mode(true);
});

main_app.config(function ($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state('home', {
            url: '/home',
            templateUrl: 'public/templates/home.html',
            controller: 'homeController'
        })
        .state('library', {
            url: '/library',
            templateUrl: 'public/templates/library.html',
            controller: 'libraryController'
        })
        .state('library.authors', {
            url: '/authors',
            views: {
                'leftside': {
                    templateUrl: 'public/templates/partials/authors.html',
                    controller: 'authors'
                },
                'books': {
                    templateUrl: 'public/templates/partials/books.html',
                }
            }
        })
        .state('library.genres', {
            url: '/genres',
            views: {
                'leftside': {
                    templateUrl: 'public/templates/partials/genres.html',
                },
                'books': {
                    templateUrl: 'public/templates/partials/books.html',
                }
            }
        })
        .state('library.series', {
            url: '/series',
            views: {
                'leftside': {
                    templateUrl: 'public/templates/partials/series.html',
                },
                'books': {
                    templateUrl: 'public/templates/partials/books.html',
                }
            }
        })
        .state('library.search', {
            url: '/search',
            views: {
                'leftside': {
                    templateUrl: 'public/templates/partials/search.html',
                },
                'books': {
                    templateUrl: 'public/templates/partials/books.html',
                }
            }
        })
        .state('login', {
            url: '/login',
            templateUrl: 'public/templates/login.html',
            controller: 'loginController'
        })
        .state('admin', {
            url: '/admin',
            templateUrl: 'public/templates/admin.html',
            controller: 'adminController'
        });

    $urlRouterProvider.otherwise('/home');
});

main_app.config(function ($provide) {
    return $provide.decorator('$rootScope', function ($delegate) {
        $delegate.safeApply = function (fn) {
            var phase = $delegate.$$phase;
            if (phase === "$apply" || phase === "$digest") {
                if (fn && typeof fn === 'function') {
                    fn();
                }
            } else {
                $delegate.$apply(fn);
            }
        };
        return $delegate;
    });
});