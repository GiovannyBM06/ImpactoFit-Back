"""
ejercicioService.py
-------------------
Implementación del servicio del catálogo de ejercicios.
"""

from domain.entities.Ejercicio import Ejercicio
from domain.interfaces.repositories.IEjercicioRepository import IEjercicioRepository
from domain.interfaces.services.IEjercicioService import IEjercicioService


class EjercicioService(IEjercicioService):

    def __init__(self, repo: IEjercicioRepository):
        self._repo = repo

    async def crearEjercicio(
        self,
        nombre: str,
        descripcion: str | None = None,
    ) -> Ejercicio:

        if await self._repo.existeNombre(nombre):
            raise ValueError(
                f"Ya existe un ejercicio con el nombre '{nombre}'"
            )

        ejercicio = Ejercicio(
            nombre=nombre,
            descripcion=descripcion,
        )

        return await self._repo.crear(ejercicio)

    async def obtenerTodos(self) -> list[Ejercicio]:
        return await self._repo.obtenerTodos()

    async def obtenerPorId(self, ejercicioId: int) -> Ejercicio:
        ejercicio = await self._repo.obtenerPorId(ejercicioId)
        if ejercicio is None:
            raise ValueError(f"No se encontró un ejercicio con id {ejercicioId}")
        return ejercicio

    async def actualizarEjercicio(
        self,
        ejercicioId: int,
        nombre: str | None = None,
        descripcion: str | None = None,
    ) -> Ejercicio:

        ejercicio = await self._repo.obtenerPorId(ejercicioId)
        if ejercicio is None:
            raise ValueError(f"No se encontró un ejercicio con id {ejercicioId}")

        if nombre is not None:
            if await self._repo.existeNombre(nombre) and nombre != ejercicio.nombre:
                raise ValueError(f"Ya existe un ejercicio con el nombre '{nombre}'")
            ejercicio.nombre = nombre

        if descripcion is not None:
            ejercicio.descripcion = descripcion

        return await self._repo.actualizar(ejercicio)

    async def eliminarEjercicio(self, ejercicioId: int) -> bool:
        ejercicio = await self._repo.obtenerPorId(ejercicioId)
        if ejercicio is None:
            raise ValueError(f"No se encontró un ejercicio con id {ejercicioId}")
        return await self._repo.eliminar(ejercicioId)

    async def buscarPorNombre(self, nombre: str) -> Ejercicio | None:
        return await self._repo.obtenerPorNombre(nombre)