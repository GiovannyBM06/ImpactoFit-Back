"""
ejercicioController.py
----------------------
Router del catálogo de ejercicios.

Endpoints:
    GET    /ejercicios           → listar catálogo (entrenador/admin)
    POST   /ejercicios           → crear ejercicio (entrenador/admin)
    GET    /ejercicios/{id}      → obtener ejercicio por id
    PUT    /ejercicios/{id}      → actualizar ejercicio (entrenador/admin)
    DELETE /ejercicios/{id}      → eliminar ejercicio (admin)
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.EjercicioSchema import (
    EjercicioRequest,
    EjercicioUpdateRequest,
    EjercicioResponse,
)
from api.schemas.AuthSchema import MensajeResponse
from api.middlewares.AuthMiddleware import requireRol
from core.dependencies import getEjercicioService
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.services.IEjercicioService import IEjercicioService

router = APIRouter(prefix="/ejercicios", tags=["Catálogo de Ejercicios"])


@router.get(
    "",
    response_model=list[EjercicioResponse],
    summary="Listar catálogo completo de ejercicios",
)
async def listarEjercicios(
    _: Usuario = Depends(requireRol(RolEnum.ENTRENADOR, RolEnum.ADMINISTRADOR)),
    service: IEjercicioService = Depends(getEjercicioService),
):
    return await service.obtenerTodos()


@router.post(
    "",
    response_model=EjercicioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear ejercicio en el catálogo",
)
async def crearEjercicio(
    body: EjercicioRequest,
    _: Usuario = Depends(requireRol(RolEnum.ENTRENADOR, RolEnum.ADMINISTRADOR)),
    service: IEjercicioService = Depends(getEjercicioService),
):
    try:
        return await service.crearEjercicio(body.nombre, body.descripcion)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{ejercicioId}",
    response_model=EjercicioResponse,
    summary="Obtener ejercicio por id",
)
async def obtenerEjercicio(
    ejercicioId: int,
    _: Usuario = Depends(requireRol(RolEnum.ENTRENADOR, RolEnum.ADMINISTRADOR)),
    service: IEjercicioService = Depends(getEjercicioService),
):
    try:
        return await service.obtenerPorId(ejercicioId)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{ejercicioId}",
    response_model=EjercicioResponse,
    summary="Actualizar ejercicio del catálogo",
)
async def actualizarEjercicio(
    ejercicioId: int,
    body: EjercicioUpdateRequest,
    _: Usuario = Depends(requireRol(RolEnum.ENTRENADOR, RolEnum.ADMINISTRADOR)),
    service: IEjercicioService = Depends(getEjercicioService),
):
    try:
        return await service.actualizarEjercicio(
            ejercicioId,
            nombre=body.nombre,
            descripcion=body.descripcion,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{ejercicioId}",
    response_model=MensajeResponse,
    summary="Eliminar ejercicio del catálogo",
)
async def eliminarEjercicio(
    ejercicioId: int,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IEjercicioService = Depends(getEjercicioService),
):
    try:
        await service.eliminarEjercicio(ejercicioId)
        return {"mensaje": f"Ejercicio {ejercicioId} eliminado del catálogo"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )