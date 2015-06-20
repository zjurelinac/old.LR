from flask      import  abort, flash, g, jsonify, redirect, render_template, request, session, url_for
from models     import  *
from peewee     import  IntegrityError, DoesNotExist
from run        import  app
from utils      import  hashfunc, pretty_date


# Request handling
@app.before_request
def set_user():
    if session.get( 'logged_in' ):
        g.user = User.get( email = session[ 'user' ] )
    else:
        g.user = None

@app.after_request
def add_header( response ):
    # """
    # Add headers to both force latest IE rendering engine or Chrome Frame,
    # and also to cache the rendered page for 10 minutes.
    # """
    # response.headers[ 'X-UA-Compatible' ] = 'IE=Edge,chrome=1'
    # response.headers[ 'Last-Modified' ] = datetime.now()
    # response.headers[ 'Cache-Control' ] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    # response.headers[ 'Pragma' ] = 'no-cache'
    # response.headers[ 'Expires' ] = '-1'
    return response


# Template helpers
@app.template_filter( 'prettify' )
def prettify( s ):
    return pretty_date( s )


# User routes
@app.route( '/' )
def show_landing():
    return render_template( 'landing.html' )

@app.route( '/user/login', methods = [ 'GET' ] )
def show_login():
    return 'login form'

@app.route( '/user/login', methods = [ 'POST' ] )
def process_login():
    email = request.form.get( 'email' )
    password = request.form.get( 'password' )
    try:
        u = User.authenticate( email, password )
        session[ 'logged_in' ] = True
        session[ 'user' ] = u.email
        return redirect( '/groups' )
    except Exception as e:
        return 'failed ' + str( e )

@app.route( '/user/register', methods = [ 'GET' ] )
def show_register():
    pass

@app.route( '/user/register', methods = [ 'POST' ] )
def process_register():
    pass

@app.route( '/user/settings', methods = [ 'GET' ] )
def show_settings():
    pass

@app.route( '/user/change-password', methods = [ 'POST' ] )
def change_password():
    pass

@app.route( '/user/delete', methods = [ 'POST' ] )
def delete_account():
    pass

@app.route( '/user/signout', methods = [ 'GET' ] )
def signout():
    session.clear()
    return redirect( '/' )


# Group routes
@app.route( '/groups', methods = [ 'GET' ] )
def show_groups():
    user = g.get( 'user', None );
    return render_template( 'groups.html', user = user, groups = Group.all( user ) )

@app.route( '/groups', methods = [ 'POST' ] )
def create_group():
    pass

@app.route( '/groups/<int:gid>', methods = [ 'GET' ] )
def show_group( gid ):
    return render_template( 'group.html', user = g.get( 'user', None ) )

@app.route( '/groups/<int:gid>/delete', methods = [ 'POST' ] )
def delete_group( gid ):
    pass


# Link routes
@app.route( '/groups/<int:gid>/links', methods = [ 'POST' ] )
def add_link( gid ):
    pass

@app.route( '/groups/<int:gid>/links/<int:lid>/delete', methods = [ 'POST' ] )
def delete_link( gid, lid ):
    pass

@app.route( '/groups/<int:gid>/links/<int:lid>/mark-seen', methods = [ 'POST' ] )
def mark_as_seen( gid, lid ):
    pass


# Comment routes
@app.route( '/groups/<int:gid>/links/<int:lid>/comments', methods = [ 'POST' ] )
def add_comment( gid, lid ):
    pass

@app.route( '/groups/<int:gid>/links/<int:lid>/comments/<int:cid>', methods = [ 'POST' ] )
def delete_comment( gid, lid, cid ):
    pass


# Error handling
@app.errorhandler( 404 )
def error404( e ):
    return render_template( '404.html' ), 404

@app.errorhandler( 500 )
def error500( e ):
    return render_template( '500.html', error = e.description ), 500
