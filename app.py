from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_database, database_exists

# Set up flask app and sqlalchemy database
app = Flask(__name__)
app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/team1_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

# Create corresponding models based off of ER diagram
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(100))
    user_pass = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
    user_admin = db.Column(db.Boolean, default = False)

    
    def __init__(self, user_id, user_name, user_pass, user_email, user_admin):
        self.user_id = user_id
        self.user_name = user_name
        self.user_pass = user_pass
        self.user_email = user_email
        self.user_admin = user_admin

class Recipes(db.Model):
    recipe_id = db.Column(db.Integer, primary_key = True)
    recipe_name = db.Column(db.String(100))
    recipe_description = db.Column(db.String(100))
    recipe_ingredients = db.Column(db.String(100))
    recipe_instructions = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, recipe_id, recipe_name, recipe_description, recipe_ingredients, recipe_instruction, user_id):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.recipe_description = recipe_description
        self.recipe_ingredients = recipe_ingredients
        self.recipe_instructions = recipe_instruction
        self.user_id = user_id

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key = True)
    comment_content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    
    def __init__(self, comment_id, comment_content, user_id, recipe_id):
        self.comment_id = comment_id
        self.comment_content = comment_content
        self.user_id = user_id
        self.recipe_id = recipe_id

class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key = True)
    tag_name = db.Column(db.String(100))

    def __init__(self, tag_id, tag_name):
        self.tag_id = tag_id
        self.tag_name = tag_name

class RecipeTags(db.Model):
    recipeTag_id = db.Column(db.Integer, primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))

    def __init__(self, recipeTag_id, tag_id, recipe_id):
        self.recipeTag_id = recipeTag_id
        self.tag_id = tag_id
        self.recipe_id = recipe_id


# Creates tables if they are missing from database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)