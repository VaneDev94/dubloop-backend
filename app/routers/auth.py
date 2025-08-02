# app/router/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.auth.auth_service import register_user, authenticate_user
from app.database import get_db
from app.models.user import User
from app.services.user_services import generate_email_verification_token, verify_user_email

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    token = generate_email_verification_token(user.email)
    print(f"Verifica tu email haciendo clic aquí: http://localhost:8000/verify-email/{token}")
    
    return register_user(user, db)

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(user.email, user.password, db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = verify_user_email(db, token)
    if not user:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    return JSONResponse(content={"message": "Email verificado correctamente"})