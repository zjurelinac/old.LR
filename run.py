from app    import app, db
from routes import *
from models import *

if __name__ == '__main__':
    db.create_tables( [ User, Group, Link, Comment, UserToGroup, UserToLink ], safe = True )
    app.run()
