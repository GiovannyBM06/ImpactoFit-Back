"""
usuarioSchema.py
----------------
Schemas Pydantic para el módulo de usuarios.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from domain.enums.RolEnum import RolEnum


# ── Request ───────────────────────────────────────────────────────────────────

class UsuarioRequest(BaseModel):
    nombre:   str
    apellido: str
    email:    EmailStr
    password: str
    rol:      RolEnum
    telefono: str | None = None

    @field_validator("password")
    @classmethod
    def validarPassword(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v

    @field_validator("nombre", "apellido")
    @classmethod
    def validarNombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        return v.strip()


class UsuarioUpdateRequest(BaseModel):
    """Para actualizar datos básicos. No permite cambiar rol ni password aquí."""
    nombre:   str | None = None
    apellido: str | None = None
    telefono: str | None = None


class AsignarEntrenadorRequest(BaseModel):
    clienteId:    int
    entrenadorId: int


# ── Response ──────────────────────────────────────────────────────────────────

class UsuarioResponse(BaseModel):
    id:        int
    nombre:    str
    apellido:  str
    email:     str
    telefono:  str | None
    rol:       RolEnum
    isActive:  bool
    createdAt: datetime

    model_config = {"from_attributes": True}


class AsignarEntrenadorResponse(BaseModel):
    mensaje:      str
    clienteId:    int
    entrenadorId: int