angular.module( 'linkerApp', [],
    function( $interpolateProvider ){
        $interpolateProvider.startSymbol( '[[' );
        $interpolateProvider.endSymbol( ']]' );
    })

.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
})

.controller( 'indexCtrl', function( $scope, $http ){
    $scope.popup = false;
    $scope.inviteUser = "";
    $scope.autocompletes = [];
    $scope.invitedUsers = [];
    $scope._invitedUsers = "Hello";

    $scope.autoCompleteUser = function(){
        if( $scope.inviteUser.length < 3 ){
            autocompletes = [];
            return;
        }

        $http.post( '/user-ac', { hello : "World", nameStart : $scope.inviteUser } )
            .success( function( data ){
                $scope.autocompletes = data.users;
            } )
    };

    $scope.autocompleteClick = function( id ){
        $scope.invitedUsers.push( $scope.autocompletes[ id ].name );
        $scope._invitedUsers = $scope.invitedUsers.toString();

        $scope.inviteUser = "";
        $scope.autocompletes = [];
    };

    $scope.enterUser = function(){
        $scope.invitedUsers.push( $scope.inviteUser );
        $scope._invitedUsers = $scope.invitedUsers.toString();

        $scope.inviteUser = "";
        $scope.autocompletes = [];
    };

    $scope.removeUser = function( id ){
        $scope.invitedUsers.splice( id, 1 );
        $scope._invitedUsers = $scope.invitedUsers.toString();
    };
})

.controller( 'groupCtrl', function( $scope, $timeout ){
    $scope.popup = false;
    $scope.hideInfos = false;

    clearInfos = function(){
        $scope.hideInfos = true;
        console.log( $scope.hideInfos )
    }

    $timeout( clearInfos, 3000 );
});
