from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        credits=0  # Nuevo usuario empieza con 0 tokens/créditos
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def update_credits(db: Session, user_id: int, amount: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.credits += amount
        db.commit()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def set_user_google_account(db: Session, email: str) -> User:
    user = get_user_by_email(db, email)
    if not user:
        # Si el usuario no existe, lo creamos sin contraseña
        user = User(email=email, hashed_password=None, credits=0)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def get_or_create_google_user(db: Session, email: str) -> User:
    return set_user_google_account(db, email)


# --- verificación de email ---
import uuid
from typing import Optional

verification_tokens = {}

def generate_email_verification_token(email: str) -> str:
    token = str(uuid.uuid4())
    verification_tokens[token] = email
    return token

def verify_user_email(db: Session, token: str) -> Optional[User]:
    email = verification_tokens.get(token)
    if not email:
        return None

    user = get_user_by_email(db, email)
    if user:
        user.is_verified = True
        db.commit()
        verification_tokens.pop(token, None)
        return user
    return None