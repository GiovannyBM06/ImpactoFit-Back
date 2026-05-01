"""
PATRÓN: Factory Method (GoF — Creacional)

Problema que resuelve:
    El MVP requiere crear tres tipos de usuario con inicializaciones distintas:
        - Cliente   → necesita membresía en estado PENDIENTE al crearse
        - Entrenador → no necesita membresía, pero tiene restricciones de rol
        - Admin     → permisos elevados, sin membresía ni rutina

    Sin Factory Method, el servicio tendría un bloque if/elif largo que decide
    cómo construir cada tipo. Eso viola SRP (el servicio haría demasiado)
    y OCP (agregar un nuevo rol requeriría modificar el servicio).

Solución:
    UsuarioFactory define el contrato (método abstracto crear_usuario).
    Cada subclase concreta sabe exactamente cómo construir su tipo de usuario.
    El servicio solo llama a la factory correcta sin conocer los detalles.

Estructura:
    UsuarioFactory          ← clase abstracta (este archivo)
        ├── ClienteFactory  ← crea usuario con rol CLIENTE
        ├── EntrenadorFactory ← crea usuario con rol ENTRENADOR
        └── AdminFactory    ← crea usuario con rol ADMINISTRADOR
"""

from abc import ABC, abstractmethod
from domain.entities.Usuario import Usuario


class UsuarioFactory(ABC):
    """
    Clase abstracta base del patrón Factory Method.

    Define el contrato que todas las fábricas concretas deben cumplir.
    No se puede instanciar directamente.
    """

    @abstractmethod
    def crearUsuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        passwordHash: str,
        telefono: str | None = None,
    ) -> Usuario:
        pass

    @staticmethod
    def obtener_factory(rol: str) -> "UsuarioFactory":
        """
        Método auxiliar: retorna la factory correcta según el rol recibido.

        Uso en el servicio:
            factory = UsuarioFactory.obtener_factory(rol)
            nuevo_usuario = factory.crear_usuario(...)

        Esto evita que el servicio conozca las subclases directamente.
        """
        # Import local para evitar importaciones circulares
        from domain.patterns.factory.ClienteFactory import ClienteFactory
        from domain.patterns.factory.EntrenadorFactory import EntrenadorFactory
        from domain.patterns.factory.AdminFactory import AdminFactory

        factories = dict[str, "UsuarioFactory"]={
            "cliente": ClienteFactory(),
            "entrenador": EntrenadorFactory(),
            "administrador": AdminFactory(),
        }

        factory = factories.get(rol.lower())

        if factory is None:
            rolesValidos =list(factories.keys())
            raise ValueError(
                f"Rol '{rol}' no reconocido. "
                f"Roles válidos: {rolesValidos}"
            )

        return factory