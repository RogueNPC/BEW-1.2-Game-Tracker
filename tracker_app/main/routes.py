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