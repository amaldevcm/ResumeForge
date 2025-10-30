from DB import Base, engine

try:
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
except Exception as e:
    print(f"Error initializing database: {str(e)}")
