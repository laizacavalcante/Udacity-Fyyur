# TODO
# Implementar busca de shows
# Verificar URL vazia (inserção de artistas ou venues)


# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import babel
import logging
import dateutil.parser
from flask_wtf import Form
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from logging import Formatter, FileHandler
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# REVIEW: Resolve circular import
from models import *


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():

    venue_locations = (
        db.session.query(Venue.city, Venue.state)
        .group_by(Venue.state, Venue.city)
        .all()
    )
    venue_locations = [dict(loc) for loc in venue_locations]

    for venue_loc in venue_locations:
        venue_match = (
            db.session.query(Venue.id, Venue.name)
            .filter(Venue.city == venue_loc["city"], Venue.state == venue_loc["state"])
            .all()
        )
        venue_loc["venues"] = [dict(v) for v in venue_match]

        upcoming_shows = (
            db.session.query(Venue.id)
            .filter(
                Venue.city == venue_loc["city"],
                Venue.state == venue_loc["state"],
                Shows.start_time > datetime.now(),
            )
            .join(Shows)
            .count()
        )

        for match in venue_loc["venues"]:
            match["upcoming_shows"] = upcoming_shows

    return render_template("pages/venues.html", areas=venue_locations)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    requested_word = request.form.get("search_term", None)
    requested_word = requested_word.lower()

    venue_match = (
        db.session.query(Venue.id, Venue.name)
        .filter(Venue.name.ilike(f"%{requested_word}%"))
        .group_by(Venue.id)
        .all()
    )
    venue_match_dict = [dict(venue) for venue in venue_match]

    for venue_m in venue_match_dict:
        num_upcoming_shows = (
            db.session.query(Venue.id)
            .filter(Venue.id == venue_m["id"])
            .join(Shows)
            .filter(Shows.start_time > datetime.now())
            .count()
        )
        venue_m["num_upcoming_shows"] = num_upcoming_shows
    response = {"count": len(venue_match), "data": venue_match_dict}

    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    venue = [Venue.query.get(venue_id)]
    output_dict = {
        t.name: getattr(v, t.name) for v in venue for t in v.__table__.columns
    }

    # Past shows
    past_shows = (
        db.session.query(
            Artist.id.label("artist_id"),
            Artist.name.label("artist_name"),
            Artist.image_link.label("artist_image_link"),
            Shows.start_time,
        )
        .select_from(Venue)
        .join(Shows)
        .join(Artist)
        .filter(Venue.id == venue_id, Shows.start_time < datetime.now())
        .all()
    )

    # Upcoming shows
    upcoming_shows = (
        db.session.query(
            Artist.id.label("artist_id"),
            Artist.name.label("artist_name"),
            Artist.image_link.label("artist_image_link"),
            Shows.start_time,
        )
        .select_from(Venue)
        .join(Shows)
        .join(Artist)
        .filter(Venue.id == venue_id, Shows.start_time > datetime.now())
        .all()
    )

    output_dict["past_shows"] = [dict(d) for d in past_shows]
    output_dict["upcoming_shows"] = [dict(d) for d in upcoming_shows]
    output_dict["past_shows_count"] = len(past_shows)
    output_dict["upcoming_shows_count"] = len(upcoming_shows)

    for shows in [output_dict["upcoming_shows"], output_dict["past_shows"]]:
        for show in shows:
            for k, v in show.items():
                if k == "start_time":
                    show["start_time"] = v.isoformat()

    return render_template("pages/show_venue.html", venue=output_dict)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    venue_info = VenueForm(request.form, meta={"csrf": False})

    # Check Phone number and URLs
    if venue_info.validate_on_submit():
        # if venue_info.validate():

        try:
            new_venue = Venue(**venue_info.to_dict())
            # new_venue = Venue()
            # new_venue.name = venue_info.name.data
            # new_venue.city = venue_info.city.data
            # new_venue.state = venue_info.state.data
            # new_venue.address = venue_info.address.data
            # new_venue.phone = venue_info.phone.data
            # new_venue.genres = venue_info.genres.data
            # new_venue.facebook_link = venue_info.facebook_link.data
            # new_venue.image_link = venue_info.image_link.data
            # new_venue.website_link = venue_info.website_link.data
            # new_venue.seeking_description = venue_info.seeking_description.data
            # new_venue.seeking_talent = venue_info.seeking_talent.data

            db.session.add(new_venue)
            db.session.commit()

            flash(f"Venue {request.form['name']} was successfully listed!")
        except:
            flash(f"An error occured, {request.form['name']} could not be listed")
        finally:
            db.session.close()

    else:
        for field, message in venue_info.errors.items():
            field = field.replace("_", " ")
            flash(f"{message[0]} Please, add a valid {field}")
    return render_template("pages/home.html")


