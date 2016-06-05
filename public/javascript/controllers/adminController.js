"use strict";
main_app.controller("adminController", function ($scope, $filter, $rootScope, $location, apiService, ngTableParams) {
    var data = [];
    $scope.roles = [];
    $scope.modules = [];
    $scope.userForm = {
        role: "",
        modules: []
    };

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

    $scope.saveUser = function () {
        if (!$scope.userForm || !$scope.userForm.role) return;
        if (!$scope.userForm.uid) {
            apiService.addNewUser($scope.userForm).then(function (response) {
                if (response && !response.error) {
                    getAllUsers();
                    $scope.userForm = {
                        role: "",
                        modules: []
                    };
                }
            });
        } else if ($scope.userForm.uid) {
            apiService.updateUser($scope.userForm.uid, $scope.userForm).then(function (response) {
                if (response && !response.error) {
                    getAllUsers();
                    $scope.userForm = {
                        role: "",
                        modules: []
                    };
                }
            });
        }

    };
    $scope.editUser = function (uid) {
        apiService.getUser(uid).then(function (response) {
            if (response && !response.error) {
                $scope.userForm = response;
            }
        });
    };

    $scope.deleteUser = function (uid) {
        apiService.deleteUser(uid).then(function (response) {
            if (response && !response.error) {
                getAllUsers();
            }
        });
    };

    var getAllUsers = function () {
        apiService.getAllUsers().then(function (result) {
            if (result && !result.error) {
                data = result.users;
                $scope.tableParams.page(1);
                $scope.tableParams.reload();
            }
        });
    };
    $scope.init = function () {
        getAllUsers();

        apiService.getAllModules().then(function (response) {
            if (response && !response.error) {
                $scope.modules = response.result;
            }
        });
        apiService.getConstant("user_role").then(function (response) {
            if (response && !response.error) {
                $scope.roles = response.result;
            }
        });
    };

    $scope.init();

    $scope.cancel = function () {
        $scope.userForm = {
            role: "",
            modules: []
        };
    }

});
