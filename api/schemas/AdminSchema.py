"""
adminSchema.py
--------------
Schemas Pydantic para el módulo de administrador.
"""

from datetime import date, datetime
from pydantic import BaseModel, field_validator
from domain.enums.TipoMembresiaEnum import TipoMembresiaEnum 
from domain.enums.EstadoMembresiaEnum import  EstadoMembresiaEnum


# ── Membresia ─────────────────────────────────────────────────────────────────

class MembresiaRequest(BaseModel):
    clienteId: int
    tipo:      TipoMembresiaEnum


class MembresiaResponse(BaseModel):
    id:               int
    usuarioId:        int
    tipo:             TipoMembresiaEnum
    estado:           EstadoMembresiaEnum
    fechaInicio:      date | None
    fechaVencimiento: date | None

    model_config = {"from_attributes": True}


# ── Pago ──────────────────────────────────────────────────────────────────────

class PagoRequest(BaseModel):
    membresiaId: int
    monto:       int
    notas:       str | None = None

    @field_validator("monto")
    @classmethod
    def validarMonto(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        return v


class PagoResponse(BaseModel):
    id:                int
    membresiaId:       int
    confirmadoPorId:   int
    monto:             int
    fechaPago:         datetime
    comprobanteCodigo: str | None
    notas:             str | None

    model_config = {"from_attributes": True}


# ── ClaseGrupal ───────────────────────────────────────────────────────────────

class ClaseGrupalRequest(BaseModel):
    entrenadorId: int
    nombre:       str
    fechaHora:    str   # ISO format: "2025-06-15T09:00:00"
    cupoMaximo:   int
    descripcion:  str | None = None

    @field_validator("cupoMaximo")
    @classmethod
    def validarCupo(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("El cupo máximo debe ser mayor a cero")
        return v

    @field_validator("nombre")
    @classmethod
    def validarNombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class ClaseGrupalResponse(BaseModel):
    id:                    int
    nombre:                str
    descripcion:           str | None
    entrenadorId:          int
    fechaHora:             datetime
    cupoMaximo:            int
    cupoActual:            int
    inscripcionesAbiertas: bool

    model_config = {"from_attributes": True}