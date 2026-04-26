"""
entrenador_factory.py
---------------------
PATRÓN: Factory Method — Implementación concreta para rol ENTRENADOR

Responsabilidad:
    Construir un Usuario con rol ENTRENADOR correctamente inicializado.

    Un entrenador al momento de su creación:
        - Recibe rol = ENTRENADOR
        - Queda activo (is_active = True)
        - NO tiene membresía (los entrenadores no son clientes del gimnasio)
        - NO tiene rutina asignada (ellos crean rutinas, no las reciben)
        - Sus clientes se asignan posteriormente por el administrador

    Si en una fase posterior el entrenador necesita atributos adicionales
    (certificaciones, especialidades, tarifa), solo se modifica esta factory
    sin tocar el servicio ni las otras factories.
"""

from domain.entities.Usuario import Usuario
from domain.enums.rolEnum import RolEnum
from domain.patterns.factory.UsuarioFactory import UsuarioFactory


class EntrenadorFactory(UsuarioFactory):
    """Factory concreta para crear usuarios con rol ENTRENADOR."""

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        password_hash: str,
        telefono: str | None = None,
    ) -> Usuario:
        """
        Crea un Usuario con rol ENTRENADOR.

        Los entrenadores pueden modificar rutinas y ver la lista de sus
        clientes asignados. No tienen acceso a funciones administrativas
        ni al módulo de pagos.
        """

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password_hash=password_hash,
            telefono=telefono,
            rol=RolEnum.ENTRENADOR,
            is_active=True,
        )

        return usuario