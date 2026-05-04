"""
authSchema.py
-------------
Schemas Pydantic para el módulo de autenticación.

Request  → datos que llegan desde Flutter al endpoint
Response → datos que se retornan a Flutter desde el endpoint
"""

from pydantic import BaseModel, EmailStr, field_validator


# ── Request ───────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def passwordNoVacio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La contraseña no puede estar vacía")
        return v


class RecuperarPasswordRequest(BaseModel):
    email: EmailStr


class ResetearPasswordRequest(BaseModel):
    token: str
    nuevaPassword: str

    @field_validator("nuevaPassword")
    @classmethod
    def validarPassword(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v


# ── Response ──────────────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    accessToken: str
    tokenType:   str
    rol:         str
    usuarioId:   int
    nombre:      str


class MensajeResponse(BaseModel):
    """Response genérico para operaciones que solo retornan confirmación."""
    mensaje: str