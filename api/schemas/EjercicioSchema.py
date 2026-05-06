"""
ejercicioSchema.py
------------------
Schemas para el catálogo de ejercicios.
"""

from pydantic import BaseModel, field_validator


class EjercicioRequest(BaseModel):
    nombre:      str
    descripcion: str | None = None

    @field_validator("nombre")
    @classmethod
    def validarNombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class EjercicioUpdateRequest(BaseModel):
    nombre:      str | None = None
    descripcion: str | None = None


class EjercicioResponse(BaseModel):
    id:          int
    nombre:      str
    descripcion: str | None

    model_config = {"from_attributes": True}