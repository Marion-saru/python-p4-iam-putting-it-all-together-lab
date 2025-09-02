#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_user = User(
                username=data['username'],
                image_url=data['image_url'],
                bio=data['bio']
            )
            new_user.password_hash = data['password']
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(rules=('-password_hash',)), 201
        except ValueError as e:
            return {'errors': [str(e)]}, 422

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(rules=('-password_hash',)), 200
        return {'error': '401 Unauthorized'}, 401

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.username == data['username']).first()
        if user:
            if user.authenticate(data['password']):
                session['user_id'] = user.id
                return user.to_dict(rules=('-password_hash',)), 200
            else:
                return {'error': 'Invalid password'}, 401
        else:
            return {'error': 'Invalid username'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {'error': '401 Unauthorized'}, 401

class RecipeIndex(Resource):
    def get(self):
        if session.get('user_id'):
            recipes = [r.to_dict(rules=('-user.recipes',)) for r in Recipe.query.all()]
            return recipes, 200
        return {'error': '401 Unauthorized'}, 401

    def post(self):
        if session.get('user_id'):
            data = request.get_json()
            try:
                new_recipe = Recipe(
                    title=data['title'],
                    instructions=data['instructions'],
                    minutes_to_complete=data['minutes_to_complete'],
                    user_id=session['user_id']
                )
                db.session.add(new_recipe)
                db.session.commit()
                return new_recipe.to_dict(rules=('-user.recipes',)), 201
            except ValueError as e:
                return {'errors': [str(e)]}, 422
        return {'error': '401 Unauthorized'}, 401

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)