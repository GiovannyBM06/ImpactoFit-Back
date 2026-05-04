"""
entrenadorController.py
-----------------------
Router del módulo entrenador.

Endpoints:
    GET    /entrenador/clientes                              → ver mis clientes
    POST   /entrenador/rutinas                               → crear rutina para cliente
    GET    /entrenador/rutinas/{clienteId}                   → ver rutina de un cliente
    POST   /entrenador/rutinas/{rutinaId}/ejercicios         → asignar ejercicio
    PUT    /entrenador/ejercicios/{ejecucionId}              → modificar ejercicio
    DELETE /entrenador/ejercicios/{ejecucionId}              → eliminar ejercicio
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.EntrenadorSchema import (
    RutinaRequest,
    RutinaResponse,
    EjecucionRequest,
    EjecucionUpdateRequest,
    EjecucionResponse,
    ClienteEntrenadorResponse,
)
from api.schemas.AuthSchema import MensajeResponse
from api.middlewares.AuthMiddleware import requireRol
from core.dependencies import getEntrenadorService
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.services.IEntrenadorService import IEntrenadorService

router = APIRouter(prefix="/entrenador", tags=["Entrenador"])


# ── Clientes ──────────────────────────────────────────────────────────────────

@router.get(
    "/clientes",
    response_model=list[ClienteEntrenadorResponse],
    summary="Ver mis clientes asignados",
)
async def verMisClientes(
    usuarioActual: Usuario = Depends(requireRol(RolEnum.ENTRENADOR)),
    service: IEntrenadorService = Depends(getEntrenadorService),
):
    return await service.verClientesAsignados(usuarioActual.id)


# ── Rutinas ───────────────────────────────────────────────────────────────────

@router.post(
    "/rutinas",
    response_model=RutinaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear rutina para un cliente",
)
async def crearRutina(
    body: RutinaRequest,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.ENTRENADOR)),
    service: IEntrenadorService = Depends(getEntrenadorService),
):
    try:
        return await service.crearRutina(
            entrenadorId=usuarioActual.id,
            clienteId=body.clienteId,
            nombre=body.nombre,
            descripcion=body.descripcion,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/rutinas/{clienteId}",
    response_model=RutinaResponse,
    summary="Ver la rutina activa de un cliente",
)
async def verRutinaDeCliente(
    clienteId: int,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.ENTRENADOR)),
    service: IEntrenadorService = Depends(getEntrenadorService),
):
    try:
        rutina = await service.verRutinaDeCliente(
            entrenadorId=usuarioActual.id,
            clienteId=clienteId,
        )
        if rutina is None:
            raise ValueError(
                f"El cliente {clienteId} no tiene rutina activa asignada por ti"
            )
        return rutina
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# ── Ejercicios ────────────────────────────────────────────────────────────────

@router.post(
    "/rutinas/{rutinaId}/ejercicios",
    response_model=EjecucionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Asignar un ejercicio del catálogo a una rutina",
)
async def asignarEjercicio(
    rutinaId: int,
    body: EjecucionRequest,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.ENTRENADOR)),
    service: IEntrenadorService = Depends(getEntrenadorService),
):
    try:
        return await service.asignarEjercicio(
            entrenadorId=usuarioActual.id,
            rutinaId=rutinaId,
            ejercicioId=body.ejercicioId,
            series=body.series,
            tipoMetrica=body.tipoMetrica.value,
            orden=body.orden,
            repeticiones=body.repeticiones,
            duracionSeg=body.duracionSeg,
            pesoKg=body.pesoKg,
            descansoSeg=body.descansoSeg,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put(
    "/ejercicios/{ejecucionId}",
    response_model=EjecucionResponse,
    summary="Modificar parámetros de un ejercicio en una rutina",
)
async def modificarEjercicio(
    ejecucionId: int,
    body: EjecucionUpdateRequest,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.ENTRENADOR)),
    service: IEntrenadorService = Depends(getEntrenadorService),
):
    try:
        return await service.modificarEjercicio(
            entrenadorId=usuarioActual.id,
            ejecucionId=ejecucionId,
            **body.model_dump(exclude_none=True),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/ejercicios/{ejecucionId}",
    response_model=MensajeResponse,
    summary="Eliminar un ejercicio de una rutina",
)
async def eliminarEjercicio(
    ejecucionId: int,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.ENTRENADOR)),
    service: IEntrenadorService = Depends(getEntrenadorService),
):
    try:
        await service.eliminarEjercicio(
            entrenadorId=usuarioActual.id,
            ejecucionId=ejecucionId,
        )
        return {"mensaje": f"Ejercicio {ejecucionId} eliminado de la rutina"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )