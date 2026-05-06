"""
registroInscripcion.py
----------------------
PATRÓN: Template Method — Implementación concreta para inscripción a clase grupal.

Implementa los pasos abstractos de IRegistroTemplate:
    _validarEspecifico() → verifica que la clase tenga inscripciones abiertas
                           y que el cliente no esté ya inscrito
    _ejecutarAccion()    → crea la inscripción y actualiza el cupo de la clase.
                           Si el cupo se agota, cierra las inscripciones.

El flujo completo al llamar ejecutar():
    1. _validarCliente()      [IRegistroTemplate] → cliente existe y activo
    2. _validarMembresia()    [IRegistroTemplate] → membresía ACTIVA
    3. _validarEspecifico()   [este archivo]      → cupo disponible y sin inscripción previa
    4. _ejecutarAccion()      [este archivo]      → persiste Inscripcion y actualiza cupo
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities.ClaseGrupal import ClaseGrupal
from domain.entities.Inscripcion import Inscripcion
from domain.patterns.template.IRegistroTemplate import IRegistroTemplate


class RegistroInscripcion(IRegistroTemplate):
    """
    Subclase concreta para la inscripción a una clase grupal.

    Uso desde ClienteService:
        registro = RegistroInscripcion(db)
        inscripcion = await registro.ejecutar(
            clienteId=clienteId,
            claseId=claseId
        )
    """

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self._clase: ClaseGrupal | None = None  # se carga en _validarEspecifico()

    # ── Pasos abstractos implementados ───────────────────────────────────────

    async def _validarEspecifico(
        self,
        clienteId: int,
        claseId: int,
        **kwargs
    ) -> None:
        """
        Verifica:
            1. Que la clase existe y tiene inscripciones abiertas (RN05)
            2. Que el cliente no esté ya inscrito en esta clase

        Raises:
            ValueError: si la clase no existe, está llena,
                        o el cliente ya está inscrito.
        """

        # Verificar que la clase existe y tiene cupo
        clase = await self._db.get(ClaseGrupal, claseId)

        if clase is None:
            raise ValueError(
                f"No se encontró una clase con id {claseId}"
            )

        if not clase.inscripcionesAbiertas:
            raise ValueError(
                f"La clase '{clase.nombre}' no tiene inscripciones abiertas. "
                f"El cupo está lleno ({clase.cupoActual}/{clase.cupoMaximo})."
            )

        # Guardar la clase para no volver a consultarla en _ejecutarAccion()
        self._clase = clase

        # Verificar que el cliente no esté ya inscrito
        resultado = await self._db.execute(
            select(Inscripcion).where(
                Inscripcion.usuarioId == clienteId,
                Inscripcion.claseId == claseId,
                Inscripcion.cancelada == False
            )
        )
        inscripcionExistente = resultado.scalar_one_or_none()

        if inscripcionExistente is not None:
            raise ValueError(
                f"Ya estás inscrito en la clase '{clase.nombre}'."
            )

    async def _ejecutarAccion(
        self,
        clienteId: int,
        claseId: int,
        **kwargs
    ) -> Inscripcion:
        """
        Crea la inscripción y actualiza el cupo de la clase.
        Si el cupo se agota, cierra automáticamente las inscripciones.

        Args:
            clienteId : id del cliente
            claseId   : id de la clase grupal

        Returns:
            Inscripcion: la inscripción persistida con id asignado.
        """

        # Crear la inscripción
        inscripcion = Inscripcion(
            usuarioId=clienteId,
            claseId=claseId,
        )
        self._db.add(inscripcion)

        # Actualizar cupo de la clase
        self._clase.cupoActual += 1

        # Si el cupo se agotó, cerrar inscripciones (RN05)
        # Nota: esta es la lógica que en el Observer futuro
        # se delegaría a CupoAgotadoObserver
        if self._clase.cupoActual >= self._clase.cupoMaximo:
            self._clase.inscripcionesAbiertas = False

        await self._db.commit()
        await self._db.refresh(inscripcion)

        return inscripcion