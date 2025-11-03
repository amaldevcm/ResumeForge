from DB import SessionLocal
from Models.Models import User
from datetime import datetime
import re

def create_user(user_data):
    # Validate and process user_data

    email = user_data.get("email")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    password = user_data.get("password")
    oauth_provider = user_data.get("oauth_provider")
    oauth_id = user_data.get("oauth_id")

    if not email:
        raise ValueError("Email is required")
    if not first_name or not last_name:
        raise ValueError("First and last name are required")

    # Simple email format validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email format")

    # Determine authentication method(s)
    using_oauth = bool(oauth_provider and oauth_id)
    using_password = bool(password)

    # Require at least one auth method; if both are missing, error
    if not (using_oauth or using_password):
        raise ValueError("Either OAuth credentials (oauth_provider and oauth_id) or a password must be provided")

    # If OAuth is provided but email doesn't match expected oauth flow, still allow (email is required already)
    # save user to postgres
    try:
        db = SessionLocal()
        createdDate = datetime.now().isoformat()
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password if using_password else None,
            created_date=createdDate,
            updated_date=createdDate,
        )

        # attach oauth fields only if provided (keeps compatibility if model lacks them)
        if using_oauth:
            try:
                setattr(new_user, "oauth_provider", oauth_provider)
                setattr(new_user, "oauth_id", oauth_id)
            except Exception:
                # ignore if model doesn't have these fields
                pass

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating user: {str(e)}")
    finally:
        db.close()

    return new_user


def update_user(user_id, update_data):
    try:
        update_data['updated_date'] = datetime.now().isoformat()
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


def login_user(email, password=None, oauth_provider=None, oauth_id=None):
    try:
        db = SessionLocal()
        
        # Base query to find user by email
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise ValueError("User not found")

        # Check authentication method
        if oauth_provider and oauth_id:
            # OAuth login
            if getattr(user, 'oauth_provider', None) == oauth_provider and \
               getattr(user, 'oauth_id', None) == oauth_id:
                return user
            raise ValueError("Invalid OAuth credentials")
        elif password:
            # Password login
            if user.password == password:
                return user
            raise ValueError("Invalid password")
        else:
            raise ValueError("Either password or OAuth credentials must be provided")
            
    except Exception as e:
        raise Exception(f"Error during login: {str(e)}")
    finally:
        db.close()

def signup_user(user_data):
    existing_user = get_user_by_email(user_data.get("email"))
    if existing_user:
        raise ValueError("User with this email already exists")

    new_user = create_user(user_data)
    return new_user