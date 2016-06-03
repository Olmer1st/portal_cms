"use strict";
main_app.controller("adminController", function ($scope, $filter, $rootScope, $location, apiService, ngTableParams) {
    var data = [];
    // $scope.users = [];
    
    $scope.tableParams = new ngTableParams({
        page: 1, // show first page
        count: 10 // count per page
    }, {
        total: data.length, // length of data
        counts: [],
        getData: function ($defer, params) {
            var orderedData = params.filter() ? $filter('filter')(data, params.filter()) : data;
            params.total(orderedData.length);
            $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));

        }
    });
    
    
    $scope.init = function () {
        var promise = apiService.getAllUsers();
        promise.then(function (result) {
            if(result && !result.error){
                data = result.users;
                $scope.tableParams.page(1);
                $scope.tableParams.reload();
            }
        });
    };

    $scope.init();

});
