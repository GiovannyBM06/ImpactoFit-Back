"""
entrenadorRepository.py
-----------------------
Implementación concreta del repositorio de entrenadores.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.Usuario import Usuario
from domain.entities.Rutina import Rutina
from domain.entities.Ejecucion import Ejecucion
from domain.enums.RolEnum import RolEnum
from domain.interfaces.repositories.IEntrenadorRepository import IEntrenadorRepository
from dataAccess.repositories.GenericRepository import GenericRepository


class EntrenadorRepository(GenericRepository[Usuario], IEntrenadorRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Usuario)

    async def obtenerClientesAsignados(self, entrenadorId: int) -> list[Usuario]:
        """
        Clientes que tienen una rutina activa asignada por este entrenador.
        Se obtienen a través de las rutinas, no del campo rol directamente.
        """
        resultado = await self._db.execute(
            select(Usuario)
            .join(Rutina, Rutina.clienteId == Usuario.id)
            .where(
                Rutina.entrenadorId == entrenadorId,
                Rutina.activa == True
            )
        )
        return list(resultado.scalars().unique().all())

    async def obtenerRutinaDeCliente(
        self, clienteId: int, entrenadorId: int
    ) -> Rutina | None:
        resultado = await self._db.execute(
            select(Rutina)
            .where(
                Rutina.clienteId == clienteId,
                Rutina.entrenadorId == entrenadorId,
                Rutina.activa == True
            )
            .options(
                selectinload(Rutina.ejecuciones)
                .selectinload(Ejecucion.ejercicio)
            )
        )
        return resultado.scalar_one_or_none()

    async def crearRutina(self, rutina: Rutina) -> Rutina:
        self._db.add(rutina)
        await self._db.commit()
        await self._db.refresh(rutina)
        return rutina

    async def agregarEjecucion(self, ejecucion: Ejecucion) -> Ejecucion:
        self._db.add(ejecucion)
        await self._db.commit()
        await self._db.refresh(ejecucion)
        return ejecucion

    async def obtenerEjecucion(self, ejecucionId: int) -> Ejecucion | None:
        return await self._db.get(Ejecucion, ejecucionId)

    async def actualizarEjecucion(self, ejecucion: Ejecucion) -> Ejecucion:
        await self._db.commit()
        await self._db.refresh(ejecucion)
        return ejecucion

    async def eliminarEjecucion(self, ejecucionId: int) -> bool:
        ejecucion = await self.obtenerEjecucion(ejecucionId)
        if ejecucion is None:
            return False
        await self._db.delete(ejecucion)
        await self._db.commit()
        return True