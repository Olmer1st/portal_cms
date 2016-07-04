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
    $scope.stateParam = null;
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
    $scope.refresh = function ($event) {
        //$event.stopPropagation();
        if (!$scope.stateParam) return;
        var button = $scope.buttons.find(function (item) {
            return item.active;
        });
        if (!button) return;
        switch (button.name) {
            case "library.authors":
                $scope.findBooksOfAuthor($scope.stateParam);
                break;
            case  "library.genres":
                $scope.findBooksByGenre($scope.stateParam);
                break;
            case "library.series":
                $scope.findBooksInSerie($scope.stateParam);
                break;
            case "library.search":
                break;
            default:
                break;
        }
    };
    
    
      $scope.findBooksbySearchForm = function (options) {
        $scope.stateParam = options;
        $scope.books = [];
        if (!options) return;
        LoadingData(true);
        var promise = apiService.searchForBooksByForm($scope.language.LANG, $scope.isHideDeleted,options);
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
    
    $scope.findBooksOfAuthor = function (aid, next) {
        $scope.stateParam = aid;
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
            if(next) next();
        }, function (reason) {
            LoadingData(false);
            if(next) next();
        });
    };

    $scope.findBooksInSerie = function (sid) {
        $scope.stateParam = sid;
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
        $scope.stateParam = gid;
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

    function rowTemplate() {
        return $timeout(function () {
            return '<div ng-class="{ \'grid-del-css-class\': row.entity.DEL}">' +
                '  <div ng-repeat="(colRenderIndex, col) in colContainer.renderedColumns track by col.colDef.name" class="ui-grid-cell" ng-class="{ \'ui-grid-row-header-cell\': col.isRowHeader }"  ui-grid-cell></div>' +
                '</div>';
        }, 0);
    }

    //AID, BID, TITLE, SERIE_NAME, SERIE_NUMBER, GENRE, FILE, EXT, DEL, LANG, SIZE, DATE, LIBRATE, KEYWORDS, PATH
    $scope.gridOptions = {
        enableSorting: false,
        enableColumnResizing: true,
        enableFiltering: false,
        showTreeExpandNoChildren: false,
        enableRowSelection: true,
        enableRowHeaderSelection: true,
        enableSelectAll: false,
        multiSelect: false,
        noUnselect: true,
        modifierKeysToMultiSelect: false,
        showGridFooter: true,
        rowTemplate: rowTemplate(),
        columnDefs: [
            {name: 'name', width: '40%', field: "TITLE", enableColumnMenu: false,cellTemplate: "<a ng-if='grid.appScope.checkIsShowUrl(row)' class='pointer' ng-click='grid.appScope.goToAuthor(row)'>{{row.entity.TITLE}}</a><span  ng-if='!grid.appScope.checkIsShowUrl(row)'>{{row.entity.TITLE}}</span>"},
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

    $scope.checkIsShowUrl = function(row){
        return row.entity.type=="author";
    };

    $scope.goToAuthor = function(row){
        $scope.findBooksOfAuthor(row.entity.AID, function () {
            var index;
            for(index=0;index<$scope.buttons.length;index++){
                var item = $scope.buttons[index];
                if(item.name == "library.authors") break;
            }
            $scope.executeState(index);
        });

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

        var book_file_name = ($scope.selectedBook.book.SERIE_NUMBER)?$scope.selectedBook.book.SERIE_NUMBER + ".":"";
        book_file_name = book_file_name + $scope.selectedBook.book.TITLE+ "." + $scope.selectedBook.book.EXT + ".zip";
        var promise = apiService.getDownloadLink($scope.selectedBook.book.BID, $scope.selectedBook.book.PATH, filename);
        promise.then(function (response) {
            var data = new Blob([response], {type: "application/zip"});
            FileSaver.saveAs(data, book_file_name);
            $scope.selectedBook.downloading = false;
        });


    };
});
