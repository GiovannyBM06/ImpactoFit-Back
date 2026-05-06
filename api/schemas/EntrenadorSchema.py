"""
entrenadorSchema.py
-------------------
Schemas Pydantic para el módulo de entrenadores.
"""

from pydantic import BaseModel, field_validator, model_validator
from domain.enums.TipoMetricaEnum import TipoMetricaEnum


# ── Rutina ────────────────────────────────────────────────────────────────────

class RutinaRequest(BaseModel):
    clienteId:   int
    nombre:      str
    descripcion: str | None = None

    @field_validator("nombre")
    @classmethod
    def validarNombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class RutinaResponse(BaseModel):
    id:           int
    clienteId:    int
    entrenadorId: int
    nombre:       str
    descripcion:  str | None
    activa:       bool

    model_config = {"from_attributes": True}


# ── Ejecucion ─────────────────────────────────────────────────────────────────

class EjecucionRequest(BaseModel):
    ejercicioId:  int
    orden:        int
    series:       int
    tipoMetrica:  TipoMetricaEnum
    repeticiones: int | None = None
    duracionSeg:  int | None = None
    pesoKg:       int | None = None
    descansoSeg:  int | None = None

    @model_validator(mode="after")
    def validarMetrica(self) -> "EjecucionRequest":
        if self.tipoMetrica == TipoMetricaEnum.REPETICIONES:
            if self.repeticiones is None:
                raise ValueError(
                    "Debe especificar repeticiones para el tipo REPETICIONES"
                )
        elif self.tipoMetrica == TipoMetricaEnum.TIEMPO:
            if self.duracionSeg is None:
                raise ValueError(
                    "Debe especificar duracionSeg para el tipo TIEMPO"
                )
        return self


class EjecucionUpdateRequest(BaseModel):
    """Todos los campos son opcionales para permitir partial update."""
    series:       int | None = None
    repeticiones: int | None = None
    duracionSeg:  int | None = None
    pesoKg:       int | None = None
    descansoSeg:  int | None = None
    orden:        int | None = None


class EjecucionResponse(BaseModel):
    id:           int
    rutinaId:     int
    ejercicioId:  int
    orden:        int
    series:       int
    tipoMetrica:  TipoMetricaEnum
    repeticiones: int | None
    duracionSeg:  int | None
    pesoKg:       int | None
    descansoSeg:  int | None

    model_config = {"from_attributes": True}


# ── Cliente (vista para entrenador) ───────────────────────────────────────────

class ClienteEntrenadorResponse(BaseModel):
    """Vista resumida de un cliente para el entrenador."""
    id:       int
    nombre:   str
    apellido: str
    email:    str

    model_config = {"from_attributes": True}