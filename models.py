from peewee     import *
from datetime   import datetime
from run        import db
from utils      import hashfunc, shorten_array

import peewee
import re

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
        if not name or len( name ) < 3 or len( name ) > 128:
            raise ValueError( 'Name too short or too long' )
        elif not email or not re.match( r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email ):
            raise ValueError( 'Wrong email format' )
        elif not password or len( password ) < 8:
            raise ValueError( 'Password too short' )

        try:
            u = cls( name = name, email = email, password = hashfunc( password ) )
            u.save()
            return u
        except IntegrityError:
            raise ValueError( 'This email is already in use' )


    @classmethod
    def authenticate( cls, email, password ):
        try:
            u = cls.get( email = email )
        except DoesNotExist:
            raise ValueError( 'No user with a given email' )

        if u.password != hashfunc( password ):
            raise ValueError( 'Passwords do not match' )

        return u

    @classmethod
    def delete( cls, email, password ):
        pass

    @classmethod
    def autocomplete( cls, query ):
        if not query or len( query ) < 3:
            raise ValueError( 'Query too short' )

        return [ { 'id' : x.id, 'name' : x.name, 'email' : x.email }
            for x in cls.select().where( User.name ** ( '%' + query + '%' ) ) ]

    def change_password( self, old, new ):
        if self.password != hashfunc( old ):
            raise ValueError( 'Passwords do not match' )
        if len( new ) < 8:
            raise ValueError( 'New password too short' )

        self.password = hashfunc( new )
        self.save()

class Group( MetaModel ):
    name = CharField()
    description = TextField()
    owner = ForeignKeyField( User, related_name = 'owned_groups' )

    @classmethod
    def new( cls, name, descr, owner ):
        if not name:
            raise ValueError( 'Incorrect name' )
        elif Group.select().where( Group.owner == owner and Group.name == name ).exists():
            raise ValueError( 'This group name already in use' )

        g = cls( name = name, description = descr, owner = owner )
        g.save()
        return g

    @classmethod
    def get( cls, id, user ):
        pass

    @classmethod
    def all( cls, user ):
        return [ {
            'id' : g.id,
            'name' : g.name,
            'descr' : g.description,
            'owner' : g.owner.name,
            'users' : shorten_array( [ x.user.name for x in g.user_rels ], 5 ) }
        for g in cls.select().where( Group.owner == user ) ]


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
