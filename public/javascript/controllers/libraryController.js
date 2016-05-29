"use strict";
main_app.controller("libraryController", function ($scope, $rootScope, $location, $state, uiGridTreeViewConstants, apiService) {
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

    $scope.hideLeftBar= function () {
        $scope.leftBar.isOpen = !$scope.leftBar.isOpen;
        $scope.gridApi.grid.refresh();
    };

    $scope.loadingData = false;

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

    $scope.findBooksOfAuthor = function (aid) {
        $scope.books = [];
        if (!aid) return;
        LoadingData(true);
        var promise = apiService.searchForBooksByAuthor(aid);
        promise.then(function (result) {
            if (result && !result.error) {
                $rootScope.safeApply(function () {
                    //$scope.books = result.rows;
                    $scope.gridOptions.data = result.rows;
                });
            }
            LoadingData(false);

        }, function (reason) {
            LoadingData(false);
        });
    };

    function LoadingData(status) {
        $rootScope.safeApply(function () {
            $scope.loadingData = status
        });
    }

    //`AID`, `BID`, `TITLE`, `serie_name`, `serie_number`, `GENRE`, `FILE`, `EXT`, `DEL`, `LANG`, `SIZE`, `DATE`, `LIBRATE`, `KEYWORDS`, `PATH`
    $scope.gridOptions = {
        enableSorting: true,
        enableFiltering: true,
        showTreeExpandNoChildren: true,
        columnDefs: [
            {name: 'name', width: '50%', field:"TITLE"},
            {name: 'ser.num', width: '10%', field: "serie_number"},
            {name: 'size', width: '10%', field: "SIZE"},
            {name: 'language', width: '10%', field: "LANG"},
            {name: 'genre', width: '*', field: "GENRE"}
        ],
        onRegisterApi: function (gridApi) {
            $scope.gridApi = gridApi;
        }
    };
});
