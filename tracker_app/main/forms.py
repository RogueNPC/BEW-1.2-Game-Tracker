from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from tracker_app.models import Console, Game, Genre, User

class ConsoleForm(FlaskForm):
    """Form to create a console."""
    name = StringField('Console Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    company = StringField('Company')
    portable = BooleanField('Portable?')
    console_notes = TextAreaField('Notes')
    submit = SubmitField('Submit')

class GameForm(FlaskForm):
    """Form to create a game."""
    title = StringField('Game Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    publisher = StringField('Publisher')
    personal_rating = IntegerField('Rating')
    console = QuerySelectField('Console', 
        query_factory=lambda: Console.query, allow_blank=False)
    genres = QuerySelectMultipleField('Genres',
        query_factory=lambda: Genre.query)
    game_notes = TextAreaField('Notes')
    submit = SubmitField('Submit')

class GenreForm(FlaskForm):
    """Form to create a genre."""
    name = StringField('Genre Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')