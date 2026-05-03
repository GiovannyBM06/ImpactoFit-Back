"""
IUsuarioService.py
------------------
Interfaz del servicio de usuarios.

Define el contrato que la capa de presentación (controllers/routers)
usa para comunicarse con la lógica de negocio de usuarios.

Por qué definir esta interfaz:
    DIP → el controller depende de esta abstracción, no de la
          implementación concreta UsuarioService. Esto permite
          reemplazar o mockear el servicio en pruebas sin tocar
          el controller.

    ISP → esta interfaz expone solo lo que el controller necesita.
          La lógica interna (hashing, factories, repositorios)
          es un detalle de implementación invisible para el caller.

Contexto:
    Este servicio gestiona la creación de cualquier tipo de usuario
    y la asignación de entrenadores a clientes (funciones del admin).
    Las operaciones específicas por rol viven en sus propios servicios:
        - IClienteService
        - IEntrenadorService
        - IAdminService
"""

from abc import ABC, abstractmethod
from domain.entities.Usuario import Usuario


class IUsuarioService(ABC):
    """
    Contrato del servicio de usuarios.
    """

    @abstractmethod
    async def crearUsuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        password: str,
        rol: str,
        telefono: str | None = None,
    ) -> Usuario:
        """
        Crea un nuevo usuario del tipo indicado.

        Internamente usa el patrón Factory Method para construir
        el objeto según el rol, y hashea la contraseña antes de persistir.

        Args:
            nombre    : Nombre del usuario
            apellido  : Apellido del usuario
            email     : Email único (se usa para el login)
            password  : Contraseña en texto plano (se hashea internamente)
            rol       : "cliente", "entrenador" o "administrador"
            telefono  : Teléfono de contacto (opcional)

        Returns:
            Usuario creado con id asignado por la BD.

        Raises:
            ValueError: si el email ya está registrado o el rol no existe.
        """
        pass

    @abstractmethod
    async def asignarEntrenador(
        self,
        clienteId: int,
        entrenadorId: int,
    ) -> dict:
        """
        Valida y registra la asignación de un entrenador a un cliente.

        Args:
            clienteId    : Id del usuario con rol CLIENTE
            entrenadorId : Id del usuario con rol ENTRENADOR

        Returns:
            Diccionario con mensaje de confirmación y los ids.

        Raises:
            ValueError: si alguno de los usuarios no existe o
                        no tiene el rol esperado.
        """
        pass

    @abstractmethod
    async def obtenerPorId(self, usuarioId: int) -> Usuario:
        """
        Retorna un usuario por su id.

        Raises:
            ValueError: si el usuario no existe.
        """
        pass