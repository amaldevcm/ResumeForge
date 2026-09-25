import uuid
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from DB import SessionLocal
from Models.Models import User
from datetime import datetime
import re

def user_to_dict(user):
    return {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_date": user.created_date,
        "updated_date": user.updated_date,
        "oauth_provider": user.oauth_provider,
        "oauth_id": user.oauth_id,
    }

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

    if using_password and len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    # If OAuth is provided but email doesn't match expected oauth flow, still allow (email is required already)
    # save user to postgres
    try:
        db = SessionLocal()
        createdDate = datetime.now().isoformat()
        new_user = User(
            id = str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password) if using_password else None,
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
    if 'email' in update_data:
        email = update_data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        existing = get_user_by_email(email)
        if existing and str(existing.id) != str(user_id):
            raise ValueError("Email already in use")

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
    except ValueError:
        raise
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

def get_user_by_id(user_id):
    try:
        db = SessionLocal()
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")
    finally:
        db.close()


def login_user(email, password=None, oauth_provider=None, oauth_id=None):
    try:
        db = SessionLocal()
        # Base query to find user by email
        user = db.query(User).filter(User.email == email).first()

        # Check authentication method. The error messages below are
        # deliberately identical whether the email doesn't exist or the
        # credentials just don't match, so a caller can't use them to
        # enumerate which emails have accounts.
        if oauth_provider and oauth_id:
            # OAuth login
            if user and getattr(user, 'oauth_provider', None) == oauth_provider and \
               getattr(user, 'oauth_id', None) == oauth_id:

                return user
            raise ValueError("Invalid OAuth credentials")
        elif password:
            # Password login
            if user and user.password and check_password_hash(user.password, password):
                return user
            raise ValueError("Invalid email or password")
        else:
            raise ValueError("Either password or OAuth credentials must be provided")

    except ValueError:
        raise
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

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        raise ValueError("Not authenticated")
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    return user_to_dict(user)

def change_password(user_id, current_password, new_password):
    if not new_password or len(new_password) < 8:
        raise ValueError("New password must be at least 8 characters")
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        if not user.password or not check_password_hash(user.password, current_password):
            raise ValueError("Current password is incorrect")
        user.password = generate_password_hash(new_password)
        user.updated_date = datetime.now().isoformat()
        db.commit()
        return True
    except ValueError:
        raise
    except Exception as e:
        db.rollback()
        raise Exception(f"Error changing password: {str(e)}")
    finally:
        db.close()

def delete_user(user_id):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        db.delete(user)
        db.commit()
        return True
    except ValueError:
        raise
    except Exception as e:
        db.rollback()
        raise Exception(f"Error deleting user: {str(e)}")
    finally:
        db.close()

def logout_user():
    session.pop('user_id', None)
    return True
