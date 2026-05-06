"""
clienteController.py
--------------------
Router del módulo cliente.

Endpoints:
    GET  /cliente/rutina                    → ver rutina activa con ejercicios
    POST /cliente/asistencia                → registrar ingreso al gimnasio
    GET  /cliente/clases                    → ver clases disponibles
    POST /cliente/clases/{claseId}/inscribir   → inscribirse a una clase
    PUT  /cliente/clases/{claseId}/cancelar    → cancelar inscripción
"""

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.Clienteschema import (
    AsistenciaRequest,
    AsistenciaResponse,
    InscripcionRequest,
    InscripcionResponse,
    RutinaResponse,
    EjercicioEnRutinaResponse,
    ClaseGrupalClienteResponse,
)
from api.middlewares.AuthMiddleware import requireRol
from core.dependencies import getClienteService
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.services.IClienteService import IClienteService

router = APIRouter(prefix="/cliente", tags=["Cliente"])


# ── Rutina ────────────────────────────────────────────────────────────────────

@router.get(
    "/rutina",
    response_model=RutinaResponse,
    summary="Ver mi rutina activa con todos los ejercicios",
)
async def verRutina(
    usuarioActual: Usuario = Depends(requireRol(RolEnum.CLIENTE)),
    service: IClienteService = Depends(getClienteService),
):
    try:
        rutina = await service.verRutina(usuarioActual.id)

        # Mapear ejecuciones al schema de respuesta
        ejercicios = [
            EjercicioEnRutinaResponse(
                ejecucionId=e.id,
                ejercicioId=e.ejercicioId,
                nombre=e.ejercicio.nombre,
                descripcion=e.ejercicio.descripcion,
                orden=e.orden,
                series=e.series,
                tipoMetrica=e.tipoMetrica,
                repeticiones=e.repeticiones,
                duracionSeg=e.duracionSeg,
                pesoKg=e.pesoKg,
                descansoSeg=e.descansoSeg,
            )
            for e in sorted(rutina.ejecuciones, key=lambda x: x.orden)
        ]

        return RutinaResponse(
            id=rutina.id,
            nombre=rutina.nombre,
            descripcion=rutina.descripcion,
            activa=rutina.activa,
            ejercicios=ejercicios,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# ── Asistencia ────────────────────────────────────────────────────────────────

@router.post(
    "/asistencia",
    response_model=AsistenciaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar mi ingreso al gimnasio",
)
async def registrarAsistencia(
    body: AsistenciaRequest,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.CLIENTE)),
    service: IClienteService = Depends(getClienteService),
):
    try:
        return await service.registrarAsistencia(
            clienteId=usuarioActual.id,
            observaciones=body.observaciones,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ── Clases grupales ───────────────────────────────────────────────────────────

@router.get(
    "/clases",
    response_model=list[ClaseGrupalClienteResponse],
    summary="Ver clases grupales disponibles",
)
async def verClasesDisponibles(
    _: Usuario = Depends(requireRol(RolEnum.CLIENTE)),
    service: IClienteService = Depends(getClienteService),
):
    return await service.obtenerClasesDisponibles()


@router.post(
    "/clases/{claseId}/inscribir",
    response_model=InscripcionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Inscribirme a una clase grupal",
)
async def inscribirseAClase(
    claseId: int,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.CLIENTE)),
    service: IClienteService = Depends(getClienteService),
):
    try:
        return await service.inscribirseAClase(
            clienteId=usuarioActual.id,
            claseId=claseId,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.put(
    "/clases/{claseId}/cancelar",
    response_model=InscripcionResponse,
    summary="Cancelar mi inscripción a una clase grupal",
)
async def cancelarInscripcion(
    claseId: int,
    usuarioActual: Usuario = Depends(requireRol(RolEnum.CLIENTE)),
    service: IClienteService = Depends(getClienteService),
):
    try:
        return await service.cancelarInscripcion(
            clienteId=usuarioActual.id,
            claseId=claseId,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )