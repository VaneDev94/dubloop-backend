

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.models.user import User
from sqlalchemy.orm import Session
import os

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

 # Hashea la contraseña usando bcrypt
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

 # Verifica si la contraseña proporcionada coincide con la contraseña hasheada
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

 # Crea un token JWT con los datos proporcionados y una expiración
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

 # Verifica si el usuario existe y si la contraseña es correcta
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


 # Registra un nuevo usuario en la base de datos con su contraseña hasheada
def register_user(db: Session, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password, credits=0)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user