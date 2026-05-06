"""
ejercicioRepository.py
----------------------
Implementación del repositorio del catálogo de ejercicios.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from domain.entities.Ejercicio import Ejercicio
from domain.interfaces.repositories.IEjercicioRepository import IEjercicioRepository
from dataAccess.repositories.GenericRepository import GenericRepository


class EjercicioRepository(GenericRepository[Ejercicio], IEjercicioRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Ejercicio)

    async def obtenerPorNombre(self, nombre: str) -> Ejercicio | None:
        resultado = await self._db.execute(
            select(Ejercicio).where(Ejercicio.nombre == nombre)
        )
        return resultado.scalar_one_or_none()

    async def existeNombre(self, nombre: str) -> bool:
        resultado = await self._db.execute(
            select(func.count()).where(Ejercicio.nombre == nombre)
        )
        return resultado.scalar_one() > 0