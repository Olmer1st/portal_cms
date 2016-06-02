"use strict";
var main_app = angular.module('main_app', ['ngCookies', 'ngAnimate', 'ngSanitize', 'ngTouch', 'ui.router', 'ui.bootstrap', 'ui.grid', 'ui.grid.treeView']);


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
            controller: 'libraryController',
            data: {
                loginRequired: true,
                admin: false
            }
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
        .state('profile', {
            url: '/profile',
            templateUrl: 'public/templates/profile.html',
            controller: 'profileController',
            data: {
                loginRequired: true,
                admin: false
            }
        })
        .state('admin', {
            url: '/admin',
            templateUrl: 'public/templates/admin.html',
            controller: 'adminController',
            data: {
                loginRequired: true,
                admin: true
            }
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

main_app.run(function ($http, $rootScope, $state, $cookieStore) {
    $rootScope.GLOBALS = {};
    $rootScope.GLOBALS.currentUser = $cookieStore.get('portalUserSession') || null;
    if ($rootScope.GLOBALS.currentUser) {
        $http.defaults.headers.common['x-access-token']  =  $rootScope.GLOBALS.currentUser.token;
    }
    $rootScope.$on('$stateChangeStart', function (e, to) {
        if (!to.data) return;
        if (to.data.loginRequired &&  $rootScope.GLOBALS.currentUser == null) {
            e.preventDefault();
            $state.go("home",null, {notify: false});
            return;
        }
        if (to.data.loginRequired && to.data.admin && $rootScope.GLOBALS.currentUser.role != "admin") {
            e.preventDefault();
            $state.go("home",null, {notify: false});
        }
    });
});