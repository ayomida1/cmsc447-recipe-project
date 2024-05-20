from flask import Flask, jsonify, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import session
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_database, database_exists
from werkzeug.security import generate_password_hash, check_password_hash
from search import indexRecipe, searchRecipes, removeRecipe
import csv
from flask_migrate import Migrate


# Initialize Flask app and configure CORS and database
app = Flask(__name__)
CORS(app)  # Apply CORS to all routes and methods
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/team1_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db) #migrates the new db if any columns existing tables are changed

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
    saved_recipes = db.Column(db.String(1000), default='') 

    # Function to set password
    def set_password(self, password):
        self.user_pass = generate_password_hash(password)

    # Function to check for password match
    def check_password(self, password):
        return check_password_hash(self.user_pass, password)

class Recipes(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100))
    recipe_description = db.Column(db.String(1000))
    recipe_ingredients = db.Column(db.String(1000))
    recipe_instructions = db.Column(db.String(1000))
    recipe_tags = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_img_name = db.Column(db.String(100))

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))

# Function to add an admin user if not exists
def add_admin_user():
    if not Users.query.filter_by(user_name="admin").first():  # Check if admin exists
        admin_user = Users(user_id = 0, user_name="admin", user_pass="admin", user_email="admin@example.com", user_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created")
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
            "user_id": recipe.user_id,
            "recipe_img_name" : recipe.recipe_img_name
        } for recipe in recipes]
        return jsonify(recipes_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#Function checks if logged if the currently logged user exists, fixes a major bug    
@app.route('/user_exists', methods=['GET'])
def user_exists():
    username = request.args.get('username')
    if not username:
        return jsonify({'exists': False})

    user = Users.query.filter_by(user_name=username).first()
    if user:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})


# Route to add a new recipe
@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    data = request.get_json()
    username = data.get('username')  # Get username from the data passed

    if not username:
        return jsonify({'error': 'You must be logged in to add recipes'}), 401

    user = Users.query.filter_by(user_name=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        new_recipe = Recipes(
            recipe_name=data['name'],
            recipe_description=data['description'],
            recipe_ingredients=data['ingredients'],
            recipe_instructions=data['instructions'],
            recipe_tags=','.join(data['tags']),  # Assuming tags are sent as a list
            user_id=user.user_id  # Use the user ID fetched from the database
        )
        db.session.add(new_recipe)
        db.session.commit()
        indexRecipe(str(new_recipe.recipe_id), new_recipe.recipe_name, new_recipe.recipe_tags)
        return jsonify({"message": "Recipe added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#function to delete recipe from database
@app.route('/delete_recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    data = request.get_json()  # Assuming username is passed in the body of the delete request
    username = data.get('username')
    if not username:
        return jsonify({'error': 'You must be logged in to delete recipes'}), 401

    user = Users.query.filter_by(user_name=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    recipe = Recipes.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    if recipe.user_id != user.user_id:
        return jsonify({'error': 'Unauthorized to delete this recipe'}), 403

    try:
        recipe = Recipes.query.get(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            removeRecipe(str(recipe_id))
            return jsonify({"message": "Recipe deleted successfully"}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


#Function to edit existing recipe
@app.route('/update_recipe/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    username = data.get('username')
    print("Username passed into updateRecipe:", username)
    if not username:
        return jsonify({'error': 'You must be logged in to update recipes'}), 401

    user = Users.query.filter_by(user_name=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    recipe = Recipes.query.get(recipe_id)
    if recipe.user_id != user.user_id:
        return jsonify({'error': 'Unauthorized to edit this recipe'}), 403

    try:
        recipe.recipe_name = data.get('name', recipe.recipe_name)
        recipe.recipe_description = data.get('description', recipe.recipe_description)
        recipe.recipe_ingredients = data.get('ingredients', recipe.recipe_ingredients)
        recipe.recipe_instructions = data.get('instructions', recipe.recipe_instructions)
        db.session.commit()
        return jsonify({"message": "Recipe updated successfully"}), 200
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
    existing_user = Users.query.filter((Users.user_name == new_user.user_name) | (Users.user_email == new_user.user_email)).first()
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

#Function to save a recipe
@app.route('/save_recipe/<int:recipe_id>', methods=['POST'])
def save_recipe(recipe_id):
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'error': 'You must be logged in to save recipes'}), 401

    user = Users.query.filter_by(user_name=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    saved_recipes = user.saved_recipes.split(',')
    if str(recipe_id) not in saved_recipes:
        saved_recipes.append(str(recipe_id))
        user.saved_recipes = ','.join(saved_recipes)
        db.session.commit()

    return jsonify({"message": "Recipe saved successfully"}), 200


# Function to fetch saved recipes
@app.route('/saved_recipes', methods=['GET'])
def get_saved_recipes():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'You must be logged in to view saved recipes'}), 401

    user = Users.query.filter_by(user_name=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    saved_recipes_ids = user.saved_recipes.split(',')
    saved_recipes = Recipes.query.filter(Recipes.recipe_id.in_(saved_recipes_ids)).all()

    recipes_data = [{
        "id": recipe.recipe_id,
        "name": recipe.recipe_name,
        "description": recipe.recipe_description,
        "ingredients": recipe.recipe_ingredients,
        "instructions": recipe.recipe_instructions,
        "user_id": recipe.user_id,
        "recipe_img_name": recipe.recipe_img_name
    } for recipe in saved_recipes]

    return jsonify(recipes_data)

def populate_recipes():
    if Recipes.query.count() == 0:
        default_recipes = []
        with open('food.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row if present
            for row in reader:
                if len(row) < 6:  # Ensure row has enough columns, adjust the index as needed
                    continue
                ingredients_field = row[5]  # Assuming ingredients are in the 6th column (index 5)
                # Remove square brackets and split by ','
                ingredients = ingredients_field.replace('[\'', '').replace(']', '').split("', '")
                formatted_ingredients = "\n".join(f"- {item.strip()}" for item in ingredients)
                recipe = Recipes(
                    recipe_name=row[1],
                    recipe_instructions=row[3],  # Adjust indices as necessary
                    recipe_ingredients=formatted_ingredients,  # Use formatted ingredients
                    recipe_img_name=row[4] + ".jpg",  # Image name from CSV
                )
                default_recipes.append(recipe)
                if len(default_recipes) == 52:
                    break
        db.session.add_all(default_recipes)
        db.session.commit()
        
        for recipe in default_recipes:
            indexRecipe(str(recipe.recipe_id), recipe.recipe_name, recipe.recipe_tags)

# Start the Flask app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
        populate_recipes() # fill the db with recipes
        add_admin_user()  # Add an admin user
    app.run(debug=True)