"""Module containing utility functions"""
import base64
import hashlib
import random
import re
import string

from datetime   import datetime
from math       import *


def hashfunc( str ):
    """Returns a hash value of a given string

    Takes a string and returns its SHA512 hash value, encoded in base64
    """
    return base64.b64encode( hashlib.sha512( str.encode() ).digest() ).decode( 'ascii' )

def markup_to_html( str ):
    """Transforms a simple markup string into html

    Supported are: bold as '**bold part**' and italic as '*italicized part*'
    """
    str = re.sub( r'\*\*(.*?)\*\*', r'<b>\1</b>', str )
    str = re.sub( r'\*(.*?)\*', r'<i>\1</i>', str )
    return str

def pretty_date( time = False ):
    """Returns a string containing a human-readable date

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

def random_string( len ):
    """Returns a random string of a given length
    """
    return ''.join( [ random.choice( string.ascii_letters + string.digits + '$%' )
                      for _ in range( 0, len ) ] )

def shorten_array( a, n ):
    """Shortens a given array to at most n elements, appending the number of elements that were cut off
    """
    return a[ :n ] + ( [ str( len( a ) - n ) + ' others' ] if len( a ) > n else [] )
