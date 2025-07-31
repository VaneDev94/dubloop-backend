from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.dubbing import router as dubbing_router

app = FastAPI(title="Dubloop Backend")

# Activar CORS para permitir conexión desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir a ["http://localhost:5173"] si usáis Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(dubbing_router, prefix="/dubbing", tags=["Dubbing"])