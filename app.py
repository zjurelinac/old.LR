from flask  import Flask
from peewee import *

import os

APP_ROOT = os.path.dirname( os.path.realpath( __file__ ) )
DATABASE = "linker.db"#os.path.join( APP_ROOT, 'linker.db' )
SECRET_KEY = "t!3pbh+o3zh9l3xtm!=5$+uy^7#7s7+aarxc=yb5v4!$b!o^77"
DEBUG = True

app = Flask( __name__ )
app.config.from_object( __name__ )
db = SqliteDatabase( app.config[ 'DATABASE' ], threadlocals = True )


