"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from tracker_app.models import Console, Game, Genre, User
from tracker_app.main.forms import ConsoleForm, GameForm, GenreForm
from tracker_app import bcrypt

# Import app and db from events_app package so that we can run app
from tracker_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_consoles = Console.query.all()
    print(all_consoles)
    return render_template('home.html', all_consoles=all_consoles)

@main.route('/new_console', methods=['GET', 'POST'])
@login_required
def new_console():
    # Creates a ConsoleForm
    form = ConsoleForm()

    # If form was submitted and was valid:
    if form.validate_on_submit():
        new_console = Console(
            name=form.name.data,
            company=form.company.data,
            portable=form.portable.data,
            console_notes=form.console_notes.data
        )
        # Add console to database
        db.session.add(new_console)
        db.session.commit()

        # Flash success message, redirect to detail page
        flash('New console was added!')
        return redirect(url_for('main.console_detail', console_id=new_console.id))
    return render_template('new_console.html', form=form)

@main.route('/new_game', methods=['GET', 'POST'])
@login_required
def new_game():
    # Creates a GameForm
    form = GameForm()

    # If form was submitted and was valid:
    if form.validate_on_submit():
        new_game = Game(
            title=form.title.data,
            publisher=form.publisher.data,
            personal_rating=form.personal_rating.data,
            game_notes=form.game_notes.data,
            console=form.console.data,
            genres=form.genres.database
        )
        # Add game to database
        db.session.add(new_game)
        db.session.commit()

        # Flash success message, redirect to detail page
        flash('New game was added!')
        return redircet(url_for('main.game_detail', game_id=new_game.id))
    return render_template('new_game.html', form=form)

@main.route('/create_genre', methods=['GET', 'POST'])
@login_required
def create_genre():
    # Creates a GenreForm
    form = GenreForm()

    # If form was submitted and was valid:
    if form.validate_on_submit():
        new_genre = Genre(
            name=form.name.data
        )
        # Add genre to database
        db.session.add(new_genre)
        db.session.commit()

        # Flash success message, redirect to homepage
        flash('New genre was added!')
        return redirect(url_for('main.homepage'))
    return render_template('create_genre.html', form=form)

@main.route('/console/<console_id>', methods=['GET', 'POST'])
@login_required
def console_detail(console_id):
    console = Console.query.get(console_id)
    form = ConsoleForm(obj=console)

    # If form was submitted and was valid:
    if form.validate_on_submit():
        # Populates the attributes of the passed obj with data from the form's fields
        form.populate_obj(console)
        db.session.add(console)
        db.session.commit()

        flash('Console was edited!')
        return redirect(url_for('main.console_detail', console_id=console.id))
    console = Console.query.get(console_id)
    return render_template('console_detail.html', console=console, form=form)

@main.route('/game/<game_id>', methods=['GET', 'POST'])
@login_required
def game_detail(game_id):
    game = Game.query.get(game_id)
    form = GameForm(obj=game)

    # If form was submitted and was valid:
    if form.validate_on_submit():
        # Populates the attributes of the passed obj with data from the form's fields
        form.populate_obj(game)
        db.session.add(game)
        db.session.commit()

        flash('Game was edited!')
        return redirect(url_for('main.game_detail', game_id=game.id))
    game = Game.query.get(game_id)
    return render_template('game_detail.html', game=game, form=form)