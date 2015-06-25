from models import *

db.create_tables( [ User, Group, Link, Comment, UserToGroup, UserToLink ], safe = True )

u1 = User.register( 'Mirko Mirković', 'mirko@mail.com', 'lozinka1', 'lozinka1' )
u2 = User.register( 'Slavko Slavković', 'slavko@mail.com', 'zaporka1', 'zaporka1' )
u3 = User.register( 'Francisco Goya', 'fgoya@mail.com', 'ThirdOfMay1808', 'ThirdOfMay1808' )
u4 = User.register( 'Pablo Picasso', 'ppicasso@mail.com', 'Guernica', 'Guernica' )
u5 = User.register( 'Vincent Van Gogh', 'vvgogh@mail.com', 'StarryNight', 'StarryNight' )
u6 = User.register( 'Claude Monet', 'cmonet@mail.com', 'Impression', 'Impression' )
u7 = User.register( 'Salvador Dali', 'sdali@mail.com', 'PersistenceOfMemory', 'PersistenceOfMemory' )
u8 = User.register( 'Paul Gauguin', 'pgauguin@mail.com', 'WhereWhatWhere', 'WhereWhatWhere' )
u9 = User.register( 'Edvard Munch', 'emunch@mail.com', 'TheScream', 'TheScream' )
u10 = User.register( 'Rembrandt van Rijn', 'rembrandt@mail.com', 'NightWatch', 'NightWatch' )

g1 = Group.new( 'Economics and Politics', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.', u1 )
g2 = Group.new( 'Programming', 'Adipisci voluptas dignissimos aspernatur dolorum sequi iste qui.', u1 )
g3 = Group.new( 'Random stuff', 'Cumque eius deleniti cupiditate impedit reprehenderit perspiciatis.', u1 )
g4 = Group.new( 'Science', 'Sapiente nam, quis fugit temporibus dignissimos nihil tempore at unde.', u2 )
g5 = Group.new( 'Philosophy', 'Temporibus corporis, eum tempore fugiat, labore libero maiores nemo.', u3 )
g6 = Group.new( 'News articles', 'Soluta facere voluptas atque quo, officia libero excepturi dignissimos.', u4 )
g7 = Group.new( 'DIY Resources', 'Ad, expedita quis recusandae, iure, commodi, dolores sed architecto.', u5 )
g8 = Group.new( 'Book list', 'Quos nihil laudantium libero sint architecto animi consequatur modi.', u6 )
g9 = Group.new( 'Chesterton', 'A collection of links on Chesterton\'s essays, poems and other writings.', u7 )
g10 = Group.new( 'Web Design Inspiration', 'Some beautifully designed web pages for inspiration.', u8 )

Group.add_user( g1.id, u1, u2 )
Group.add_user( g1.id, u1, u3 )
Group.add_user( g1.id, u1, u4 )

Group.add_user( g2.id, u1, u5 )
Group.add_user( g2.id, u1, u6 )
Group.add_user( g2.id, u1, u7 )

Group.add_user( g5.id, u3, u2 )
Group.add_user( g5.id, u3, u4 )
Group.add_user( g5.id, u3, u7 )

Group.add_user( g9.id, u7, u5 )

l1 = Link.add( 'http://www.cse.dmu.ac.uk/~mward/gkc/books/Fancies_Versis_Fads.txt',
    'A collection of G. K. Chesterton\'s essays on various topics', u7, g9 )
l2 = Link.add( 'http://www.cse.dmu.ac.uk/~mward/gkc/books/superstitions-of-the-sceptic.txt',
    'A transcript of Chesterton\'s speech on the subject of *modern scepticism and modern superstitions*', u7, g9 )
l3 = Link.add( 'http://www.cse.dmu.ac.uk/~mward/gkc/books/gkcday/gkcday03.html',
    'Selection of Chesterton\'s quotes and short works, one for every day of the year.', u5, g9 )

Link.mark_seen( l1.id, g9.id, u5 )

Comment.add( 'Stvarno fora, isplati se procitat', l2.id, u5 )
