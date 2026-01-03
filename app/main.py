# Archivo principal de la aplicación
# Aquí se configura FastAPI y se agregan las rutas

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

# Crear la app de FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS - para que el frontend pueda hacer requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar las rutas de la API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    # Ruta principal, solo para verificar que la API funciona
    return {"message": "Technical Test Backend API"}

@app.get("/health")
def health_check():
    # Endpoint de health check para verificar que el servidor está vivo
    return {"status": "healthy"}
