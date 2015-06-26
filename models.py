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
    def register( cls, name, email, password, password2 ):
        if not name or len( name ) < 3 or len( name ) > 128:
            raise ValueError( 'Name too short or too long' )
        elif not email or not re.match( r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email ):
            raise ValueError( 'Wrong email format' )
        elif password != password2:
            raise ValueError( 'Passwords do not match' )
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
        u = User.authenticate( email, password )
        u.delete_instance( True )

    @classmethod
    def autocomplete( cls, query, user ):
        if not query or len( query ) < 3:
            raise ValueError( 'Query too short' )

        # filter out the asker
        return [ { 'id' : x.id, 'name' : x.name, 'email' : x.email }
            for x in cls.select().where( User.name ** ( '%' + query + '%' ) ).where( User.email != user.email ) ]

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
    def get_dict( cls, id, user ):
        group = cls.get( id = id )

        if group.is_member_of( user ):
            return {
                'id' : group.id,
                'name' : group.name,
                'descr' : group.description,
                'owner' : group.owner.name,
                'is_owner' : user == group.owner,
                'users' : shorten_array( [ x.user.name for x in group.user_rels ], 5 ),
                'links' : [ l.get_dict( group, user ) for l in group.links ] }
        else:
            raise AuthorizationError( 'Not allowed to see the group' )

    @classmethod
    def get_all( cls, user ):
        return [ {
            'id' : group.id,
            'name' : group.name,
            'descr' : group.description,
            'owner' : group.owner.name,
            'users' : shorten_array( [ x.user.name for x in group.user_rels ], 5 ),
            'links_count' : group.get_links_count( user ),
            'unseen_count' : group.get_unseen_count( user ) }
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
    def remove( cls, id, owner ):
        group = Group.get( id = id )

        if group.owner != owner:
            raise AuthorizationError( 'Not allowed to make changes to this group' )

        group.delete_instance( True )

    def is_member_of( self, user ):
        return ( self.owner == user or
            self in [ utg.group for utg in user.group_rels ] )

    def get_links_count( self, user ):
        if not self.is_member_of( user ):
            raise AuthorizationError( 'Not allowed to obtain this information' )

        return self.links.count()

    def get_unseen_count( self, user ):
        if not self.is_member_of( user ):
            raise AuthorizationError( 'Not allowed to obtain this information' )

        return 0
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

        if not group.is_member_of( owner ):
            raise AuthorizationError( 'Cannot add a link into a group you\'re not a member of' )

        if url is None or len( url ) < 0: # + other checks
            raise ValueError( 'Incorrect URL' )

        link = cls( url = url, description = descr, owner = owner, date = datetime.now(), group = group )
        link.save()

        return link

    @classmethod
    def remove( cls, id, group_id, user ):
        group = Group.get( id = group_id )
        link = Link.get( id = id )

        if link.owner != user and group.owner != user:
            raise AuthorizationError( 'Not allowed to delete link' )

        link.delete_instance( True )

    @classmethod
    def mark_seen( cls, id, group_id, user ):
        group = Group.get( id = group_id )
        link = Link.get( id = id )

        if not group.is_member_of( user ):
            raise AuthorizationError( 'Not allowed to see the link' )

        try:
            UserToLink.create( user = user, link = link )
        except IntegrityError:
            raise ValueError( 'User already seen the link' )

    def get_dict( self, group, user ):
        if not group.is_member_of( user ):
            raise AuthorizationError( 'Not allowed to obtain the information' )

        users_seen = [ utl.user for utl in UserToLink.select().where( UserToLink.link == self ) ]

        return {
            'id' : self.id,
            'url' : self.url,
            'descr' : self.description,
            'owner' : self.owner.name,
            'date' : self.date,
            'seen' : shorten_array( [ u.name for u in users_seen ], 5 ),
            'seen_by_owner' : user in users_seen,
            'comments' : [ c.get_dict( self, user ) for c in self.comments ]
        }


class Comment( MetaModel ):
    content = TextField()
    date = DateTimeField()
    link = ForeignKeyField( Link, related_name = 'comments' )
    owner = ForeignKeyField( User, related_name = 'comments' )

    @classmethod
    def add( cls, content, link_id, owner ):
        if not content:
            raise ValueError( 'No contents provided for a comment' )

        link = Link.get( id = link_id )

        if not link.group.is_member_of( owner ):
            raise AuthorizationError( 'Not allowed to add a comment' )

        comment = Comment( content = content, date = datetime.now(), link = link, owner = owner )
        comment.save()

        return comment

    @classmethod
    def delete( cls, id, user ):
        pass

    def get_dict( self, link, user ):
        if not link.group.is_member_of( user ):
            raise AuthorizationError( 'Not allowed to obtain the information' )

        return {
            'content' : self.content,
            'date' : self.date,
            'owner' : self.owner.name
        }

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
