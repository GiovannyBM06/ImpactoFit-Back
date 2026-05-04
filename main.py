"""
main.py
-------
Punto de entrada de la aplicación ImpactoFit API.

Responsabilidades:
    - Crear la instancia de FastAPI
    - Configurar CORS para Flutter
    - Registrar todos los routers
    - Configurar el manejador global de errores

Ejecutar en desarrollo:
    uvicorn main:app --reload

Ejecutar en producción:
    uvicorn main:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from api.controllers.AuthController import router as authRouter
from api.controllers.UsuarioController import router as usuarioRouter

app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para la aplicación móvil ImpactoFit",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)


# ── CORS ──────────────────────────────────────────────────────────────────────
# En desarrollo permitimos cualquier origen para facilitar las pruebas
# desde el emulador de Flutter y Postman.
# En producción se restringe al dominio real de la app.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://impactofit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Manejador global de excepciones ───────────────────────────────────────────

@app.exception_handler(Exception)
async def globalExceptionHandler(request: Request, exc: Exception):
    """
    Captura cualquier excepción no manejada y retorna un 500 limpio.
    En producción no expone el detalle del error interno.
    """
    detalle = str(exc) if settings.DEBUG else "Error interno del servidor"
    return JSONResponse(
        status_code=500,
        content={"detail": detalle},
    )


# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(authRouter)
app.include_router(usuarioRouter)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def healthCheck():
    return {"status": "ok", "app": settings.APP_NAME}