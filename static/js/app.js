angular.module( 'linkerApp', [],
    function( $interpolateProvider ){
        $interpolateProvider.startSymbol( '[[' );
        $interpolateProvider.endSymbol( ']]' );
    })

.directive( 'ngEnter', function () {
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

.controller( 'allGroupsCtrl', function( $http, $scope, $timeout ){
    $scope.isCreateShown = false;
    $scope.isAutocompleteShown = false;
    $scope.suggestions = [];
    $scope.invited = [];
    $scope.invitedMails = [];
    $scope._invited = "";

    $scope.showCreate = function(){
        $scope.isCreateShown = true;
    }

    $scope.addUser = function( id ){
    }

    $scope.removeUser = function( id ){
        console.log( 'remove' + id );
        $scope.invited.splice( id, 1 );
        $scope.invitedMails.splice( id, 1 );
        $scope._invited = $scope.invitedMails.toString();
    }

    $scope.updateAutocomplete = function(){
        if( $scope.nameStart.length < 3 ){
            $scope.suggestions = [];
            $scope.isAutocompleteShown = false;
        } else {
            console.log( 'try' );
            $http.post( '/user/autocomplete', { 'name_start' : $scope.nameStart } )
                .success( function( data ){
                    $scope.suggestions = data.users;
                    $scope.isAutocompleteShown = true;
                });
        }
    }

    $scope.autocompleteClick = function( id ){
        // var temp = $scope.suggestions[ id ];
        // if( $scope._invited.indexOf( temp ) == -1 ){
        //     $scope.invited.push( temp.name );
        //     $scope._invited.push( temp );
        // } else {
        //     console.log( 'duplicate' );
        // }

        var item = $scope.suggestions[ id ];
        if( $scope.invited.indexOf( item ) == -1 ){
            $scope.invited.push( item );
            $scope.invitedMails.push( item.email );
            $scope._invited = $scope.invitedMails.toString();
        }

        $scope.nameStart = "";
        $scope.suggestions = [];
        $scope.isAutocompleteShown = false;
    }
} )

.controller( 'groupCtrl', function( $http, $scope, $timeout ){

})
