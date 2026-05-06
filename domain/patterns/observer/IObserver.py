"""
IObserver.py
------------
PATRÓN: Observer (GoF — Comportamental)

Interfaces base del patrón Observer.

Problema que resuelve:
    Al confirmar un pago y activar una membresía, múltiples
    subsistemas deben reaccionar:
        1. Generar el código de comprobante en el Pago
        2. Activar el estado del Usuario (isActive)

    Sin Observer, AdminService haría todo eso en secuencia dentro
    del mismo método, acoplando responsabilidades que deberían
    ser independientes. Agregar una nueva reacción (ej: enviar email)
    requeriría modificar el servicio, violando OCP.

Solución:
    MembresiaActivadaEvent actúa como Observable.
    Cada subsistema que debe reaccionar implementa IObserver
    y se suscribe al evento. El servicio solo dispara el evento;
    no sabe cuántos ni cuáles observadores reaccionarán.

Estructura:
    IObserver                           ← contrato de suscriptores
    IObservable                         ← contrato del emisor
    MembresiaActivadaEvent              ← evento concreto (Observable)
        ├── ComprobanteObserver         ← genera código de comprobante
        └── EstadoUsuarioObserver       ← activa el usuario
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date

@dataclass
class MembresiaActivadaData:
    """
    Datos que se pasan a los observadores cuando se activa una membresía.
    Contiene todo lo que los observadores podrían necesitar.
    """
    membresiaId:  int
    usuarioId:    int
    pagoId:       int
    tipo:         str
    fechaInicio:  date
    fechaVencimiento: date

class IObserver(ABC):
    """
    Contrato para todos los suscriptores del sistema.
    Cualquier clase que quiera reaccionar a un evento debe implementar esta interfaz.
    """

    @abstractmethod
    async def actualizar(self, data: MembresiaActivadaData) -> None:
        pass


class IObservable(ABC):
    """
    Contrato para los emisores de eventos.
    Gestiona la lista de suscriptores y notifica cuando ocurre el evento.
    """

    def __init__(self):
        self._observadores: list[IObserver] = []

    def suscribir(self, observador: IObserver) -> None:
        """Agrega un observador a la lista de suscriptores."""
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador: IObserver) -> None:
        """Elimina un observador de la lista de suscriptores."""
        self._observadores.remove(observador)

    async def notificar(self, data: MembresiaActivadaData) -> None:
        """Notifica a todos los suscriptores con los datos del evento."""
        for observador in self._observadores:
            await observador.actualizar(data)