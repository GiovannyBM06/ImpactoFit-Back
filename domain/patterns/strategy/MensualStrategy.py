from datetime import date, timedelta
from domain.patterns.strategy.IMembresiaStrategy import IMembresiaStrategy
 
 
class MensualStrategy(IMembresiaStrategy):
    """Plan mensual: 30 días desde la fecha de inicio."""
 
    def calcularFechaVencimiento(self, fechaInicio: date) -> date:
        return fechaInicio + timedelta(days=30)