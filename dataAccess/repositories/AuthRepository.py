"""
authRepository.py
-----------------
Implementación concreta del repositorio de autenticación.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities.Usuario import Usuario
from domain.interfaces.repositories.IAuthRepository import IAuthRepository


class AuthRepository(IAuthRepository):

    def __init__(self, db: AsyncSession):
        self._db = db

    async def obtenerPorEmail(self, email: str) -> Usuario | None:
        resultado = await self._db.execute(
            select(Usuario).where(Usuario.email == email)
        )
        return resultado.scalar_one_or_none()

    async def obtenerPorResetToken(self, token: str) -> Usuario | None:
        resultado = await self._db.execute(
            select(Usuario).where(Usuario.resetToken == token)
        )
        return resultado.scalar_one_or_none()

    async def guardarResetToken(
        self,
        usuarioId: int,
        token: str
    ) -> bool:
        usuario = await self._db.get(Usuario, usuarioId)
        if usuario is None:
            return False

        usuario.resetToken = token
        await self._db.commit()
        return True

    async def invalidarResetToken(self, usuarioId: int) -> bool:
        usuario = await self._db.get(Usuario, usuarioId)
        if usuario is None:
            return False

        usuario.resetToken = None
        await self._db.commit()
        return True

    async def actualizarPassword(
        self,
        usuarioId: int,
        passwordHash: str
    ) -> bool:
        usuario = await self._db.get(Usuario, usuarioId)
        if usuario is None:
            return False

        usuario.passwordHash = passwordHash
        await self._db.commit()
        return True