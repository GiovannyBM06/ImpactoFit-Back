"""
dependencies.py
---------------
Registro de dependencias para inyección en FastAPI (Depends).

Este archivo es el equivalente al contenedor de DI de .NET (Program.cs).
Centraliza cómo se construye cada servicio y qué implementaciones
concretas se usan para cada interfaz.

Uso en un router:
    from core.dependencies import getUsuarioService

    @router.post("/usuarios")
    def crearUsuario(
        body: UsuarioRequest,
        service: IUsuarioService = Depends(getUsuarioService)
    ):
        return service.crearUsuario(...)

Por qué esta centralización importa:
    Si se cambia UsuarioRepository por una implementación distinta
    (por ejemplo, para tests), se cambia solo aquí.
    Los controllers no se tocan.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from dataAccess.context.database import getDb
from dataAccess.repositories.UsuarioRepository import UsuarioRepository
from domain.interfaces.services.IUsuarioService import IUsuarioService
from domain.services.UsuarioService import UsuarioService


def getUsuarioService(
    db: AsyncSession = Depends(getDb)
) -> IUsuarioService:
    """
    Construye el servicio de usuarios con sus dependencias inyectadas.

    Cadena de construcción:
        getDb() → AsyncSession
        AsyncSession → UsuarioRepository (implementación concreta)
        UsuarioRepository → UsuarioService
        UsuarioService → retornado al controller como IUsuarioService
    """
    repo = UsuarioRepository(db)
    return UsuarioService(repo)