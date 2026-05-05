"""
IEntrenadorService.py
---------------------
Interfaz del servicio de entrenadores.

Casos de uso del MVP para el rol ENTRENADOR:
    - Ver sus clientes asignados
    - Crear rutina para un cliente
    - Asignar ejercicio a una rutina (con parámetros de ejecución)
    - Modificar parámetros de un ejercicio en una rutina
    - Eliminar un ejercicio de una rutina
"""

from abc import ABC, abstractmethod
from domain.entities.Rutina import Rutina
from domain.entities.Ejecucion import  Ejecucion
from domain.entities.Usuario import Usuario


class IEntrenadorService(ABC):

    @abstractmethod
    async def verClientesAsignados(self, entrenadorId: int) -> list[Usuario]:
        """Retorna los clientes que tienen rutina asignada por este entrenador."""
        pass

    @abstractmethod
    async def verRutinaDeCliente(
        self,
        entrenadorId: int,
        clienteId: int,
    ) -> Rutina | None:
        """
        Retorna la rutina activa de un cliente verificando que
        pertenezca a este entrenador. Retorna None si no existe.
        """
        pass
    
    @abstractmethod
    async def crearRutina(
        self,
        entrenadorId: int,
        clienteId: int,
        nombre: str,
        descripcion: str | None = None,
    ) -> Rutina:
        """
        Crea una rutina para un cliente.

        Raises:
            ValueError: si el cliente no existe o ya tiene una rutina activa.
        """
        pass

    @abstractmethod
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
        """
        Agrega un ejercicio del catálogo a una rutina con sus parámetros.

        Raises:
            ValueError: si la rutina no pertenece al entrenador,
                        el ejercicio no existe, o la combinación
                        tipoMetrica/repeticiones/duracionSeg es inválida.
        """
        pass

    @abstractmethod
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
        """
        Modifica los parámetros de un ejercicio dentro de una rutina.

        Raises:
            ValueError: si la ejecución no existe o no pertenece
                        a una rutina de este entrenador.
        """
        pass

    @abstractmethod
    async def eliminarEjercicio(
        self,
        entrenadorId: int,
        ejecucionId: int,
    ) -> bool:
        """
        Elimina un ejercicio de una rutina.

        Raises:
            ValueError: si la ejecución no existe o no pertenece
                        a una rutina de este entrenador.
        """
        pass