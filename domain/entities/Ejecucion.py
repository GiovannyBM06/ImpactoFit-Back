"""
Tabla intermedia para la relacion N:M entrer las entidades Rutina y Ejercicio
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from domain.entities.AuditBase import AuditBase
from domain.enums.TipoMetricaEnum import TipoMetricaEnum

class Ejecicion(AuditBase):

    __tablename__ = "ejecuciones"

    rutinaId = Column(Integer, ForeignKey("rutinas.id"), nullable= False)
    EjercicioId = Column(Integer, ForeignKey("ejercicios.id"), nullable=False)
    orden = Column(Integer, nullable=False, default=1)
    tipoMetrica = Column(Enum(TipoMetricaEnum), nullable=False, default=TipoMetricaEnum.REPETICIONES)
    series = Column(Integer, nullable=False, default=3)
    repeticiones = Column(Integer, nullable=True)
    duracionSeg =Column(Integer, nullable=True)
    pesoKg = Column(Integer, nullable=True)
    descansoSeg = Column(Integer, nullable=True, default=60)

    #Relaciones
    rutina    = relationship("Rutina",    back_populates="ejecuciones")
    ejercicio = relationship("Ejercicio", back_populates="ejecuciones")
 
    def __repr__(self):
        metrica = (
            f"{self.repeticiones} reps"
            if self.tipoMetrica == TipoMetricaEnum.REPETICIONES
            else f"{self.duracionSeg}s"
        )
        return (
            f"<Ejecucion rutinaId={self.rutinaId} "
            f"ejercicioId={self.EjercicioId} "
            f"{self.series}x{metrica}>"
        )