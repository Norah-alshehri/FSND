#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)),nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(800))
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Venue', lazy="joined")

    @property 
    def upcoming_shows(self):
      upcoming_shows = [show for show in self.shows if show.start_time > datetime.now()] #datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > now]
      return upcoming_shows
    @property
    def num_upcoming_shows(self):
      return len(self.upcoming_shows)
    
    @property
    def past_shows(self):
      past_shows = [show for show in self.shows if show.start_time < datetime.now()]
      return past_shows
    
    @property
    def num_past_shows(self):
      return len(self.past_shows)

    
    
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate: DONE

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)),nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist', lazy="joined")

    @property
    def upcoming_shows(self):
      upcoming_shows = [show for show in self.shows if show.start_time > datetime.now()]
      return upcoming_shows
      
    @property
    def num_upcoming_shows(self):      
      return len(self.upcoming_shows)
        
    @property
    def past_shows(self):
      past_shows = [show for show in self.shows if show.start_time < datetime.now()]
      
      return past_shows
      
    @property
    def num_past_shows(self):
      return len(self.past_shows)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate: DONE

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.:DONE
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>'

  