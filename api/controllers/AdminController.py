"""
adminController.py
------------------
Router del módulo administrador.

Endpoints:
    GET  /admin/clientes                        → listar todos los clientes
    GET  /admin/membresias                      → listar todas las membresías
    POST /admin/membresias                      → crear membresía para cliente
    POST /admin/membresias/{membresiaId}/activar → confirmar pago y activar
    POST /admin/clases                          → crear clase grupal
    GET  /admin/entrenadores                    → listar entrenadores disponibles
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.AdminSchema import (
    MembresiaRequest,
    MembresiaResponse,
    PagoRequest,
    PagoResponse,
    ClaseGrupalRequest,
    ClaseGrupalResponse,
)
from api.schemas.UsuarioSchema import UsuarioResponse
from api.middlewares.AuthMiddleware import requireRol
from core.dependencies import getAdminService
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.services.IAdminService import IAdminService

router = APIRouter(prefix="/admin", tags=["Administrador"])


# ── Clientes ──────────────────────────────────────────────────────────────────

@router.get(
    "/clientes",
    response_model=list[UsuarioResponse],
    summary="Listar todos los clientes",
)
async def listarClientes(
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IAdminService = Depends(getAdminService),
):
    return await service.verTodosLosClientes()


# ── Entrenadores ──────────────────────────────────────────────────────────────

@router.get(
    "/entrenadores",
    response_model=list[UsuarioResponse],
    summary="Listar todos los entrenadores",
)
async def listarEntrenadores(
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IAdminService = Depends(getAdminService),
):
    return await service.verEntrenadores()


# ── Membresías ────────────────────────────────────────────────────────────────

@router.get(
    "/membresias",
    response_model=list[MembresiaResponse],
    summary="Listar todas las membresías",
)
async def listarMembresias(
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IAdminService = Depends(getAdminService),
):
    return await service.verTodasLasMembresias()


@router.post(
    "/membresias",
    response_model=MembresiaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear membresía en estado PENDIENTE para un cliente",
)
async def crearMembresia(
    body: MembresiaRequest,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IAdminService = Depends(getAdminService),
):
    try:
        return await service.crearMembresia(
            clienteId=body.clienteId,
            tipo=body.tipo.value,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/membresias/{membresiaId}/activar",
    response_model=PagoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Confirmar pago y activar membresía (Strategy + Observer)",
)
async def confirmarPagoYActivarMembresia(
    membresiaId: int,
    body: PagoRequest,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IAdminService = Depends(getAdminService),
):
    try:
        return await service.confirmarPagoYActivarMembresia(
            membresiaId=membresiaId,
            adminId=usuarioActual.id,
            monto=body.monto,
            notas=body.notas,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ── Clases grupales ───────────────────────────────────────────────────────────

@router.post(
    "/clases",
    response_model=ClaseGrupalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una clase grupal",
)
async def crearClaseGrupal(
    body: ClaseGrupalRequest,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IAdminService = Depends(getAdminService),
):
    try:
        return await service.crearClaseGrupal(
            entrenadorId=body.entrenadorId,
            nombre=body.nombre,
            fechaHora=body.fechaHora,
            cupoMaximo=body.cupoMaximo,
            descripcion=body.descripcion,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )