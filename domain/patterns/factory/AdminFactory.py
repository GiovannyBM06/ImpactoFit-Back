"""
admin_factory.py
----------------
PATRÓN: Factory Method — Implementación concreta para rol ADMINISTRADOR

Responsabilidad:
    Construir un Usuario con rol ADMINISTRADOR correctamente inicializado.

    Un administrador al momento de su creación:
        - Recibe rol = ADMINISTRADOR
        - Queda activo (is_active = True)
        - NO tiene membresía (no es un cliente)
        - NO tiene rutina
        - Tiene acceso completo al sistema: gestión de usuarios,
          confirmación de pagos, creación de clases y asignación
          de entrenadores a clientes

    Nota de seguridad: la creación de administradores debería estar
    restringida a otro administrador existente. Esta validación
    se aplica en el controller mediante el middleware de autenticación,
    no en la factory.
"""

from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.patterns.factory.UsuarioFactory import UsuarioFactory


class AdminFactory(UsuarioFactory):
    """Factory concreta para crear usuarios con rol ADMINISTRADOR."""

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        passwordHash: str,
        telefono: str | None = None,
    ) -> Usuario:
        """
        Crea un Usuario con rol ADMINISTRADOR.

        Los administradores tienen acceso a todos los módulos:
        usuarios, membresías, pagos, clases y reportes.
        """

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            passwordHash=passwordHash,
            telefono=telefono,
            rol=RolEnum.ADMINISTRADOR,
            isActive=True,
        )

        return usuario