"""
membresiaActivadaEvent.py
-------------------------
PATRÓN: Observer — Evento concreto (Observable)

Representa el evento "una membresía fue activada".
AdminService instancia este evento, suscribe los observadores
y lo dispara. El servicio no sabe qué harán los observadores,
solo que algo ocurrió.
"""

from domain.patterns.observer.IObserver import IObservable, MembresiaActivadaData


class MembresiaActivadaEvent(IObservable):
    """
    Evento concreto que se dispara cuando el admin activa una membresía.

    Uso en AdminService:
        evento = MembresiaActivadaEvent()
        evento.suscribir(ComprobanteObserver(db))
        evento.suscribir(EstadoUsuarioObserver(db))
        await evento.notificar(data)
    """
    pass