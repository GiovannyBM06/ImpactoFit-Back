"""
usuarioService.py
-----------------
Implementación del servicio de usuarios.

Implementa IUsuarioService e internamente usa:
    - IUsuarioRepository (inyectado, no instanciado directamente)
    - UsuarioFactory (patrón Factory Method) para construir usuarios

El servicio no instancia UsuarioRepository directamente.
Recibe la interfaz IUsuarioRepository por el constructor,
manteniendo DIP: depende de abstracciones, no de implementaciones.

Esto permite en el futuro inyectar un repositorio mock en tests
sin modificar el servicio.
"""

from passlib.context import CryptContext

from domain.entities.Usuario import Usuario
from domain.enums.RolEnum import RolEnum
from domain.interfaces.repositories.IUsuarioRepository import IUsuarioRepository
from domain.interfaces.services.IUsuarioService import IUsuarioService
from domain.patterns.factory.UsuarioFactory import UsuarioFactory

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsuarioService(IUsuarioService):
    """
    Lógica de negocio para creación y gestión general de usuarios.

    Recibe el repositorio por constructor (inyección de dependencias).
    No importa qué implementación concreta recibe, solo le importa
    que cumpla el contrato IUsuarioRepository.
    """

    def __init__(self, repo: IUsuarioRepository):
        self._repo = repo

    # ── IUsuarioService implementation ───────────────────────────────────────

    async def crearUsuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        password: str,
        rol: str,
        telefono: str | None = None,
    ) -> Usuario:
    
        # 1. Unicidad de email (delegado al repositorio)
        if await self._repo.existeEmail(email):
            raise ValueError(
                f"Ya existe un usuario registrado con el email '{email}'"
            )

        # 2. Hash de contraseña (nunca se almacena texto plano)
        passwordHash = pwdContext.hash(password)

        # 3 y 4. Factory Method: el servicio no conoce las subclases concretas
        factory = UsuarioFactory.obtenerFactory(rol)
        nuevoUsuario = factory.crearUsuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            passwordHash=passwordHash,
            telefono=telefono,
        )

        # 5. Persistir (delegado al repositorio)
        return await self._repo.crear(nuevoUsuario)

    async def asignarEntrenador(
        self,
        clienteId: int,
        entrenadorId: int,
    ) -> dict:
        """
        Valida que ambos usuarios existan y tengan el rol correcto.
        La asignación se materializa cuando el entrenador crea
        una Rutina con ambos ids (en EntrenadorService).
        """

        cliente = await self._repo.obtenerPorId(clienteId)
        if cliente is None:
            raise ValueError(f"No se encontró un usuario con id {clienteId}")

        entrenador = await self._repo.obtenerPorId(entrenadorId)
        if entrenador is None:
            raise ValueError(f"No se encontró un usuario con id {entrenadorId}")

        if cliente.rol != RolEnum.CLIENTE:
            raise ValueError(
                f"El usuario {clienteId} tiene rol '{cliente.rol}', se esperaba CLIENTE"
            )

        if entrenador.rol != RolEnum.ENTRENADOR:
            raise ValueError(
                f"El usuario {entrenadorId} tiene rol '{entrenador.rol}', se esperaba ENTRENADOR"
            )

        return {
            "mensaje": (
                f"Entrenador {entrenador.nombre} {entrenador.apellido} "
                f"asignado a {cliente.nombre} {cliente.apellido}. "
                f"Proceda a crear la rutina desde el módulo de entrenamiento."
            ),
            "clienteId":    clienteId,
            "entrenadorId": entrenadorId,
        }

    async def obtenerPorId(self, usuarioId: int) -> Usuario:
        usuario = await self._repo.obtenerPorId(usuarioId)
        if usuario is None:
            raise ValueError(f"No se encontró un usuario con id {usuarioId}")
        return usuario