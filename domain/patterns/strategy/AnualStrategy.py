from datetime import date, timedelta
from domain.patterns.strategy import IMembresiaStrategy

class AnualStrategy(IMembresiaStrategy):
    """Plan anual: 365 días desde la fecha de inicio."""
 
    def calcularFechaVencimiento(self, fechaInicio: date) -> date:
        return fechaInicio + timedelta(days=365)