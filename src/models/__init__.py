# src/models/__init__.py
# Módulo de modelos de optimización matemática

"""
Este módulo contiene:
- Modelo de optimización principal (PuLP)
- Multi-Commodity Flow Problem para ruteo de ambulancias
- Función objetivo: Minimización de costos operacionales
- Restricciones: Conservación de flujo y capacidades de vías
"""

from .optimization_model import (
    AmbulanceOptimizationModel,
    resolver_modelo_ambulancias
)

__all__ = [
    'AmbulanceOptimizationModel',
    'resolver_modelo_ambulancias'
]

