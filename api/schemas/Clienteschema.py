"""
clienteSchema.py
----------------
Schemas Pydantic para el módulo de clientes.
"""

from datetime import date, datetime
from pydantic import BaseModel, field_validator
from domain.enums.TipoMetricaEnum import TipoMetricaEnum


# ── Asistencia ────────────────────────────────────────────────────────────────

class AsistenciaRequest(BaseModel):
    observaciones: str | None = None


class AsistenciaResponse(BaseModel):
    id:            int
    usuarioId:     int
    fecha:         date
    horaRegistro:  datetime
    observaciones: str | None

    model_config = {"from_attributes": True}


# ── Inscripcion ───────────────────────────────────────────────────────────────

class InscripcionRequest(BaseModel):
    claseId: int


class InscripcionResponse(BaseModel):
    id:               int
    usuarioId:        int
    claseId:          int
    fechaInscripcion: datetime
    cancelada:        bool

    model_config = {"from_attributes": True}


# ── Ejecucion (vista dentro de la rutina) ─────────────────────────────────────

class EjercicioEnRutinaResponse(BaseModel):
    """Vista de un ejercicio dentro de la rutina del cliente."""
    ejecucionId:  int
    ejercicioId:  int
    nombre:       str
    descripcion:  str | None
    orden:        int
    series:       int
    tipoMetrica:  TipoMetricaEnum
    repeticiones: int | None
    duracionSeg:  int | None
    pesoKg:       int | None
    descansoSeg:  int | None

    model_config = {"from_attributes": True}


# ── Rutina ────────────────────────────────────────────────────────────────────

class RutinaResponse(BaseModel):
    id:           int
    nombre:       str
    descripcion:  str | None
    activa:       bool
    ejercicios:   list[EjercicioEnRutinaResponse]

    model_config = {"from_attributes": True}


# ── ClaseGrupal (vista para cliente) ──────────────────────────────────────────

class ClaseGrupalClienteResponse(BaseModel):
    id:                   int
    nombre:               str
    descripcion:          str | None
    fechaHora:            datetime
    cupoMaximo:           int
    cupoActual:           int
    inscripcionesAbiertas: bool

    model_config = {"from_attributes": True}