from flask import Flask, jsonify, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import session
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_database, database_exists
from werkzeug.security import generate_password_hash, check_password_hash
from search import indexRecipe #for elasticsearch indexing
from search import searchRecipes

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

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search term from query parameters
    if query:
        recipe_ids = searchRecipes(query)
        # Assuming you want to return full recipe details, not just IDs:
        recipes = Recipes.query.filter(Recipes.recipe_id.in_(recipe_ids)).all()
        recipes_data = [{
            "id": recipe.recipe_id,
            "name": recipe.recipe_name,
            "description": recipe.recipe_description,
            "ingredients": recipe.recipe_ingredients,
            "instructions": recipe.recipe_instructions
        } for recipe in recipes]
        return jsonify(recipes_data)
    else:
        return jsonify([]), 400  # Bad request if no query provided
    
# Route to retrieve a recipe by ID
@app.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        recipes = Recipes.query.all()
        recipes_data = [{
            "id": recipe.recipe_id,
            "name": recipe.recipe_name,
            "description": recipe.recipe_description,
            "ingredients": recipe.recipe_ingredients,
            "instructions": recipe.recipe_instructions,
           # "user_id": recipe.user_id ADD BACK LATER
        } for recipe in recipes]
        return jsonify(recipes_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

        # Index the new recipe in Elasticsearch
        indexRecipe(str(new_recipe.recipe_id), new_recipe.recipe_name)

        return jsonify(response_data), 201
    except Exception as e:
        error_message = {"error": str(e)}
        print("Sending error:", error_message)  # Debug print
        return jsonify(error_message), 400

#function to delete recipe from database
@app.route('/delete_recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        recipe = Recipes.query.get(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({"message": "Recipe deleted successfully"}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Function to register a user 
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = Users(
            user_name=data['username'],
            user_pass=data['password'],
            user_email=data['email'],
    )
    
    # Check if username or email already exists
    existing_user = Users.query.filter((Users.user_name == username) | (Users.user_email == email)).first()
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 400
    
    # Create new user
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Function to log in user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Retrieve user from the database by username
    user = Users.query.filter_by(user_name=username).first()

    print("User:", user)
    
    if user is not None and user.user_pass == password:
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Function to log out user
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # clear the session

    return jsonify({'message': 'Logged out successfully'}), 200

# Start the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
        add_admin_user()  # Add an admin user
    app.run(debug=True)