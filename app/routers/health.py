from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Utils"])
def health_check():
    return {"status": "ok"}