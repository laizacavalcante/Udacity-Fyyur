import re
import enum
from datetime import datetime
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, URL, InputRequired, Optional


STATE_OPTIONS = [
    ("AL", "AL"),
    ("AK", "AK"),
    ("AZ", "AZ"),
    ("AR", "AR"),
    ("CA", "CA"),
    ("CO", "CO"),
    ("CT", "CT"),
    ("DE", "DE"),
    ("DC", "DC"),
    ("FL", "FL"),
    ("GA", "GA"),
    ("HI", "HI"),
    ("ID", "ID"),
    ("IL", "IL"),
    ("IN", "IN"),
    ("IA", "IA"),
    ("KS", "KS"),
    ("KY", "KY"),
    ("LA", "LA"),
    ("ME", "ME"),
    ("MT", "MT"),
    ("NE", "NE"),
    ("NV", "NV"),
    ("NH", "NH"),
    ("NJ", "NJ"),
    ("NM", "NM"),
    ("NY", "NY"),
    ("NC", "NC"),
    ("ND", "ND"),
    ("OH", "OH"),
    ("OK", "OK"),
    ("OR", "OR"),
    ("MD", "MD"),
    ("MA", "MA"),
    ("MI", "MI"),
    ("MN", "MN"),
    ("MS", "MS"),
    ("MO", "MO"),
    ("PA", "PA"),
    ("RI", "RI"),
    ("SC", "SC"),
    ("SD", "SD"),
    ("TN", "TN"),
    ("TX", "TX"),
    ("UT", "UT"),
    ("VT", "VT"),
    ("VA", "VA"),
    ("WA", "WA"),
    ("WV", "WV"),
    ("WI", "WI"),
    ("WY", "WY"),
]


class GenresOptions(enum.Enum):
    Alternative = "Alternative"
    Blues = "Blues"
    Classical = "Classical"
    Country = "Country"
    Electronic = "Electronic"
    Folk = "Folk"
    Funk = "Funk"
    Hipop = "Hip-Hop"
    HeavyMetal = "Heavy Metal"
    Instrumental = "Instrumental"
    Jazz = "Jazz"
    MusicalTheatre = "Musical Theatre"
    Pop = "Pop"
    Punk = "Punk"
    RB = "R&B"
    Reggae = "Reggae"
    RocknRoll = "Rock n Roll"
    Soul = "Soul"
    Other = "Other"

    def __str__(self):
        return self.name

    def __html__(self):
        return self.value


def validate_phone(form, field):
    if not re.search(r"^[\+\(]?\d+(?:[- \)\(]+\d+)+$", field.data):
        raise ValidationError("Invalid phone number!")


def genres_enum_opts(enum):
    # Adapted from: https://stackoverflow.com/questions/44078845/using-wtforms-with-enum
    assert not {"__str__", "__html__"}.isdisjoint(
        vars(enum)
    ), "The {!r} enum class does not implement __str__ and __html__ methods"

    def coerce(name):
        if isinstance(name, enum):
            return name
        try:
            return enum[name]
        except KeyError:
            raise ValueError(name)

    return {"choices": [(v.name, v.value) for v in enum]}


class ShowForm(FlaskForm):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=STATE_OPTIONS)
    address = StringField("address", validators=[DataRequired()])
    phone = StringField(
        "phone",
        validators=[InputRequired(), validate_phone],
    )
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], **genres_enum_opts(GenresOptions)
    )
    facebook_link = StringField("facebook_link", validators=[Optional(), URL()])
    website_link = StringField("website_link", validators=[Optional(), URL()])

    seeking_talent = BooleanField("seeking_talent")

    seeking_description = StringField("seeking_description")


class ArtistForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=STATE_OPTIONS)
    phone = StringField("phone", validators=[InputRequired(), validate_phone])
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], **genres_enum_opts(GenresOptions)
    )
    facebook_link = StringField(
        "facebook_link",
        validators=[Optional(), URL()],
    )

    website_link = StringField("website_link", validators=[Optional(), URL()])

    seeking_venue = BooleanField("seeking_venue")

    seeking_description = StringField("seeking_description")
