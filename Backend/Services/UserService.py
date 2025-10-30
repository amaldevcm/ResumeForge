from DB import SessionLocal
from Models.Models import User

def create_user(user_data):
    # Validate and process user_data
    if not user_data.get("email"):
        raise ValueError("Email is required")
    if not user_data.get("name"):
        raise ValueError("Name is required")
    if not user_data.get("password"):
        raise ValueError("Password is required")

    # save user to postgres
    try:
        db = SessionLocal()
        new_user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"])
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating user: {str(e)}")
        return None
    finally:
        db.close()

    return new_user


def update_user(user_id, update_data):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating user: {str(e)}")
    finally:
        db.close()

def get_user_by_email(email):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        return user
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")
    finally:
        db.close()

    return None

def login_user(email, password):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.email == email, User.password == password).first()
        return user
    except Exception as e:
        raise Exception(f"Error during login: {str(e)}")
    finally:
        db.close()

    return None

def signup_user(user_data):
    existing_user = get_user_by_email(user_data.get("email"))
    if existing_user:
        raise ValueError("User with this email already exists")

    new_user = create_user(user_data)
    return new_user