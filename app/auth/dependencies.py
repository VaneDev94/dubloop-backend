

from fastapi import Depends, HTTPException, status
from app.auth.auth_handler import get_current_user

def require_verified_email(current_user=Depends(get_current_user)):
    if not getattr(current_user, "is_verified", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu correo no está verificado. Por favor, verifica tu email para continuar."
        )
    return current_user