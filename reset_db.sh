find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
# rm db.sqlite3
$ [ -f db.sqlite3 ] && rm db.sqlite3 || echo "The file db.sqlite3 does not exist in your directory or has already been removed."
python manage.py makemigrations
python manage.py migrate
echo "The database has been reset. Please remember to create a new superuser by typing in the command: \"python manage.py createsuperuser\" before running the server."
