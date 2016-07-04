"use strict";
main_app.controller("search", function ($scope, $rootScope, $state, apiService) {
    var libraryScope = $scope.$parent;
    var mainScope = libraryScope.$parent;
    $scope.searchParam = {};
    $scope.genres = [];
    $scope.loadingData = false;
    $scope.searchParam.dtFrom = (new Date()).setMonth((new Date()).getMonth() - 1);
    $scope.searchParam.dtTo = new Date();

    $scope.dateOptions = {
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22),
        minDate: new Date(2007, 1, 1),
        startingDay: 1
    };


    $scope.open1 = function () {
        $scope.popup1.opened = true;
    };

    $scope.open2 = function () {
        $scope.popup2.opened = true;
    };


    $scope.popup1 = {
        opened: false
    };

    $scope.popup2 = {
        opened: false
    };

    $scope.clearSearch = function () {
        $rootScope.safeApply(function () {
            $scope.searchParam = {};
        });

    };
    function formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [year, month, day].join('-');
    }

    function getAllGenres() {
        LoadingData(true);
        apiService.getAllGenres().then(function (response) {
            if (response && !response.error) {
                $scope.genres = response.children;
            }
            LoadingData(false);
        });
    }

    $scope.searchByForm = function () {
        var options = {};
        options.author = $scope.searchParam.anchor?$scope.searchParam.anchor:'all';
        options.title = $scope.searchParam.title?$scope.searchParam.title:'all';
        options.gid = $scope.searchParam.genre?$scope.searchParam.genre:'all';
        options.fromDate =formatDate($scope.searchParam.dtFrom);
        options.toDate = formatDate($scope.searchParam.dtTo);
        libraryScope.findBooksbySearchForm(options);
    };

    $scope.init = function () {
        getAllGenres();
    };
    $scope.init();

    function LoadingData(status) {
        $rootScope.safeApply(function () {
            $scope.loadingData = status
        });
    }


});