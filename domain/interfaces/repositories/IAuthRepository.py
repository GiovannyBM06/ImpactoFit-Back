"""
Interfaz del repositorio de autenticación.

    Gestiona las operaciones de BD relacionadas
    directamente con el flujo de autenticación:
    buscar usuario para login, gestionar el reset token.
"""

from abc import ABC, abstractmethod
from domain.entities.Usuario import Usuario


class IAuthRepository(ABC):

    @abstractmethod
    async def obtenerPorEmail(self, email: str) -> Usuario | None:
        """
        Busca un usuario por email para el flujo de login.
        Retorna None si no existe.
        """
        pass

    @abstractmethod
    async def obtenerPorResetToken(self, token: str) -> Usuario | None:
        """
        Busca un usuario por su token de recuperación de contraseña.
        Retorna None si el token no existe o ya fue usado.
        """
        pass

    @abstractmethod
    async def guardarResetToken(
        self,
        usuarioId: int,
        token: str
    ) -> bool:
        """
        Guarda el token de recuperación en el usuario.
        Retorna True si se guardó correctamente.
        """
        pass

    @abstractmethod
    async def invalidarResetToken(self, usuarioId: int) -> bool:
        """
        Invalida el token de recuperación poniéndolo en None.
        Se llama después de que el usuario resetea su contraseña.
        Retorna True si se invalidó correctamente.
        """
        pass

    @abstractmethod
    async def actualizarPassword(
        self,
        usuarioId: int,
        passwordHash: str
    ) -> bool:
        """
        Actualiza el hash de contraseña de un usuario.
        Retorna True si se actualizó correctamente.
        """
        pass