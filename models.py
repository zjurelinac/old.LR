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
            raise ValueError( 'Email is already in use' )


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
            raise ValueError( 'Group name already in use' )

        g = cls( name = name, description = descr, owner = owner )
        g.save()
        return g

    @classmethod
    def get_single( cls, id, user ):
        group = cls.get( id = id )

        if group.is_group_member( user ):
            return {
                'id' : group.id,
                'name' : group.name,
                'descr' : group.description,
                'owner' : group.owner.name,
                'users' : shorten_array( [ x.user.name for x in group.user_rels ], 5 ) }
        else:
            raise AuthorizationError( 'Not allowed to see the group' )

    @classmethod
    def all( cls, user ):
        return [ {
            'id' : group.id,
            'name' : group.name,
            'descr' : group.description,
            'owner' : group.owner.name,
            'users' : shorten_array( [ x.user.name for x in group.user_rels ], 5 ),
            'links_count' : group.get_links_count( user ) }
        for group in list( cls.select().where( Group.owner == user ) ) + list( [ g.group for g in user.group_rels ] ) ]


    @classmethod
    def add_user( cls, id, owner, user ):
        group = Group.get( id = id )

        if user == owner:
            raise ValueError( 'Owner is always a group member' )

        if group.owner != owner:
            raise AuthorizationError( 'Not allowed to make changes to the group' )

        try:
            UserToGroup.create( user = user, group = group )
        except IntegrityError:
            raise ValueError( 'User is already in the group' )

    @classmethod
    def remove_user( cls, id, owner, user ):
        group = Group.get( id = id )

        if group.owner != owner:
            raise AuthorizationError( 'Not allowed to make changes to the group' )

        utg = UserToGroup.select().where( UserToGroup.user == user & UserToGroup.group == group ).first()
        utg.delete_instance()

    @classmethod
    def change( cls, id, name, descr, owner ):
        group = Group.get( id = id )

        if group.owner != owner:
            raise AuthorizationError( 'Not allowed to make changes to the group' )

        if not name:
            name = group.name

        if not descr:
            descr = group.descr

        group.name = name
        group.description = descr
        group.save()

    @classmethod
    def delete( cls, id, owner ):
        group = Group.get( id = id )

        if group.owner != owner:
            raise AuthorizationError( 'Not allowed to make changes to this group' )

        group.delete_instance( True )

    def is_group_member( self, user ):
        return ( self.owner == user or
            UserToGroup.select().where( UserToGroup.user == user & UserToGroup.group == self ).exists() )

    def get_links_count( self, user ):
        if not self.is_group_member( user ):
            raise AuthorizationError( 'Not allowed to obtain this information' + self.name + ' ' + user.name )

        return self.links.count()

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
        group = Group.get( id = group_id )

        if not group.is_group_member( owner ):
            raise AuthorizationError( 'Cannot add a link into a group you\'re not a member of' )

        if url is null: # + other checks
            raise ValueError( 'Incorrect URL' )

        link = cls( url = url, description = descr, owner = owner, date = datetime.now(), group = group )
        link.save()

        return link

    @classmethod
    def delete( cls, id, group_id, user ):
        group = Group.get( id = group_id )
        link = Link.get( id = id )

        if link.owner != user and group.owner != user:
            raise AuthorizationError( 'Not allowed to delete link' )

        link.delete_instance( True )

    @classmethod
    def mark_seen( cls, id, group_id, user ):
        group = Group.get( id = group_id )
        link = Link.get( id = id )


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
