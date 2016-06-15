"use strict";
main_app.controller("libraryController", function ($scope, $rootScope, $location, $state, $timeout, uiGridTreeViewConstants, apiService, FileSaver, Blob) {
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

    $scope.selectedBook = {book: null, downloading: false};

    $scope.languages = [];
    $scope.language = {LANG: "ru"};
    $scope.isHideDeleted = true;
    $scope.hideLeftBar = function () {
        $scope.leftBar.isOpen = !$scope.leftBar.isOpen;
        $scope.gridApi.grid.refresh();
    };

    $scope.loadingData = false;

    $scope.init = function () {


        apiService.getAllLanguages().then(function (response) {
            if (response && !response.error) {
                $scope.languages = response.rows;
                $scope.languages.unshift({LANG: 'all'});
            }
        });
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
        var promise = apiService.searchForBooksByAuthor(aid, $scope.language.LANG, $scope.isHideDeleted);
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
        var promise = apiService.searchForBooksBySerie(sid, $scope.language.LANG, $scope.isHideDeleted);
        promise.then(function (result) {
            if (result && !result.error) {
                $rootScope.safeApply(function () {
                    //$scope.books = result.rows;
                    $scope.gridOptions.data = result.rows;

                });
            }
            $timeout(function () {
                $scope.gridApi.treeBase.expandAllRows();
            }, 0, true)

            LoadingData(false);

        }, function (reason) {
            LoadingData(false);
        });
    };
    $scope.findBooksByGenre = function (gid) {
        $scope.books = [];
        if (!gid) return;
        LoadingData(true);
        var promise = apiService.searchForBooksByGenre(gid, $scope.language.LANG, $scope.isHideDeleted);
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


    //AID, BID, TITLE, SERIE_NAME, SERIE_NUMBER, GENRE, FILE, EXT, DEL, LANG, SIZE, DATE, LIBRATE, KEYWORDS, PATH
    $scope.gridOptions = {
        enableSorting: false,
        enableColumnResizing: true,
        enableFiltering: false,
        showTreeExpandNoChildren: false,
        enableRowSelection: true,
        enableRowHeaderSelection: false,
        enableSelectAll: false,
        multiSelect: false,
        noUnselect: true,
        modifierKeysToMultiSelect: false,
        showGridFooter: true,
        columnDefs: [
            {name: 'name', width: '40%', field: "TITLE", enableColumnMenu: false},
            {name: '#', width: '2%', field: "SERIE_NUMBER", enableColumnMenu: false},
            {name: 'size', width: '7%', field: "SIZE", enableColumnMenu: false},
            {name: 'lng.', width: '5%', field: "LANG", enableColumnMenu: false},
            {name: 'date', width: '10%', field: "DATE", enableColumnMenu: false},
            {name: 'genre', width: '*', field: "GENRE", enableColumnMenu: false}
        ],
        onRegisterApi: function (gridApi) {
            $scope.gridApi = gridApi;
            gridApi.selection.on.rowSelectionChanged($scope, function (row) {
                $scope.selectedBook = {book: null, url: null};
                if (row) {
                    $rootScope.safeApply(function () {
                        $scope.selectedBook.book = row.entity;

                    });

                }

            });
        }
    };

    $scope.gridOptions.isRowSelectable = function (row) {
        if (!row.entity.type) {
            return true;
        } else {
            return false;
        }
    };


    $scope.download = function () {
        $scope.selectedBook.downloading = true;
        var filename = $scope.selectedBook.book.FILE + "."
            + $scope.selectedBook.book.EXT + ".zip";
        var promise = apiService.getDownloadLink($scope.selectedBook.book.BID, $scope.selectedBook.book.PATH, filename);
        promise.then(function (response) {
            var data = new Blob([response], {type: "application/zip"});
            FileSaver.saveAs(data, filename);
            $scope.selectedBook.downloading = false;
        });


    };
});
