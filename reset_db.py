print('Resetting database...')
import db.sqlite3
# Reset the database
db.db.drop_all()
# Create the tables
db.db.create_all()
print('Database reset: success!')
