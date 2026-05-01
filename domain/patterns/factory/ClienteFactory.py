"""
cliente_factory.py
------------------
PATRÓN: Factory Method — Implementación concreta para rol CLIENTE

Responsabilidad:
    Construir un Usuario con rol CLIENTE correctamente inicializado.

    Un cliente al momento de su creación:
        - Recibe rol = CLIENTE
        - Queda activo (is_active = True)
        - NO tiene membresía aún (se crea por separado cuando el admin
          registra el pago — RN04)
        - NO tiene rutina aún (se asigna cuando el entrenador la crea)

    Esta inicialización mínima respeta el flujo real del gimnasio:
    primero se registra el cliente, luego el admin gestiona el pago
    y activa la membresía, y finalmente el entrenador asigna la rutina.
"""

from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.patterns.factory.UsuarioFactory import UsuarioFactory


class ClienteFactory(UsuarioFactory):
    """Factory concreta para crear usuarios con rol CLIENTE."""

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        passworHash: str,
        telefono: str | None = None,
    ) -> Usuario:
        """
        Crea un Usuario con rol CLIENTE.

        El usuario queda activo desde el inicio para que pueda
        hacer login, pero sin membresía activa (RN02 se aplica
        en el registro de asistencia, no en el login).
        """

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            passworHash=passworHash,
            telefono=telefono,
            rol=RolEnum.CLIENTE,
            is_active=True,
        )

        return usuario

         