"""
entrenadorService.py
--------------------
Implementación del servicio de entrenadores.
"""

from domain.entities.Rutina import Rutina
from domain.entities.Ejecucion import Ejecucion
from domain.entities.Usuario import Usuario
from domain.entities.Ejercicio import Ejercicio
from domain.enums.TipoMetricaEnum import TipoMetricaEnum
from domain.interfaces.repositories.IEntrenadorRepository import IEntrenadorRepository
from domain.interfaces.services.IEntrenadorService import IEntrenadorService


class EntrenadorService(IEntrenadorService):

    def __init__(self, repo: IEntrenadorRepository):
        self._repo = repo

    async def verClientesAsignados(self, entrenadorId: int) -> list[Usuario]:
        return await self._repo.obtenerClientesAsignados(entrenadorId)

    async def crearRutina(
        self,
        entrenadorId: int,
        clienteId: int,
        nombre: str,
        descripcion: str | None = None,
    ) -> Rutina:
        # Verificar que el cliente no tenga ya una rutina activa de este entrenador
        rutinaExistente = await self._repo.obtenerRutinaDeCliente(
            clienteId, entrenadorId
        )
        if rutinaExistente is not None:
            raise ValueError(
                f"El cliente ya tiene una rutina activa asignada por ti. "
                f"Modifica la existente o desactívala primero."
            )

        rutina = Rutina(
            clienteId=clienteId,
            entrenadorId=entrenadorId,
            nombre=nombre,
            descripcion=descripcion,
            activa=True,
        )

        return await self._repo.crearRutina(rutina)

    async def asignarEjercicio(
        self,
        entrenadorId: int,
        rutinaId: int,
        ejercicioId: int,
        series: int,
        tipoMetrica: str,
        orden: int,
        repeticiones: int | None = None,
        duracionSeg: int | None = None,
        pesoKg: int | None = None,
        descansoSeg: int | None = None,
    ) -> Ejecucion:

        # Validar combinación tipoMetrica / repeticiones / duracionSeg
        tipo = TipoMetricaEnum(tipoMetrica.lower())

        if tipo == TipoMetricaEnum.REPETICIONES:
            if repeticiones is None:
                raise ValueError(
                    "Debe especificar repeticiones para el tipo REPETICIONES"
                )
            duracionSeg = None  # ignorar si viene por error

        elif tipo == TipoMetricaEnum.TIEMPO:
            if duracionSeg is None:
                raise ValueError(
                    "Debe especificar duracionSeg para el tipo TIEMPO"
                )
            repeticiones = None  # ignorar si viene por error

        ejecucion = Ejecucion(
            rutinaId=rutinaId,
            ejercicioId=ejercicioId,
            orden=orden,
            series=series,
            tipoMetrica=tipo,
            repeticiones=repeticiones,
            duracionSeg=duracionSeg,
            pesoKg=pesoKg,
            descansoSeg=descansoSeg,
        )

        return await self._repo.agregarEjecucion(ejecucion)

    async def modificarEjercicio(
        self,
        entrenadorId: int,
        ejecucionId: int,
        series: int | None = None,
        repeticiones: int | None = None,
        duracionSeg: int | None = None,
        pesoKg: int | None = None,
        descansoSeg: int | None = None,
        orden: int | None = None,
    ) -> Ejecucion:

        ejecucion = await self._repo.obtenerEjecucion(ejecucionId)
        if ejecucion is None:
            raise ValueError(f"No se encontró el ejercicio con id {ejecucionId}")

        # Actualizar solo los campos que vienen con valor
        if series is not None:
            ejecucion.series = series
        if repeticiones is not None:
            ejecucion.repeticiones = repeticiones
        if duracionSeg is not None:
            ejecucion.duracionSeg = duracionSeg
        if pesoKg is not None:
            ejecucion.pesoKg = pesoKg
        if descansoSeg is not None:
            ejecucion.descansoSeg = descansoSeg
        if orden is not None:
            ejecucion.orden = orden

        return await self._repo.actualizarEjecucion(ejecucion)

    async def eliminarEjercicio(
        self,
        entrenadorId: int,
        ejecucionId: int,
    ) -> bool:
        ejecucion = await self._repo.obtenerEjecucion(ejecucionId)
        if ejecucion is None:
            raise ValueError(f"No se encontró el ejercicio con id {ejecucionId}")

        return await self._repo.eliminarEjecucion(ejecucionId)