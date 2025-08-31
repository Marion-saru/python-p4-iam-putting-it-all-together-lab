#!/usr/bin/env python3
from flask import Flask, request, session
from flask_restful import Api, Resource
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from extensions import db, bcrypt  # import single db and bcrypt
from models import User, Recipe

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'super_secret_key'
    app.json.compact = False

    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    # register resources...
    from routes import register_resources
    register_resources(api)

    @app.route('/')
    def home():
        return '<h1>Recipe Sharing API</h1>'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5555, debug=True)
