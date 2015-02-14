import string
import random
import hashlib
import base64


def hashfunc( str ):
    return base64.b85encode( hashlib.sha512( str.encode() ).digest() ).decode( 'ascii' )


def random_string( len ):
    return ''.join( [ random.choice( string.ascii_letters + string.digits + '$%' )
                      for _ in range( 0, len ) ] )
