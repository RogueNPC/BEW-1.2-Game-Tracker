"""Create database models to represent tables."""
from tracker_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class Console(db.model):
    """Console model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80))
    portable = db.Column(db.Boolean())
    console_notes = db.Column(db.String(200))
    games = db.relationship('Game', back_populates='console')


class Game(db.model):
    """Game model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80))
    personal_rating = db.Column(db.Integer)
    game_notes = db.Column(db.String(200))
    console_id = db.Column(db.Integer, db.ForeignKey('console.id'), nullable=False)
    console = db.relationship('Console', back_populates='games')
    genres = db.relationship('Genre', secondary='game_genre', back_populates='games')

class Genre(db.model):
    """Genre model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    games = db.relationship('Game', secondary='game_genre', back_populates='genres')

game_genre_table = db.Table('game_genre',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)