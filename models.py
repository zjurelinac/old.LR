from peewee     import *
from datetime   import datetime
from run        import db


# Helper classes
class AuthorizationError( Exception ):
    pass

class MetaModel( Model ):
    database = db


class User( MetaModel ):
    name = CharField()
    email = CharField( unique = True )
    password = CharField()


class Group( MetaModel ):
    name = CharField( unique = True )
    owner = ForeignKeyField( User, related_name = 'owned_groups' )

    def getLastActivity( self ):
        q = self.links.select().order_by( Link.date.desc() )
        return q.get().date if q.count() > 0 else datetime.min


class Link( MetaModel ):
    url = CharField()
    description = TextField()
    owner = ForeignKeyField( User, related_name = 'shared_links' )
    date = DateTimeField( default = datetime.now() )
    group = ForeignKeyField( Group, related_name = 'links' )


class UserToGroup( MetaModel ):
    user = ForeignKeyField( User, related_name = 'group_rels' )
    group = ForeignKeyField( Group, related_name = 'user_rels' )

    class Meta:
        primary_key = CompositeKey( 'user', 'group' )