@app.route("/venues/<venue_id>/delete", methods=["GET"])
def delete_venue(venue_id):
    try:
        venue_remove = Venue.query.get(venue_id)
        db.session.delete(venue_remove)
        db.session.commit()
        flash(f"{venue_remove.name} removed!")

    except:
        db.session.rollback()
        flash(f"An error occured, {venue_remove.name} could not be removed")
    finally:
        db.session.close()

    return render_template("pages/home.html")


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    artists = db.session.query(Artist.name, Artist.id).all()
    return render_template("pages/artists.html", artists=artists)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    requested_word = request.form.get("search_term", None)
    requested_word = requested_word.lower()

    artist_match = (
        db.session.query(Artist.id, Artist.name)
        .filter(Artist.name.ilike(f"%{requested_word}%"))
        .group_by(Artist.id)
        .all()
    )
    artist_match_dict = [dict(venue) for venue in artist_match]

    for artist_m in artist_match_dict:
        num_upcoming_shows = (
            db.session.query(Artist.id)
            .filter(Artist.id == artist_m["id"])
            .join(Shows)
            .filter(Shows.start_time > datetime.now())
            .count()
        )
        artist_m["num_upcoming_shows"] = num_upcoming_shows

    response = {"count": len(artist_match), "data": artist_match_dict}
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # Get artist info
    request_artist = [Artist.query.get(artist_id)]
    request_artist_dict = {
        t.name: getattr(a, t.name) for a in request_artist for t in a.__table__.columns
    }
    request_artist_dict["past_shows"] = {}

    # Past shows
    past_shows = (
        db.session.query(
            Venue.id.label("venue_id"),
            Venue.name.label("venue_name"),
            Venue.image_link.label("venue_image_link"),
            Shows.start_time,
        )
        .select_from(Venue)
        .join(Shows)
        .join(Artist)
        .filter(Artist.id == artist_id, Shows.start_time <= datetime.now())
        .all()
    )

    # Upcoming shows
    upcoming_shows = (
        db.session.query(
            Venue.id.label("venue_id"),
            Venue.name.label("venue_name"),
            Venue.image_link.label("venue_image_link"),
            Shows.start_time,
        )
        .select_from(Venue)
        .join(Shows)
        .join(Artist)
        .filter(Artist.id == artist_id, Shows.start_time < datetime.now())
        .all()
    )

    request_artist_dict["past_shows"] = [dict(d) for d in past_shows]
    request_artist_dict["upcoming_shows"] = [dict(d) for d in upcoming_shows]
    request_artist_dict["past_shows_count"] = len(past_shows)
    request_artist_dict["upcoming_shows_count"] = len(upcoming_shows)

    for shows in [
        request_artist_dict["upcoming_shows"],
        request_artist_dict["past_shows"],
    ]:
        for show in shows:
            for k, v in show.items():
                if k == "start_time":
                    show["start_time"] = v.isoformat()

    return render_template("pages/show_artist.html", artist=request_artist_dict)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist_info = Artist.query.get(artist_id)
    form = ArtistForm(
        name=artist_info.name,
        city=artist_info.city,
        state=artist_info.state,
        phone=artist_info.phone,
        image_link=artist_info.image_link,
        genres=artist_info.genres,
        facebook_link=artist_info.facebook_link,
        website_link=artist_info.website,
        seeking_venue=artist_info.seeking_venue,
        seeking_description=artist_info.seeking_description,
    )
    form.validate()
    return render_template("forms/edit_artist.html", form=form, artist=artist_info)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    error = False
    try:
        form = ArtistForm(request.form)
        artist_update = Artist.query.get(artist_id)

        artist_update.name = form.name.data
        artist_update.city = form.city.data
        artist_update.state = form.state.data
        artist_update.phone = form.phone.data
        artist_update.image_link = form.image_link.data
        artist_update.genres = form.genres.data
        artist_update.facebook_link = form.facebook_link.data
        artist_update.website = form.website_link.data
        artist_update.seeking_venue = form.seeking_venue.data
        artist_update.seeking_description = form.seeking_description.data

        db.session.commit()

    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        flash(f"Artist {form.name.data}, id {artist_id} not updated.")
    else:
        flash(f"Artist {form.name.data}, id {artist_id} updated.")

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    venue_info = Venue.query.get(venue_id)
    form = VenueForm(
        name=venue_info.name,
        city=venue_info.city,
        state=venue_info.state,
        address=venue_info.address,
        phone=venue_info.phone,
        image_link=venue_info.image_link,
        genres=venue_info.genres,
        facebook_link=venue_info.facebook_link,
        website_link=venue_info.website,
        seeking_talent=venue_info.seeking_talent,
        seeking_description=venue_info.seeking_description,
    )
    form.validate()
    return render_template("forms/edit_venue.html", form=form, venue=venue_info)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    error = False
    try:
        form = VenueForm(request.form)
        venue_update = Venue.query.get(venue_id)

        venue_update.name = form.name.data
        venue_update.city = form.city.data
        venue_update.state = form.state.data
        venue_update.address = form.address.data
        venue_update.phone = form.phone.data
        venue_update.image_link = form.image_link.data
        venue_update.genres = form.genres.data
        venue_update.facebook_link = form.facebook_link.data
        venue_update.website = form.website_link.data
        venue_update.seeking_talent = form.seeking_talent.data
        venue_update.seeking_description = form.seeking_description.data

        db.session.commit()

    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        flash(f"Venue {form.name.data}, id {venue_id} not updated.")
    else:
        flash(f"Venue {form.name.data}, id {venue_id} updated.")

    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    artist_info = ArtistForm(request.form, meta={"csrf": False})

    if artist_info.validate():
        try:
            new_artist = Artist(**artist_info.to_dict())
            # new_artist.name = artist_info.name.data
            # new_artist.city = artist_info.city.data
            # new_artist.state = artist_info.state.data
            # new_artist.phone = artist_info.phone.data
            # new_artist.genres = artist_info.genres.data
            # new_artist.facebook_link = artist_info.facebook_link.data
            # new_artist.image_link = artist_info.image_link.data
            # new_artist.website_link = artist_info.website_link.data
            # new_artist.seeking_description = artist_info.seeking_description.data
            # new_artist.seeking_venue = artist_info.seeking_venue.data

            db.session.add(new_artist)
            db.session.commit()

            flash(f"Artist {request.form['name']} was successfully listed!")
        except:
            flash(f"An error occured, {request.form['name']} could not be listed")
        finally:
            db.session.close()
    else:
        for field, message in artist_info.errors.items():
            field = field.replace("_", " ")
            flash(f"{message[0]} Please, add a valid {field}")

    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    data = (
        db.session.query(
            Venue.id.label("venue_id"),
            Venue.name.label("venue_name"),
            Artist.id.label("artist_id"),
            Artist.image_link.label("artist_image_link"),
            Shows.start_time,
        )
        .select_from(Venue)
        .join(Shows)
        .join(Artist)
        .all()
    )

    dict_data = [dict(element) for element in data]
    for show in dict_data:
        for k, v in show.items():
            if k == "start_time":
                show["start_time"] = v.isoformat()

    return render_template("pages/shows.html", shows=dict_data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    new_show_info = ShowForm(request.form, meta={"csrf": False})

    if new_show_info.validate():
        try:
            new_show = Shows()
            new_show.artist_id = new_show_info.artist_id.data
            new_show.venue_id = new_show_info.venue_id.data
            new_show.start_time = new_show_info.start_time.data

            db.session.add(new_show)
            db.session.commit()

            flash("Show was successfully listed!")
        except:
            flash(f"An error occured, current show could not be listed")
        finally:
            db.session.close()
    else:
        for field, message in new_show_info.errors.items():
            field = field.replace("_", " ")
            flash(f"{message[0]} Please, add a valid {field}")
    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run(debug=True)

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
