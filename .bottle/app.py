from bottle import route, run

@route( '/' )
def index():
    return "Hello"


# User actions
@route( '/login' )
def login():
    pass


@route( '/signup' )
def signup():
    pass


# Group actions
@get( '/group/<group_id:int>' )
def group( id ):
    pass


@post( '/group' )
def addGroup():
    pass


@delete( '/group' )
def deleteGroup():
    pass


# Link actions
@post( '/link' )
def addLink():
    pass

@delete( '/link/<link_id:int>' )
def deleteLink( link_id ):
    pass





run( host = 'localhost', port = 8080, debug = True )
