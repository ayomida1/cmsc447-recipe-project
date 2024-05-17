How to test Team 1 Recipe App:

1) In the main project directory, set up venv by executing "python -m venv venv"
2) Activate venv by executing "./venv/Scripts/activate" (linux) or ".\venv\Scripts\activate" (windows)
3) cd into backend folder and install dependencies by executing "pip install -r requirements.txt"
3) Run Apache and MySQL modules through a program like XAMPP
4) Run app.py and navigate to http://127.0.0.1:5000/
5) See database changes through phpMyAdmin: http://localhost/phpmyadmin/index.php?route=/database/structure&db=team1_project


**** Debugging: SQL Errors - will happen if you have run the project before but not properly reloaded your updated changes to SQL tables before re-running ***

1) Go to phpMyAdmin: http://localhost/phpmyadmin/index.php?route=/database/structure&db=team1_project and dump all tables

2) Reload the project