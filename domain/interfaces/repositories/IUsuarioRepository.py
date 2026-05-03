"""
IUsuarioRepository.py
---------------------
Interfaz específica del repositorio de usuarios.

Extiende IGenericRepository con los métodos de consulta propios
del dominio de usuarios que van más allá del CRUD básico.

Por qué extender y no solo usar IGenericRepository:
    Operaciones como buscar por email (necesaria para el login)
    o verificar si un email ya está registrado son específicas
    del contexto de Usuario y no aplican a otras entidades.
    ISP → los servicios que solo necesitan CRUD básico dependen
    de IGenericRepository; los que necesitan lógica de usuario
    dependen de esta interfaz más específica.
"""

from abc import abstractmethod
from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.repositories.IGenericRepository import IGenericRepository


class IUsuarioRepository(IGenericRepository[Usuario]):
    """
    Contrato del repositorio de usuarios.

    Agrega métodos específicos del dominio de usuarios
    sobre el CRUD base heredado de IGenericRepository.
    """

    @abstractmethod
    async def obtenerPorEmail(self, email: str) -> Usuario | None:
        """
        Busca un usuario por su email.
        Usado principalmente en el flujo de autenticación (login).

        Returns:
            El usuario si existe, None si no se encuentra.
        """
        pass

    @abstractmethod
    async def existeEmail(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado en el sistema.
        Usado en la creación de usuarios para garantizar unicidad.

        Returns:
            True si el email ya existe, False si está disponible.
        """
        pass

    @abstractmethod
    async def obtenerPorRol(self, rol: RolEnum) -> list[Usuario]:
        """
        Lista todos los usuarios que tienen un rol específico.
        Usado por los repositorios especializados (Cliente, Entrenador, Admin)
        que encapsulan internamente el filtro por rol.

        Returns:
            Lista de usuarios con el rol indicado (puede estar vacía).
        """
        pass

    @abstractmethod
    async def actualizarResetToken(self, usuarioId: int, token: str | None) -> bool:
        """
        Actualiza el token de recuperación de contraseña de un usuario.
        Recibe None para invalidar el token después de usarlo.

        Returns:
            True si se actualizó correctamente, False si el usuario no existe.
        """
        pass