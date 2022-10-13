# music_hop = Venue(
#     id = 1,
#     name = "The Musical Hop",
#     address = "1015 Folsom Street",
#     city = "San Francisco",
#     state = "CA",
#     phone = "123-123-1234",
#     genres = ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#     website = "https://www.themusicalhop.com",
#     image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#     facebook_link = "https://www.facebook.com/TheMusicalHop",
#     seeking_talent = True,
#     seeking_description = "We are on the lookout for a local artist to play every two weeks. Please call us.",
# )

# guns = Artist(
#     id = 4,
#     name = "Guns N Petals",
#     city = "San Francisco",
#     state = "CA",
#     phone = "326-123-5000",
#     genres = ["Rock n Roll"],
#     image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     facebook_link = "https://www.facebook.com/GunsNPetals",
#     website = "https://www.gunsnpetalsband.com",
#     seeking_venue = True,
#     seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!",
# )

# # Ao montar a relacão entre artista, venue e show, eu devo usar o campo de 
# # relationship e não o de FK, pois esse será preenchido automaticamente pela 
# # relacao definida
show_guns_hop = Shows(
    start_time="2019-05-21T21:30:00.000Z",
    artist=guns,
    venue=music_hop
)

###############################################
dueling_piano = Venue(
    id = 2,
    name = "The Dueling Pianos Bar",
    address = "335 Delancey Street",
    city = "New York",
    state = "NY",
    phone = "914-003-1132",
    genres = ["Classical", "R&B", "Hip-Hop"],
    website = "https://www.theduelingpianos.com",
    image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    facebook_link = "https://www.facebook.com/theduelingpianos",
    seeking_talent = False
)
db.session.add(dueling_piano)
db.session.commit()

park_square = Venue(
    id = 3,
    name = "Park Square Live Music & Coffee",
    address = "34 Whiskey Moore Ave",
    city = "San Francisco",
    state = "CA",
    phone = "415-000-1234",
    genres = ["Rock n Roll", "Jazz", "Classical", "Folk"],
    website = "https://www.parksquarelivemusicandcoffee.com",
    image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",    
    facebook_link = "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent = False
)

wild_sax = Artist(
    id = 6,
    name = "The Wild Sax Band",
    city = "San Francisco",
    state = "CA",
    phone = "432-325-5432",
    genres = ["Jazz", "Classical"],
    image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    seeking_venue = False
)

show_wild_sax_1 = Shows(
    start_time="2035-04-01T20:00:00.000Z",
    artist=wild_sax,
    venue=park_square
)

show_wild_sax_2 = Shows(
    start_time="2035-04-08T20:00:00.000Z",
    artist=wild_sax,
    venue=park_square
)

show_wild_sax_3 = Shows(
    start_time="2035-04-15T20:00:00.000Z",
    artist=wild_sax,
    venue=park_square
)

db.session.add_all([
    park_square, wild_sax, show_wild_sax_1, show_wild_sax_2, show_wild_sax_3
])
db.session.commit()


###############################################

matt = Artist(
    id = 5,
    name = "Matt Quevedo",
    city = "New York",
    state = "NY",
    phone = "300-400-5000",
    genres = ["Jazz"],
    image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    facebook_link = "https://www.facebook.com/mattquevedo923251523",
    seeking_venue = False,
)


mat_venue = Shows(
    start_time="2019-06-15T23:00:00.000Z",
    artist=matt,
    venue=Venue.query.get(3)
)


db.session.query(Artist).join(Shows, Artist.id == Shows.artist_id, isouter=True).all()


tt = (
    db.session.query(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, Shows.start_time)
    .join(Shows, Venue.id == Shows.venue_id)
    .join(Artist, Shows.artist_id == Shows.artist_id)
    .all()
)


shows = (
db.session.query(
Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, 
func.to_char(Shows.start_time, 'YYYY-mm-dd HH:MM:SS')
)
.join(Shows, Venue.id == Shows.venue_id)
.join(Artist, Shows.artist_id == Shows.artist_id)
.all()
)


shows = (
db.session.query(
Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, 
Shows.start_time
)
.join(Shows, Venue.id == Shows.venue_id)
.join(Artist, Shows.artist_id == Shows.artist_id)
.all()
)
shows_dict = [dict(row) for row in shows]

for show in shows_dict:
    for k, v in show.items():
        if k == "start_time":
            k['start_time'] = v.isoformat()

#%%
import sqlalchemy
from models import *
from sqlalchemy import select
query = (
    db.session.query(Venue, Shows)
    .join(Shows)
    .join(Artist)
    .filter(Venue.id == Shows.venue_id, 
        Artist.id == Shows.artist_id)
).all()
query



# venue_artist_shows = select(Artist).join(subq, Artist.id == subq.c.artist_id)
#%%

shows = (
db.session.query(
    Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, 
    Shows.start_time
)
.join(Shows, Venue.id == Shows.venue_id)
.join(Artist, Shows.artist_id == Shows.artist_id)
.all()
)
shows_dict = [dict(row) for row in shows]


#%%
from datetime import datetime


past_shows = (
    db.session.query(
        (Artist.id).label('artist_id'), Artist.name, Artist.image_link, Shows.start_time
    )
    .select_from(Venue)
    .join(Shows)
    .join(Artist)
    .filter(Venue.id == 3, Shows.start_time < datetime.now())
    .all()
)
upcoming_shows = (
    db.session.query(
        Artist.id, Artist.name, Artist.image_link, Shows.start_time
    )
    .select_from(Venue)
    .join(Shows)
    .join(Artist)
    .filter(Venue.id == 3, Shows.start_time > datetime.now())
    .all()
)
# %%
output = (
    db.session.query(Venue.id, Venue.name)
    .filter(Venue.name.ilike('%music%'))
    .join(Shows)
    .filter(Shows.start_time > datetime.now())
    .all()


#%%
from models import * 
from sqlalchemy.sql.functions import coalesce, count
from sqlalchemy import case
from datetime import datetime


db.session.query(
    coalesce(db.func.count(Shows.start_time ), 0),
    Shows
).filter(Shows.start_time > datetime.now()).all()


#%%

from sqlalchemy import case, select

tt = select(Shows.id, Shows.venue_id, Shows.start_time).\
            where(
                case(
                    (Shows.start_time > datetime.now(), True),
                    else_=False
                )
            )

#%%

my_config = session.query(Config).order_by(coalesce(Config.last_processed_at, datetime.date.min)).first()
subquery = (
    db.session.query(Venue)
    .order_by()
)