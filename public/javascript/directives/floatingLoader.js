main_app.directive('floatingLoader', function () {
    return {
        restrict: 'E',
        replace: true,
        scope: {status: '=', obj: '='},
        link: function (scope, ele, attrs) {
        },
        templateUrl: '/public/templates/directives/floatingLoader.html?_=' + (new Date())
    };
});