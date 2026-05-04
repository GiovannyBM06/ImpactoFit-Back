"""
authController.py
-----------------
Router de autenticación.

Endpoints:
    POST /auth/login                → iniciar sesión
    POST /auth/logout               → cerrar sesión
    POST /auth/recuperar-password   → solicitar recuperación por email
    POST /auth/resetear-password    → resetear con token del email
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.AuthSchema import (
    LoginRequest,
    TokenResponse,
    RecuperarPasswordRequest,
    ResetearPasswordRequest,
    MensajeResponse,
)
from api.middlewares.AuthMiddleware import oauth2Scheme
from core.dependencies import getAuthService
from domain.interfaces.services.IAuthService import IAuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
)
async def login(
    body: LoginRequest,
    service: IAuthService = Depends(getAuthService),
):
    try:
        return await service.login(body.email, body.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/logout",
    response_model=MensajeResponse,
    summary="Cerrar sesión",
)
async def logout(
    token: str = Depends(oauth2Scheme),
    service: IAuthService = Depends(getAuthService),
):
    try:
        return await service.logout(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/recuperar-password",
    response_model=MensajeResponse,
    summary="Solicitar recuperación de contraseña por email",
)
async def recuperarPassword(
    body: RecuperarPasswordRequest,
    service: IAuthService = Depends(getAuthService),
):
    # No lanza excepción: siempre retorna el mismo mensaje por seguridad
    return await service.solicitarRecuperacionPassword(body.email)


@router.post(
    "/resetear-password",
    response_model=MensajeResponse,
    summary="Resetear contraseña con token del email",
)
async def resetearPassword(
    body: ResetearPasswordRequest,
    service: IAuthService = Depends(getAuthService),
):
    try:
        return await service.resetearPassword(body.token, body.nuevaPassword)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )