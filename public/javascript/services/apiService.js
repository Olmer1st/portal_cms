"use strict";
main_app.service('apiService', function ($http, $q) {
    var ROOT = "/api/v1/";
    this.searchForAuthor = function (searchParam) {
        return getMethod("library/authors/search/" + searchParam);
    };

    this.searchForBooksByAuthor = function (aid) {
        return getMethod("library/books/byauthor/" + aid);
    };

    this.LoginToTheSystem = function (email, password) {
        return postMethod("public/authenticate",{email:email, password:password});
    };


    this.getAllUsers = function () {
        return getMethod("admin/users");
    };

    function getMethod(query) {
        var dfd = $q.defer();
        //console.log('get', ROOT + query);
        $http.get(ROOT + query).success(function (data) {
            dfd.resolve(data);
        }).error(function (err) {
            dfd.reject(err);
        });


        return dfd.promise;
    };

    function postMethod(query, param) {
        var dfd = $q.defer();
        $http.post(ROOT + query, param).success(function (data) {
            dfd.resolve(data);
        }).error(function (err) {
            dfd.reject(err);
        });
        return dfd.promise;
    };

    function deleteMethod(query) {
        var dfd = $q.defer();

        $http.delete(ROOT + query).success(function (data) {
            dfd.resolve(data);
        }).error(function (err) {
            dfd.reject(err);
        });

        return dfd.promise;
    };

    function putMethod(query, param) {
        var dfd = $q.defer();
        if (param) {
            $http.put(ROOT + query, param).success(function (data) {
                dfd.resolve(data);
            }).error(function (err) {
                dfd.reject(err);
            });
        } else {
            $http.put(ROOT + query).success(function (data) {
                dfd.resolve(data);
            }).error(function (err) {
                dfd.reject(err);
            });
        }

        return dfd.promise;
    };

});