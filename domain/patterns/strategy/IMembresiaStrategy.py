"""
IMembresiaStrategy.py
---------------------
PATRÓN: Strategy (GoF — Comportamental)

Interfaz base del patrón Strategy para el cálculo de membresías.

Problema que resuelve:
    Al activar una membresía, la fecha de vencimiento se calcula
    de forma diferente según el tipo de plan (mensual, trimestral, anual).
    Sin Strategy, el servicio tendría un bloque if/elif que violaría OCP:
    agregar un nuevo tipo de plan requeriría modificar el servicio.

Solución:
    Cada tipo de plan es una estrategia concreta que encapsula
    su propia lógica de cálculo. El servicio solo conoce esta
    interfaz y delega el cálculo a la estrategia correcta.

Estructura:
    IMembresiaStrategy              ← este archivo
        ├── MensualStrategy         → fecha + 30 días
        ├── TrimestralStrategy      → fecha + 90 días
        └── AnualStrategy           → fecha + 365 días
"""

from abc import ABC, abstractmethod
from datetime import date


class IMembresiaStrategy(ABC):
    """
    Contrato base para todas las estrategias de membresía.
    """

    @abstractmethod
    def calcularFechaVencimiento(self, fechaInicio: date) -> date:
        pass

    @staticmethod
    def obtenerStrategy(tipo: str) -> "IMembresiaStrategy":
        """
        Retorna la estrategia concreta según el tipo de membresía.

        Uso en el servicio:
            strategy = IMembresiaStrategy.obtenerStrategy("mensual")
            fechaVencimiento = strategy.calcularFechaVencimiento(hoy)
        """
        from domain.patterns.strategy.MensualStrategy import MensualStrategy
        from domain.patterns.strategy.TrimestralStrategy import TrimestralStrategy
        from domain.patterns.strategy.AnualStrategy import AnualStrategy

        strategies: dict[str, "IMembresiaStrategy"] = {
            "mensual":     MensualStrategy(),
            "trimestral":  TrimestralStrategy(),
            "anual":       AnualStrategy(),
        }

        strategy = strategies.get(tipo.lower())

        if strategy is None:
            tiposValidos = list(strategies.keys())
            raise ValueError(
                f"Tipo de membresía '{tipo}' no reconocido. "
                f"Tipos válidos: {tiposValidos}"
            )

        return strategy