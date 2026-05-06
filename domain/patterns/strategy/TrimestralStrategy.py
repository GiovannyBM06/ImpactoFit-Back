from datetime import date, timedelta
from domain.patterns.strategy.IMembresiaStrategy import IMembresiaStrategy
 
 
class TrimestralStrategy(IMembresiaStrategy):
    """Plan trimestral: 90 días desde la fecha de inicio."""
 
    def calcularFechaVencimiento(self, fechaInicio: date) -> date:
        return fechaInicio + timedelta(days=90)