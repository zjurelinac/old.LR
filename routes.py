from flask      import  abort, flash, jsonify, redirect, render_template, request, session, url_for
from models     import  *
from peewee     import  IntegrityError, DoesNotExist
from run        import  app
from utils      import  hashfunc, pretty_date


@app.errorhandler( 404 )
def error404( e ):
    return render_template( '404.html' ), 404

@app.errorhandler( 500 )
def error500( e ):
    return render_template( '500.html', error = e.description ), 500

@app.template_filter( 'prettify' )
def prettify( s ):
    return pretty_date( s )

@app.after_request
def add_header( response ):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers[ 'X-UA-Compatible' ] = 'IE=Edge,chrome=1'
    response.headers[ 'Last-Modified' ] = datetime.now()
    response.headers[ 'Cache-Control' ] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers[ 'Pragma' ] = 'no-cache'
    response.headers[ 'Expires' ] = '-1'
    return response



@app.route( '/' )
def index():
    if( 'logged_in' in session ):
        user = User.get( User.email == session.get( 'email' ) )
        groups = [ { 'id'           : r.group.id,
                     'name'         : r.group.name,
                     'links_count'  : r.group.links.count(),
                     'users'        : [ rr.user.name for rr in r.group.user_rels.select() ],
                     'users_count'  : r.group.user_rels.count(),
                     'last_activity': r.group.getLastActivity() }
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
        flash( 'Given email already in use.', 'error' )
        return redirect( url_for( 'showSignup' ) )

    flash( 'Successfully signed up.', 'success' )
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
        flash( 'Wrong email address', 'error' )
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


@app.route( '/user/suggest', methods = [ 'POST' ] )
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


@app.route( '/user/change-password', methods = [ 'GET' ] )
def showChangePassword():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )
    return render_template( 'change_password.html', user = { 'name' : session[ 'name' ],
                                                             'email' : session[ 'email' ] } )


@app.route( '/user/change-password', methods = [ 'POST' ] )
def changePassword():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    oldpass     = request.form.get( 'old-password' )
    newpass1    = request.form.get( 'new-password' )
    newpass2    = request.form.get( 'new-password-repeat' )

    if not oldpass or not newpass1 or not newpass2:
        flash( 'Please provide all the data', 'error' )
        return redirect( url_for( 'showChangePassword' ) )

    user = User.get( User.id == session[ 'user_id' ] )

    if user.password != hashfunc( oldpass ):
        flash( 'The password you entered does not match your old password.', 'error' )
        return redirect( url_for( 'showChangePassword' ) )

    if newpass1 != newpass2:
        flash( 'The new passwords do not match.', 'error' )
        return redirect( url_for( 'showChangePassword' ) )

    user.password = hashfunc( newpass1 )
    user.save()
    flash( 'Password successfully changed.', 'success' )

    return redirect( '/' )


@app.route( '/user/delete', methods = [ 'GET' ] )
def showDeleteUser():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )
    return render_template( 'delete_account.html', user = { 'name' : session[ 'name' ],
                                                            'email' : session[ 'email' ] } )
@app.route( '/user/delete', methods = [ 'POST' ] )
def deleteUser():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )



@app.route( '/group/<int:id>', methods = [ 'GET' ] )
def showGroup( id ):
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    user    = User.get( User.id == session[ 'user_id' ] )

    try:
        group   = Group.get( Group.id == id )
    except Group.DoesNotExist:
        abort( 500, { 'message' : 'Group does not exist.' } )


    if group not in [ r.group for r in user.group_rels.select() ]:
        return "unauthorized"

    g = { 'name'    : group.name,
          'id'      : group.id,
          'users'   : [ u.user for u in group.user_rels.select() ],
          'links'   : [ l for l in group.links.select().order_by( Link.date.desc() ) ],
          'isOwner' : group.owner == user }

    return render_template( 'group.html', user = user, group = g )


@app.route( '/group', methods = [ 'POST' ] )
def createGroup():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    name        = request.form.get( 'group-name' )
    users_str   = request.form.get( 'users-list' )

    if not name:
        flash( 'Please choose the name of the new group.', 'error' )
        return redirect( url_for( 'index' ) )

    owner       = User.get( User.id == session[ 'user_id' ] )

    group       = Group( name = name, owner = owner )
    group.save()

    if users_str:
        users       = [ User.get( User.name == u ) for u in users_str.split( ',' ) ]

        for u in users:
            UserToGroup.create( user = u, group = group )

    UserToGroup.create( user = owner, group = group )

    return redirect( '/group/' + str( group.id ) )


@app.route( '/group/invite', methods = [ 'POST' ] )
def inviteUsers():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    group_id    = request.form.get( 'group-id' )
    users_str   = request.form.get( 'users-list' )

    if not group_id:
        flash( 'Wrong group id.', 'error' )
        return redirect( url_for( 'index' ) )

    if not users_str:
        flash( 'Please enter all the required data.', 'error' )
        return redirect( url_for( '/group/' + str( group_id ) ) )

    owner       = User.get( User.id == session[ 'user_id' ] )

    try:
        group   = Group.get( Group.id == group_id )
    except Group.DoesNotExist:
        flash( 'Please enter all the required data.', 'error' )
        return redirect( url_for( 'index' ) )

    users = [ User.get( User.name == u ) for u in users_str.split( ',' ) ]

    for u in users:
        UserToGroup.create( user = u, group = group )

    return redirect( '/group/' + str( group_id ) )


@app.route( '/group/delete/<int:id>', methods = [ 'GET' ] )
def deleteGroup( id ):
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    user = User.get( User.id == session[ 'user_id' ] )

    try:
        group = Group.get( Group.id == id )
    except Group.DoesNotExist:
        abort( 500, { 'message' : 'Group does not exist.' } )




@app.route( '/link', methods = [ 'POST' ] )
def shareLink():
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    user = User.get( User.id == session[ 'user_id' ] )

    group_id    = request.form.get( 'group-id' )
    link_url    = request.form.get( 'link-url' )
    link_descr  = request.form.get( 'link-descr' )

    if not link_url:
        flash( 'Please provide the URL of the link you\'d like to share.', 'error' )
        return redirect( "/group/" + group_id )

    try:
        group = Group.get( Group.id == group_id )
    except Group.DoesNotExist:
        flash( 'Cannot share a link, it\'s group does not exist.', 'error' )
        return redirect( "/group/" + group_id )

    Link.create( owner = user, group = group, url = link_url, description = link_descr, date = datetime.now() )
    return redirect( "/group/" + group_id )


@app.route( '/link/delete/<int:id>' )
def deleteLink( id ):
    if 'logged_in' not in session:
        return redirect( url_for( 'login' ) )

    try:
        link = Link.get( Link.id == id )
    except Link.DoesNotExist:
        flash( 'Link with a given id does not exist', 'error' )
        return redirect( '/index' )

    user = User.get( User.id == session[ 'user_id' ] )

    if link.owner != user and link.group.owner != user:
        return 'Unauthorized'

    gid = link.group.id

    link.delete_instance()

    return redirect( '/group/' + str( gid ) )


