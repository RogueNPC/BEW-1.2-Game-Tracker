import os
import unittest

from tracker_app import app, db, bcrypt
from tracker_app.models import Console, Game, User

"""
Run these tests with the command:
python -m unittest discover
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_items():
    a1 = Console(name='Gamecube', portable=False)
    b1 = Game(
        title='NBA 2K3',
        console=a1,
    )
    db.session.add(b1)

    a2 = Console(name='Samsung S10', portable=True)
    b2 = Game(
        title='Dynamix', 
        console=a2
    )
    db.session.add(b2)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='username', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that everything that should show up on the homepage does."""
        # Set up
        create_items()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Gamecube', response_text)
        self.assertIn('Samsung S10', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Create Console', response_text)
        self.assertNotIn('Create Game', response_text)
        self.assertNotIn('Create Genre', response_text)
        self.assertNotIn('Profile', response_text)
        self.assertNotIn('Log Out', response_text)

    def test_homepage_logged_in(self):
        """Test that everything that should show up on the homepage does."""
        # Set up
        create_items()
        create_user()
        login(self.app, 'username', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Gamecube', response_text)
        self.assertIn('Samsung S10', response_text)
        self.assertIn('Create Console', response_text)
        self.assertIn('Create Game', response_text)
        self.assertIn('Create Genre', response_text)
        self.assertIn('Profile', response_text)
        self.assertIn('Log Out', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_console_detail(self):
        """Test that everything that should show up on the homepage does."""
        # Set up
        create_items()
        create_user()
        login(self.app, 'username', 'password')

        # a GET request to the URL /console/1, check to see that the
        # status code is 200
        result = app.test_client().get('/console/1', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        result_text = result.get_data(as_text=True)

        # Checks that the response contains the console's name and if it's portable
        console = Console.query.get(1)
        self.assertEqual(console.name, 'Gamecube')
        self.assertEqual(console.portable, False)

    def test_game_detail(self):
        # Set up
        create_items()
        create_user()
        login(self.app, 'username', 'password')

        # a GET request to the URL /game/1, check to see that the
        # status code is 200
        result = app.test_client().get('/game/1', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        result_text = result.get_data(as_text=True)

        # Checks that the response contains the game's title and console
        game = Game.query.get(1)
        self.assertEqual(game.title, 'NBA 2K3')
        self.assertEqual(game.console, Console.query.get(1))

    def test_create_console(self):
        # Set up
        create_items()
        create_user()
        login(self.app, 'username', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Wii',
            'company': 'Nintendo',
            'console_notes': 'The first of its kind when it came out. It revolutionized the market!'
        }
        self.app.post('/new_console', data=post_data)

        # Make sure console was created as we'd expect
        created_console = Console.query.filter_by(name='Wii').one()
        self.assertIsNotNone(created_console)
        self.assertEqual(created_console.company, 'Nintendo')
        self.assertEqual(created_console.portable, False)

    def test_create_game(self):
        # Set up
        create_items()
        create_user()
        login(self.app, 'username', 'password')

        # Make POST request with data
        post_data = {
            'title': 'Kirbys Epic Yarn',
            'publisher': 'Nintendo',
            'personal rating': '7',
            'game_notes': 'One of the best kirby games I have played! Just a bit on the easy side.',
            'console': 1
        }
        self.app.post('/new_game', data=post_data)

        # Make sure game was created as we'd expect
        created_game = Game.query.filter_by(title='Kirbys Epic Yarn').one()
        self.assertIsNotNone(created_game)
        self.assertEqual(created_game.publisher, 'Nintendo')
        self.assertEqual(created_game.console.name, 'Gamecube')