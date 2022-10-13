import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

# REVIEW username, password and port should be accessed from .ENV
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost:5432/fyyur"
