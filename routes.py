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

@app.template_filter( 'markupify' )
def markupify( s ):
    return s

# User routes
@app.route( '/' )
def show_landing():
    if session.get( 'logged_in' ):
        return redirect( '/groups' )
    return render_template( 'landing.html' )

@app.route( '/user/login', methods = [ 'GET' ] )
def show_login():
    if session.get( 'logged_in' ):
        return redirect( '/groups' )
    return render_template( 'login.html' )

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
        flash( str( e ) )
        return redirect( '/user/login' )

# @app.route( '/user/register', methods = [ 'GET' ] )
# def show_register():
#     pass

@app.route( '/user/register', methods = [ 'POST' ] )
def process_register():
    name = request.form.get( 'name' )
    email = request.form.get( 'email' )
    password = request.form.get( 'password' )
    password2 = request.form.get( 'password2' )

    try:
        u = User.register( name, email, password, password2 )
        session[ 'logged_in' ] = True
        session[ 'user' ] = u.email
        return redirect( '/groups' )
    except Exception as e:
        flash( str( e ), 'error' )
        return redirect( '/' )

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
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    user = g.get( 'user', None );
    return render_template( 'groups.html', user = user, groups = Group.get_all( user ) )

@app.route( '/groups', methods = [ 'POST' ] )
def create_group():
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass

@app.route( '/groups/<int:gid>', methods = [ 'GET' ] )
def show_group( gid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    user = g.get( 'user', None )
    return render_template( 'group.html', user = user, group = Group.get_dict( gid, user ) )

@app.route( '/groups/<int:gid>/delete', methods = [ 'POST' ] )
def delete_group( gid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass

@app.route( '/groups/<int:gid>/invite', methods = [ 'POST' ] )
def invite_to_group( gid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass


# Link routes
@app.route( '/groups/<int:gid>/links', methods = [ 'POST' ] )
def add_link( gid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass

@app.route( '/groups/<int:gid>/links/<int:lid>/delete', methods = [ 'POST' ] )
def delete_link( gid, lid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass

@app.route( '/groups/<int:gid>/links/<int:lid>/mark-seen', methods = [ 'POST' ] )
def mark_as_seen( gid, lid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass


# Comment routes
@app.route( '/groups/<int:gid>/links/<int:lid>/comments', methods = [ 'POST' ] )
def add_comment( gid, lid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass

@app.route( '/groups/<int:gid>/links/<int:lid>/comments/<int:cid>', methods = [ 'POST' ] )
def delete_comment( gid, lid, cid ):
    if not session.get( 'logged_in' ):
        flash( 'Not authorized to perform this action, login first.' )
        return redirect( '/user/login' )

    pass


# Error handling
@app.errorhandler( 404 )
def error404( e ):
    return render_template( '404.html' ), 404

@app.errorhandler( 500 )
def error500( e ):
    return render_template( '500.html', error = e.description ), 500
