from peewee     import *
from datetime   import datetime
from run        import db


# Helper classes
class AuthorizationError( Exception ):
    pass


class MetaModel( Model ):
    class Meta:
        database = db


class User( MetaModel ):
    name = CharField()
    email = CharField( unique = True )
    password = CharField()

    @classmethod
    def register( cls, name, email, password ):
        pass

    @classmethod
    def authenticate( cls, email, password ):
        pass

    @classmethod
    def delete( cls, email, password ):
        pass

    @classmethod
    def autocomplete( cls, name ):
        pass

    def change_password( old, new ):
        pass


class Group( MetaModel ):
    name = CharField( unique = True )
    description = TextField()
    owner = ForeignKeyField( User, related_name = 'owned_groups' )

    @classmethod
    def create( cls, name, owner ):
        pass

    @classmethod
    def get( cls, id, user ):
        pass

    @classmethod
    def invite_user( cls, id, owner, user ):
        pass

    @classmethod
    def remove_user( cls, id, owner, user ):
        pass

    @classmethod
    def change( cls, id, name, descr, owner ):
        pass

    @classmethod
    def delete( cls, id, owner ):
        pass

    # def get_last_activity( self ):
    #     q = self.links.select().order_by( Link.date.desc() )
    #     return q.get().date if q.count() > 0 else datetime.min


class Link( MetaModel ):
    url = CharField()
    description = TextField()
    owner = ForeignKeyField( User, related_name = 'shared_links' )
    date = DateTimeField()
    group = ForeignKeyField( Group, related_name = 'links' )

    @classmethod
    def add( cls, url, descr, owner, group_id ):
        pass

    @classmethod
    def delete( cls, id, group_id, user ):
        pass

    @classmethod
    def mark_seen( cls, id, user ):
        pass


class Comment( MetaModel ):
    content = TextField()
    date = DateTimeField()
    link = ForeignKeyField( Link, related_name = 'comments' )
    owner = ForeignKeyField( User, related_name = 'comments' )

    @classmethod
    def create( cls, content, link, owner ):
        pass

    @classmethod
    def delete( cls, id, user ):
        pass


class UserToGroup( MetaModel ):
    user = ForeignKeyField( User, related_name = 'group_rels' )
    group = ForeignKeyField( Group, related_name = 'user_rels' )

    class Meta:
        primary_key = CompositeKey( 'user', 'group' )


class UserToLink( MetaModel ):
    user = ForeignKeyField( User, related_name = 'seen_rels' )
    link = ForeignKeyField( Link, related_name = 'user_rels' )

    class Meta:
        primary_key = CompositeKey( 'user', 'link' )
