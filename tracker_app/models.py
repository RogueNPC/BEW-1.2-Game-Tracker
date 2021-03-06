"""Create database models to represent tables."""
from tracker_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

class Console(db.Model):
    """Console model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80))
    portable = db.Column(db.Boolean, nullable=False)
    console_notes = db.Column(db.String(200))

    # The games - What games exist on this console?
    games = db.relationship('Game', back_populates='console')

    # Who owns this console?
    users_who_own = db.relationship('User', secondary='user_console', back_populates='consoles_owned')

    def __str__(self):
        return f'<Console: {self.name}>'

    def __repr__(self):
        return f'<Console: {self.name}>'

class Game(db.Model):
    """Game model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80))
    personal_rating = db.Column(db.Integer)
    game_notes = db.Column(db.String(200))

    # The console - Which console do users play this game on?
    console_id = db.Column(db.Integer, db.ForeignKey('console.id'), nullable=False)
    console = db.relationship('Console', back_populates='games')

    # The genres, e.g. first-person shooter (FPS), role-playing game (RPG), sandbox
    genres = db.relationship('Genre', secondary='game_genre', back_populates='games')

    # Who owns this game?
    users_who_own = db.relationship('User', secondary='user_game', back_populates='games_owned')

    def __str__(self):
        return f'<Game: {self.name}>'

    def __repr__(self):
        return f'<Game: {self.name}>'

class Genre(db.Model):
    """Genre model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # The games - what games have these genres?
    games = db.relationship('Game', secondary='game_genre', back_populates='genres')

    def __str__(self):
        return f'<Genre: {self.name}>'

    def __repr__(self):
        return f'<Genre: {self.name}>'

# Game <--> Genre table
game_genre_table = db.Table('game_genre',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    consoles_owned = db.relationship('Console', secondary='user_console', back_populates='users_who_own')
    games_owned = db.relationship('Game', secondary='user_game', back_populates='users_who_own')

# Console <--> User table
consoles_owned_table = db.Table('user_console',
    db.Column('console_id', db.Integer, db.ForeignKey('console.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# Game <--> User table
games_owned_table = db.Table('user_game',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)