from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# Modeling many to many relationships
# Info: https://stackoverflow.com/questions/70321045/sqlalchemy-orm-many-to-many-relationship-query-with-junction-table-attribute
# Link: https://michaelcho.me/article/many-to-many-relationships-in-sqlalchemy-models-flask
# Link: https://www.youtube.com/watch?v=IlkVu_LWGys

# Split database models
# Link: https://stackoverflow.com/questions/34281873/how-do-i-split-flask-models-out-of-app-py-without-passing-db-object-all-over

# Verificar se o problmea é o datetime da coluna de shows (deveria ser string?)

class Venue(db.Model):
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String(120))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String))
  website = db.Column(db.String)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(800))

  venue_shows = db.relationship("Shows", back_populates="venue") #alimenta a relacao Shows.venue

class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String)
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(800))

  artist_shows = db.relationship("Shows", back_populates="artist") #alimenta a relacao Shows.artist

class Shows(db.Model):
  __tablename__ = "shows"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  start_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'))
  venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'))

  artist = db.relationship('Artist', back_populates='artist_shows')
  venue = db.relationship('Venue', back_populates='venue_shows')