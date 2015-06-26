angular.module( 'linkerApp', [],
    function( $interpolateProvider ){
        $interpolateProvider.startSymbol( '[[' );
        $interpolateProvider.endSymbol( ']]' );
    })

.directive( 'ngEnter', function () {
    return function ( scope, element, attrs ) {
        element.bind("keydown keypress", function( event ) {
            if( event.which === 13 ) {
                scope.$apply( function(){
                    scope.$eval( attrs.ngEnter );
                });

                event.preventDefault();
            }
        });
    };
})

.controller( 'allGroupsCtrl', function( $http, $scope, $timeout ){
    $scope.hideErrors = false;
    $scope.isCreateShown = false;
    $scope.isAutocompleteShown = false;
    $scope.suggestions = [];
    $scope.invited = [];
    $scope.invitedMails = [];
    $scope._invited = "";
    $scope.selectionIndex = -1;

    var alreadySelected = function( item ){
        console.log( 'testing ', item, $scope.invited );
        for( var i = 0; i < $scope.invited.length; ++i )
            if( $scope.invited[ i ].email == item.email )
                return true;
        return false;
    }

    $scope.showCreate = function(){
        $scope.isCreateShown = true;
        $scope.hideErrors = true;
    }

    $scope.hideCreate = function(){
        $scope.isCreateShown = false;
    }

    $scope.updateSelection = function( e ){
        if( e.keyCode == 40 && $scope.selectionIndex < $scope.suggestions.length-1 ){
            e.preventDefault();
            ++$scope.selectionIndex;
        } else if( e.keyCode == 38 && $scope.selectionIndex >= 0 ){
            e.preventDefault();
            --$scope.selectionIndex;
        }
    }

    $scope.addUser = function(){
        if( $scope.selectionIndex < 0 ) return;

        var item = $scope.suggestions[ $scope.selectionIndex ];
        if( !alreadySelected( item ) ){
            $scope.invited.push( item );
            $scope.invitedMails.push( item.email );
            $scope._invited = $scope.invitedMails.toString();
        }

        $scope.nameStart = "";
        $scope.suggestions = [];
        $scope.isAutocompleteShown = false;
        $scope.selectionIndex = -1;
    }

    $scope.removeUser = function( id ){
        $scope.invited.splice( id, 1 );
        $scope.invitedMails.splice( id, 1 );
        $scope._invited = $scope.invitedMails.toString();
    }

    $scope.updateAutocomplete = function(){
        if( $scope.nameStart.length < 3 ){
            $scope.suggestions = [];
            $scope.isAutocompleteShown = false;
            $scope.selectionIndex = -1;
        } else {
            $http.post( '/user/autocomplete', { 'name_start' : $scope.nameStart } )
                .success( function( data ){
                    $scope.suggestions = data.users;
                    $scope.isAutocompleteShown = true;
                });
        }
    }

    $scope.autocompleteClick = function( id ){
        var item = $scope.suggestions[ id ];
        if( !alreadySelected( item ) ){
            $scope.invited.push( item );
            $scope.invitedMails.push( item.email );
            $scope._invited = $scope.invitedMails.toString();
        }

        $scope.nameStart = "";
        $scope.suggestions = [];
        $scope.isAutocompleteShown = false;
        $scope.selectionIndex = -1;
    }
} )

.controller( 'groupCtrl', function( $http, $scope, $timeout ){
    $scope.isShareShown = false;
    $scope.isInviteShown = false;
    $scope.isDeleteShown = false;
    $scope.isEditShown = false;

    $scope.showInvite = function(){
        $scope.isShareShown = false;
        $scope.isInviteShown = true;
        $scope.isDeleteShown = false;
        $scope.isEditShown = false;
    }

    $scope.showShare = function(){
        $scope.isShareShown = true;
        $scope.isInviteShown = false;
        $scope.isDeleteShown = false;
        $scope.isEditShown = false;
    }

    $scope.showDelete = function(){
        $scope.isShareShown = false;
        $scope.isInviteShown = false;
        $scope.isDeleteShown = true;
        $scope.isEditShown = false;
    }

    $scope.showEdit = function(){
        $scope.isShareShown = false;
        $scope.isInviteShown = false;
        $scope.isDeleteShown = false;
        $scope.isEditShown = true;
    }
})
