
main_app.service('principal', function($http, $cookieStore, $rootScope, apiService) {

    this.Login = function(email, password, callback) {
        var promise = apiService.LoginToTheSystem(email, password);
        promise.then(function(response){
             callback(response);
        }, function(reason){
            
        });

    };

    this.SetCredentials = function(response) {
        if (response) {
            if(!$rootScope.GLOBALS) $rootScope.GLOBALS={};
            $rootScope.GLOBALS["currentUser"] =  {
                    email: response.email,
                    role: response.role,
                    modules: response.modules,
                    display: response.display,
                    uid: response.uid,
                    token: response.token
                };
            $http.defaults.headers.common['x-access-token'] = response.token;
            $cookieStore.put('portalUserSession', $rootScope.GLOBALS.currentUser);
        }



    };

    this.ClearCredentials = function() {
        if($rootScope.GLOBALS) $rootScope.GLOBALS.currentUser = null;
        $cookieStore.remove('portalUserSession');
        $http.defaults.headers.common['x-access-token'] = '';
    };

});