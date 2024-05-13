How to test Team 1 Recipe App:

1) In the main project directory, set up venv by executing "python -m venv venv"
2) Activate venv by executing "./venv/Scripts/activate" (linux) or ".\venv\Scripts\activate" (windows)
3) cd into backend folder and install dependencies by executing "pip install -r requirements.txt"
3) Run Apache and MySQL modules through a program like XAMPP
4) Run app.py and navigate to http://127.0.0.1:5000/
5) See database changes through phpMyAdmin: http://localhost/phpmyadmin/index.php?route=/database/structure&db=team1_project


**** if you have run the project before on your system aka already have a sql table on your end, you need to do this ***

1) Activate Your Virtual Environment: Before running any commands, ensure that your virtual environment (if you are using one) is activated. This is crucial because Flask-Migrate and your application's dependencies should be installed in this environment. Activation usually looks like this:

Windows:
.\venv\Scripts\activate
macOS/Linux:
source venv/bin/activate

2) Set Flask Environment Variables: Flask-Migrate uses Flask CLI to run its commands, which requires your app to be discoverable by Flask. Set the FLASK_APP environment variable to point to your Flask application script:
set FLASK_APP=app.py  # On Windows
export FLASK_APP=app.py  # On macOS/Linux

3) Initialize Migrations: If you haven't already initialized migrations in your project, you need to set up the migrations directory. This directory will store all your migration scripts. Run:
flask db init
This command only needs to be run once per project to set up the migration environment.

4) Generate Migration Script: Generate an automatic migration by running:

flask db migrate -m "updated database"

This command scans your models and database and makes a migration script for differences it finds—in this case, adding the recipe_img_name column. The -m flag adds a message to your migration script, describing what the migration does.

5) Apply the Migration: To update your database schema according to the migration script, run:

flask db upgrade

This command applies the migration to your database, altering the schema by adding the new column.

6) Verify Changes: Optionally, you can log into your database and verify that the recipes table now includes the recipe_img_name column. Use a database management tool or command-line interface suitable for your database system to check this.