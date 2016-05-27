main_app.directive('floatingLoader', function () {
    return {
        restrict: 'E',
        replace: true,
        scope: {status: '=', obj: '='},
        link: function (scope, ele, attrs) {
        },
        templateUrl: '/public/partials/directives/floatingLoader.html?_=' + (new Date())
    };
});