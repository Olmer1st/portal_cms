"use strict";
main_app.controller("libraryController", function ($scope, $rootScope, $location, $state, $timeout, uiGridTreeViewConstants, apiService) {
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
    
    $scope.findBooksInSerie = function (sid) {
        $scope.books = [];
        if (!sid) return;
        LoadingData(true);
        var promise = apiService.searchForBooksBySerie(sid);
        promise.then(function (result) {
            if (result && !result.error) {
                $rootScope.safeApply(function () {
                    //$scope.books = result.rows;
                    $scope.gridOptions.data = result.rows;

                });
            }
            $timeout(function () {
                $scope.gridApi.treeBase.expandAllRows();
            },0, true)

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

    //AID, BID, TITLE, SERIE_NAME, SERIE_NUMBER, GENRE, FILE, EXT, DEL, LANG, SIZE, DATE, LIBRATE, KEYWORDS, PATH
    $scope.gridOptions = {
        enableSorting: false,
        enableFiltering: false,
        showTreeExpandNoChildren: false,
        columnDefs: [
            {name: 'name', width: '45%', field:"TITLE", enableColumnMenu:false},
            {name: '#', width: '2%', field: "SERIE_NUMBER", enableColumnMenu:false},
            {name: 'size', width: '5%', field: "SIZE", enableColumnMenu:false},
            {name: 'lang.', width: '2%', field: "LANG",enableColumnMenu:false},
            {name: 'date', width: '10%', field: "DATE", enableColumnMenu:false},
            {name: 'genre', width: '*', field: "GENRE", enableColumnMenu:false}
        ],
        onRegisterApi: function (gridApi) {
            $scope.gridApi = gridApi;
        }
    };
});
