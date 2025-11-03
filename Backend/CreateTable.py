from DB import Base, engine
from Models.Models import *

'''
This script creates all the tables defined in the Models.py file.
It uses SQLAlchemy to create the tables in the database specified
in the DB.py file.
just run this script once to set up the database schema.
'''

try:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
except Exception as e:
    print(f"Error creating database tables: {str(e)}")

