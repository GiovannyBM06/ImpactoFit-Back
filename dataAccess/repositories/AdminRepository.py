"""
adminRepository.py
------------------
Implementación concreta del repositorio de administradores.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.entities.Usuario import Usuario
from domain.entities.Membresia import Membresia
from domain.entities.Pago import Pago
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.enums.RolEnum import RolEnum
from domain.interfaces.repositories.IAdminRepository import IAdminRepository
from dataAccess.repositories.GenericRepository import GenericRepository


class AdminRepository(GenericRepository[Usuario], IAdminRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Usuario)

    async def obtenerTodosLosClientes(self) -> list[Usuario]:
        resultado = await self._db.execute(
            select(Usuario).where(Usuario.rol == RolEnum.CLIENTE)
        )
        return list(resultado.scalars().all())

    async def obtenerTodasLasMembresias(self) -> list[Membresia]:
        resultado = await self._db.execute(select(Membresia))
        return list(resultado.scalars().all())

    async def obtenerMembresiaPorId(self, membresiaId: int) -> Membresia | None:
        return await self._db.get(Membresia, membresiaId)

    async def crearMembresia(self, membresia: Membresia) -> Membresia:
        self._db.add(membresia)
        await self._db.commit()
        await self._db.refresh(membresia)
        return membresia

    async def actualizarMembresia(self, membresia: Membresia) -> Membresia:
        await self._db.commit()
        await self._db.refresh(membresia)
        return membresia

    async def crearPago(self, pago: Pago) -> Pago:
        self._db.add(pago)
        await self._db.commit()
        await self._db.refresh(pago)
        return pago

    async def crearClaseGrupal(self, clase: ClaseGrupal) -> ClaseGrupal:
        self._db.add(clase)
        await self._db.commit()
        await self._db.refresh(clase)
        return clase

    async def obtenerClasePorId(self, claseId: int) -> ClaseGrupal | None:
        return await self._db.get(ClaseGrupal, claseId)
    
    async def obtenerTodasLasClases(self) -> list[ClaseGrupal]:
        resultado = await self._db.execute(select(ClaseGrupal))
        return list(resultado.scalars().all())

    async def obtenerEntrenadores(self) -> list[Usuario]:
        resultado = await self._db.execute(
            select(Usuario).where(Usuario.rol == RolEnum.ENTRENADOR)
        )
        return list(resultado.scalars().all())