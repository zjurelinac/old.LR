from flask      import  flash, jsonify, redirect, render_template, request, session, url_for
from models     import  *
from peewee     import  IntegrityError, DoesNotExist
from run        import  app
from utils      import  hashfunc


@app.errorhandler( 404 )
def error404( e ):
    return render_template( '404.html' ), 404

@app.errorhandler( 500 )
def error500( e ):
    return render_template( '500.html', error = e ), 500




@app.route( '/' )
def index():
    if( 'logged_in' in session ):
        user = User.get( User.email == session.get( 'email' ) )
        groups = [ { 'id'           : r.group.id,
                     'name'         : r.group.name,
                     'links_count'  : r.group.links.count(),
                     'users'        : [ rr.user.name for rr in r.group.user_rels.select() ],
                     'users_count'  : r.group.user_rels.count()}
                     #'last_activity': r.group.links.select().order_by( Link.date.desc() ).get() }
                 for r in user.group_rels.select() ]

        return render_template( 'index.html', user = { 'name' : session[ 'name' ],
                                                       'email' : session[ 'email' ] },
                                              groups = groups )

    else:
        return redirect( url_for( 'showLogin' ) )


@app.route( '/signup', methods = [ 'GET' ] )
def showSignup():
    if( 'logged_in' in session ):
        return redirect( url_for( 'index' ) )

    return render_template( 'signup.html' )


@app.route( '/signup', methods = [ 'POST' ] )
def processSignup():
    name    = request.form.get( 'name' )
    email   = request.form.get( 'email' )
    pass1   = request.form.get( 'password' )
    pass2   = request.form.get( 'password-repeat' )

    if pass1 != pass2:
        flash( 'Passwords do not match.', 'error' )
        return redirect( url_for( 'showSignup' ) )

    if not name or not email or not pass1 or not pass2:
        flash( 'Please provide all the data.', 'error' )
        return redirect( url_for( 'showSignup' ) )

    try:
        user = User( name = name, email = email, password = hashfunc( pass1 ) )
        user.save()
    except IntegrityError:
        flash( 'Given email already in use.' )
        return redirect( url_for( 'showSignup' ) )

    flash( 'Successfully signed up.', 'info' )
    return redirect( url_for( 'index' ) )


@app.route( '/login', methods = [ 'GET' ] )
def showLogin():
    if( 'logged_in' in session ):
        return redirect( url_for( 'index' ) )

    return render_template( 'login.html' )


@app.route( '/login', methods = [ 'POST' ] )
def processLogin():
    email   = request.form.get( 'email' )
    passwd  = request.form.get( 'password' )

    if not email or not passwd:
        flash( 'Please enter all the data.', 'error' )
        return redirect( url_for( 'showLogin' ) )

    try:
        user = User.get( User.email == email )
    except User.DoesNotExist:
        flash( 'Wrong email address' )
        return redirect( url_for( 'showLogin' ) )

    if user.password != hashfunc( passwd ):
        flash( 'Wrong password', 'error' )
        return redirect( url_for( 'showLogin' ) )

    session[ 'logged_in' ]  = True
    session[ 'name' ]       = user.name
    session[ 'email' ]      = user.email
    session[ 'user_id' ]    = user.id

    return redirect( url_for( 'index' ) )


@app.route( '/signout', methods = [ 'GET' ] )
def signout():
    session.clear()
    return redirect( url_for( 'index' ) )


@app.route( '/user-ac', methods = [ 'POST' ] )
def autocompleteUser():
    if 'logged_in' not in session:
        return jsonify( message = "Error" ), 404

    start = request.json.get( 'nameStart' )

    if not start:
        return jsonify( message = "Error" ), 500

    possible = []
    for u in User.select().where( User.name.startswith( start ) ):
        possible.append( { 'name' : u.name, 'email' : u.email } )

    return jsonify( users = possible )



@app.route( '/group/<int:id>', methods = [ 'GET' ] )
def showGroup( id ):
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    user    = User.get( User.id == session[ 'user_id' ] )
    group   = Group.get( Group.id == id )


    if group not in [ r.group for r in user.group_rels.select() ]:
        return "unauthorized"

    g = { 'name' : group.name,
          'id' : group.id,
          'users' : [ u.user for u in group.user_rels.select() ],
          'links' : [ l for l in group.links.select() ] }

    return render_template( 'group.html', user = user, group = g )


@app.route( '/group', methods = [ 'POST' ] )
def createGroup():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    name        = request.form.get( 'group-name' )
    users_str   = request.form.get( 'users-list' )

    if not name or not users_str:
        flash( 'Please enter all the required data.', 'error' )
        return redirect( url_for( 'index' ) )

    owner       = User.get( User.id == session[ 'user_id' ] )

    users       = [ User.get( User.name == u ) for u in users_str.split( ',' ) ]
    group       = Group( name = name, owner = owner )
    group.save()

    for u in users:
        UserToGroup.create( user = u, group = group )

    UserToGroup.create( user = owner, group = group )

    return redirect( '/group' )



@app.route( '/link', methods = [ 'POST' ] )
def shareLink():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    user = User.get( User.id == session[ 'user_id' ] )

    group_id    = request.form.get( 'group-id' )
    link_url    = request.form.get( 'link-url' )
    link_descr  = request.form.get( 'link-descr' )

    if not link_url:
        flash( 'Please provide the url.', 'error' )
        return redirect( "/group/" + group_id )

    return "Hi " + link_url
