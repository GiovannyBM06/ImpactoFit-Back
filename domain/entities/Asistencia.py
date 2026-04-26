"""
asistencia.py
-------------
Entidad Asistencia. Registra cada ingreso de un cliente al gimnasio.

El cliente llena un formulario desde la app móvil para registrar su asistencia.
Regla de negocio (RN02): si la membresía está vencida, no se registra asistencia.
Esta validación se aplica en el Template Method del servicio.
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, String, Text
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase


class Asistencia(AuditBase):
    """
    Tabla: asistencias

    Cada fila representa un ingreso al gimnasio.
    Un usuario puede tener múltiples registros, uno por día de visita.
    """

    __tablename__ = "asistencias"

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Fecha de la visita (solo fecha, sin hora)
    fecha = Column(Date, nullable=False, default=date.today)

    # Hora exacta de registro (timestamp completo)
    hora_registro = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Campos del formulario que llena el cliente desde la app
    # (se pueden extender según necesidades del gimnasio)
    observaciones = Column(Text, nullable=True)

    # ── Relaciones ──────────────────────────────────────────────────────────

    usuario = relationship("Usuario", back_populates="asistencias")

    def __repr__(self):
        return (
            f"<Asistencia id={self.id} "
            f"usuario_id={self.usuario_id} "
            f"fecha={self.fecha}>"
        )