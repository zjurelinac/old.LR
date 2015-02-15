import base64
import hashlib
import random
import string

from datetime   import datetime
from math       import *


def hashfunc( str ):
    return base64.b85encode( hashlib.sha512( str.encode() ).digest() ).decode( 'ascii' )


def random_string( len ):
    return ''.join( [ random.choice( string.ascii_letters + string.digits + '$%' )
                      for _ in range( 0, len ) ] )

def pretty_date( time = False ):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """

    now = datetime.now()
    if isinstance( time, datetime ):
        diff = now - time
    else:
        return time

    if time == datetime.min:
        return "Never"

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str( second_diff ) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str( round( second_diff / 60 ) ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( round( second_diff / 3600 ) ) + " hours ago"

    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str( day_diff ) + " days ago"
    if day_diff < 31:
        return str( round( day_diff / 7 ) ) + " weeks ago"
    if day_diff < 365:
        return str( round( day_diff / 30 ) ) + " months ago"
    return str( round( day_diff / 365 ) ) + " years ago"
