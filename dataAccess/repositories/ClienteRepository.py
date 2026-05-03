"""
clienteRepository.py
--------------------
Implementación concreta del repositorio de clientes.

El filtro por rol = CLIENTE está encapsulado aquí.
Ningún servicio ni controller escribe ese filtro directamente.
"""

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.Usuario import Usuario
from domain.entities.Rutina import Rutina
from domain.entities.Ejecucion import Ejecucion
from domain.entities.Asistencia import Asistencia
from domain.entities.ClaseGrupal import ClaseGrupal
from domain.entities.Inscripcion import Inscripcion
from domain.enums.RolEnum import RolEnum
from domain.enums.EstadoMembresiaEnum import EstadoMembresiaEnum
from domain.interfaces.repositories.IClienteRepository import IClienteRepository
from dataAccess.repositories.GenericRepository import GenericRepository


class ClienteRepository(GenericRepository[Usuario], IClienteRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db, Usuario)

    async def obtenerTodosLosClientes(self) -> list[Usuario]:
        resultado = await self._db.execute(
            select(Usuario).where(Usuario.rol == RolEnum.CLIENTE)
        )
        return list(resultado.scalars().all())

    async def obtenerRutinaConEjecuciones(self, clienteId: int) -> Rutina | None:
        """
        Carga la rutina activa con sus ejecuciones y ejercicios en una
        sola query usando eager loading (evita el problema N+1).
        """
        resultado = await self._db.execute(
            select(Rutina)
            .where(
                Rutina.clienteID == clienteId,
                Rutina.activa == True
            )
            .options(
                selectinload(Rutina.ejecuciones)
                .selectinload(Ejecucion.ejercicio)
            )
        )
        return resultado.scalar_one_or_none()

    async def registrarAsistencia(self, asistencia: Asistencia) -> Asistencia:
        self._db.add(asistencia)
        await self._db.commit()
        await self._db.refresh(asistencia)
        return asistencia

    async def tieneAsistenciaHoy(self, clienteId: int) -> bool:
        resultado = await self._db.execute(
            select(Asistencia).where(
                Asistencia.usuarioId == clienteId,
                Asistencia.fecha == date.today()
            )
        )
        return resultado.scalar_one_or_none() is not None

    async def obtenerClasesDisponibles(self) -> list[ClaseGrupal]:
        resultado = await self._db.execute(
            select(ClaseGrupal).where(
                ClaseGrupal.inscripcionesAbiertas == True
            )
        )
        return list(resultado.scalars().all())

    async def obtenerInscripcion(
        self, clienteId: int, claseId: int
    ) -> Inscripcion | None:
        resultado = await self._db.execute(
            select(Inscripcion).where(
                Inscripcion.usuarioId == clienteId,
                Inscripcion.claseId == claseId,
                Inscripcion.cancelada == False
            )
        )
        return resultado.scalar_one_or_none()

    async def crearInscripcion(self, inscripcion: Inscripcion) -> Inscripcion:
        self._db.add(inscripcion)
        await self._db.commit()
        await self._db.refresh(inscripcion)
        return inscripcion

    async def cancelarInscripcion(self, inscripcion: Inscripcion) -> Inscripcion:
        inscripcion.cancelada = True
        await self._db.commit()
        await self._db.refresh(inscripcion)
        return inscripcion