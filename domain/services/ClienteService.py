"""
clienteService.py
-----------------
Implementación del servicio de clientes.

Versión refactorizada para usar el patrón Template Method formal.

Comparación antes/después:
    AHORA: el servicio instancia la template correcta y llama a ejecutar().
           La validación común vive en IRegistroTemplate, no aquí.
           El servicio solo orquesta qué template usar en cada caso.

Responsabilidad del servicio:
    - Decidir qué template instanciar según la operación
    - Pasarle los parámetros correctos a ejecutar()
    - Manejar operaciones que no requieren template (verRutina,
      obtenerClases, cancelarInscripcion)
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.Rutina import Rutina
from domain.entities.Ejecucion import Ejecucion
from domain.entities.Asistencia import Asistencia
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.entities.Inscripcion import Inscripcion
from domain.interfaces.services.IClienteService import IClienteService
from domain.patterns.template.RegistroAsistencia import RegistroAsistencia
from domain.patterns.template.RegistroInscripcion import RegistroInscripcion


class ClienteService(IClienteService):
    """
    Servicio de clientes que delega los flujos de registro
    a las implementaciones concretas del patrón Template Method.
    """

    def __init__(self, db: AsyncSession):
        # El servicio recibe la sesión directamente porque las templates
        # también la necesitan. No hay repositorio intermediario aquí
        # dado que las templates acceden a la BD por su cuenta.
        self._db = db

    # ── Ver rutina ────────────────────────────────────────────────────────────

    async def verRutina(self, clienteId: int) -> Rutina:
        """
        Retorna la rutina activa del cliente con sus ejecuciones
        y ejercicios cargados (eager loading para evitar N+1).
        """
        resultado = await self._db.execute(
            select(Rutina)
            .where(
                Rutina.clienteId == clienteId,
                Rutina.activa == True
            )
            .options(
                selectinload(Rutina.ejecuciones)
                .selectinload(Ejecucion.ejercicio)
            )
        )
        rutina = resultado.scalar_one_or_none()

        if rutina is None:
            raise ValueError(
                "No tienes una rutina activa asignada. "
                "Comunícate con tu entrenador."
            )

        return rutina

    # ── Registrar asistencia (Template Method) ────────────────────────────────

    async def registrarAsistencia(
        self,
        clienteId: int,
        observaciones: str | None = None,
    ) -> Asistencia:
        """
        Delega al Template Method RegistroAsistencia.

        El flujo completo vive en IRegistroTemplate.ejecutar():
            1. _validarCliente()    → cliente existe y activo
            2. _validarMembresia()  → membresía ACTIVA
            3. _validarEspecifico() → sin asistencia hoy
            4. _ejecutarAccion()    → persiste Asistencia
        """
        template = RegistroAsistencia(self._db)
        return await template.ejecutar(
            clienteId=clienteId,
            observaciones=observaciones,
        )

    # ── Clases grupales ───────────────────────────────────────────────────────

    async def obtenerClasesDisponibles(self) -> list[ClaseGrupal]:
        resultado = await self._db.execute(
            select(ClaseGrupal).where(
                ClaseGrupal.inscripcionesAbiertas == True
            )
        )
        return list(resultado.scalars().all())

    # ── Inscripción a clase (Template Method) ─────────────────────────────────

    async def inscribirseAClase(
        self,
        clienteId: int,
        claseId: int,
    ) -> Inscripcion:
        """
        Delega al Template Method RegistroInscripcion.

        El flujo completo vive en IRegistroTemplate.ejecutar():
            1. _validarCliente()    → cliente existe y activo
            2. _validarMembresia()  → membresía ACTIVA
            3. _validarEspecifico() → cupo disponible y sin inscripción previa
            4. _ejecutarAccion()    → persiste Inscripcion y actualiza cupo
        """
        template = RegistroInscripcion(self._db)
        return await template.ejecutar(
            clienteId=clienteId,
            claseId=claseId,
        )

    # ── Cancelar inscripción ──────────────────────────────────────────────────

    async def cancelarInscripcion(
        self,
        clienteId: int,
        claseId: int,
    ) -> Inscripcion:
        """
        Cancela la inscripción activa del cliente a una clase.
        No requiere template porque no comparte flujo con otras operaciones.
        """
        resultado = await self._db.execute(
            select(Inscripcion).where(
                Inscripcion.usuarioId == clienteId,
                Inscripcion.claseId == claseId,
                Inscripcion.cancelada == False
            )
        )
        inscripcion = resultado.scalar_one_or_none()

        if inscripcion is None:
            raise ValueError(
                "No se encontró una inscripción activa para esta clase."
            )

        # Devolver el cupo a la clase al cancelar
        clase = await self._db.get(ClaseGrupal, claseId)
        if clase is not None:
            clase.cupoActual = max(0, clase.cupoActual - 1)
            if not clase.inscripcionesAbiertas:
                clase.inscripcionesAbiertas = True

        inscripcion.cancelada = True
        await self._db.commit()
        await self._db.refresh(inscripcion)

        return inscripcion