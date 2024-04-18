from flask import Flask, jsonify, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_database, database_exists
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app and configure CORS and database
app = Flask(__name__)
CORS(app)  # Apply CORS to all routes and methods
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/team1_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Check and create database if not exists
if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

# Define database models
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    user_pass = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
    user_admin = db.Column(db.Boolean, default=False)

    # Function to set password
    def set_password(self, password):
        self.user_pass = generate_password_hash(password)

    # Function to check for password match
    def check_password(self, password):
        return check_password_hash(self.user_pass, password)

class Recipes(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100))
    recipe_description = db.Column(db.String(100))
    recipe_ingredients = db.Column(db.String(100))
    recipe_instructions = db.Column(db.String(100))
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))

class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))

class RecipeTags(db.Model):
    recipeTag_id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))

# Function to add an admin user if not exists
def add_admin_user():
    if not Users.query.filter_by(user_id=0).first():  # Check if admin with user_id 0 exists
        admin_user = Users(user_id=0, user_name="admin", user_pass="admin", user_email="admin@example.com", user_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with user_id 0")
    else:
        print("Admin user already exists")

# Route to retrieve a recipe by ID
@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipes.query.filter_by(recipe_id=recipe_id).first()
    if recipe:
        recipe_data = {
            "id": recipe.recipe_id,
            "name": recipe.recipe_name,
            "description": recipe.recipe_description,
            "ingredients": recipe.recipe_ingredients,
            "instructions": recipe.recipe_instructions,
            "user_id": recipe.user_id
        }
        return jsonify(recipe_data)
    else:
        return jsonify({"error": "Recipe not found"}), 404

# Route to add a new recipe
@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    data = request.get_json()
    print(data) #DELETE LATER
    print("Received data:", data)  # Debug print
    try:
        new_recipe = Recipes(
            recipe_name=data['name'],
            recipe_description=data['description'],
            recipe_ingredients=data['ingredients'],
            recipe_instructions=data['instructions'],
            # user_id=data['user_id']
        )
        db.session.add(new_recipe)
        db.session.commit()
        response_data = {"message": "Recipe added successfully"}
        print("Sending response:", response_data)  # Debug print
        return jsonify(response_data), 201
    except Exception as e:
        error_message = {"error": str(e)}
        print("Sending error:", error_message)  # Debug print
        return jsonify(error_message), 400

# Start the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
        add_admin_user()  # Add an admin user
    app.run(debug=True)