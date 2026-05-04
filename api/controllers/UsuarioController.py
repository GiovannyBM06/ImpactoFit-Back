"""
usuarioController.py
--------------------
Router de usuarios.

Endpoints:
    POST   /usuarios                        → crear usuario (admin)
    GET    /usuarios                        → listar todos los usuarios (admin)
    GET    /usuarios/{usuarioId}            → obtener usuario por id (admin)
    PUT    /usuarios/{usuarioId}            → actualizar datos básicos (admin)
    DELETE /usuarios/{usuarioId}            → eliminar usuario (admin)
    POST   /usuarios/asignar-entrenador     → asignar entrenador a cliente (admin)
    POST   /usuarios/desvincular-entrenador → desvincular entrenador de cliente (admin)
    GET    /usuarios/me                     → obtener perfil propio (cualquier rol)
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.UsuarioSchema import (
    UsuarioRequest,
    UsuarioUpdateRequest,
    UsuarioResponse,
    AsignarEntrenadorRequest,
    AsignarEntrenadorResponse,
)
from api.schemas.AuthSchema import MensajeResponse
from api.middlewares.AuthMiddleware import getCurrentUsuario, requireRol
from core.dependencies import getUsuarioService, getAdminService
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.services.IUsuarioService import IUsuarioService
from domain.interfaces.services.IAdminService import IAdminService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ── Perfil propio (cualquier rol autenticado) ─────────────────────────────────

@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Obtener perfil del usuario autenticado",
)
async def obtenerPerfil(
    usuarioActual: Usuario = Depends(getCurrentUsuario),
):
    return usuarioActual


# ── CRUD (solo administrador) ─────────────────────────────────────────────────

@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
)
async def crearUsuario(
    body: UsuarioRequest,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IUsuarioService = Depends(getUsuarioService),
):
    try:
        return await service.crearUsuario(
            nombre=body.nombre,
            apellido=body.apellido,
            email=body.email,
            password=body.password,
            rol=body.rol.value,
            telefono=body.telefono,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[UsuarioResponse],
    summary="Listar todos los usuarios",
)
async def listarUsuarios(
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IUsuarioService = Depends(getUsuarioService),
):
    return await service.obtenerTodos()


@router.get(
    "/{usuarioId}",
    response_model=UsuarioResponse,
    summary="Obtener un usuario por id",
)
async def obtenerUsuario(
    usuarioId: int,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IUsuarioService = Depends(getUsuarioService),
):
    try:
        return await service.obtenerPorId(usuarioId)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{usuarioId}",
    response_model=UsuarioResponse,
    summary="Actualizar datos básicos de un usuario",
)
async def actualizarUsuario(
    usuarioId: int,
    body: UsuarioUpdateRequest,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IUsuarioService = Depends(getUsuarioService),
):
    try:
        return await service.actualizar(usuarioId, body.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{usuarioId}",
    response_model=MensajeResponse,
    summary="Eliminar un usuario",
)
async def eliminarUsuario(
    usuarioId: int,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IUsuarioService = Depends(getUsuarioService),
):
    try:
        eliminado = await service.eliminar(usuarioId)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró un usuario con id {usuarioId}",
            )
        return {"mensaje": f"Usuario {usuarioId} eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ── Asignaciones (solo administrador) ────────────────────────────────────────

@router.post(
    "/asignar-entrenador",
    response_model=AsignarEntrenadorResponse,
    summary="Asignar un entrenador a un cliente",
)
async def asignarEntrenador(
    body: AsignarEntrenadorRequest,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    service: IUsuarioService = Depends(getUsuarioService),
):
    try:
        return await service.asignarEntrenador(body.clienteId, body.entrenadorId)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/desvincular-entrenador",
    response_model=MensajeResponse,
    summary="Desvincular un entrenador de un cliente",
)
async def desvincularEntrenador(
    body: AsignarEntrenadorRequest,
    _: Usuario = Depends(requireRol(RolEnum.ADMINISTRADOR)),
    adminService: IAdminService = Depends(getAdminService),
):
    try:
        return await adminService.desvincularEntrenador(
            body.clienteId,
            body.entrenadorId,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )