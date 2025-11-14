# src/utils/calculations.py
# Funciones de cálculo: distancias, tiempos, costos

"""
PROPÓSITO:
-----------
Proporciona funciones matemáticas y de cálculo utilizadas en todo el proyecto.
Centraliza operaciones comunes para evitar duplicación de código.

FUNCIONALIDADES PRINCIPALES:
-----------------------------

1. calcular_distancia_haversine(lat1, lon1, lat2, lon2):
   - Calcula la distancia real entre dos puntos geográficos
   - Usa la fórmula de Haversine (considera curvatura de la Tierra)
   - Parámetros: latitudes y longitudes en grados decimales
   - Retorna: distancia en kilómetros (float)
   
   FÓRMULA:
   a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
   c = 2 * atan2(√a, √(1-a))
   d = R * c  (donde R = 6371 km, radio de la Tierra)

2. calcular_distancia_euclidiana(x1, y1, x2, y2):
   - Distancia euclidiana simple entre dos puntos
   - Útil para coordenadas proyectadas (no geográficas)
   - Retorna: distancia (float)

3. calcular_tiempo_viaje(distancia_km, velocidad_kmh):
   - Calcula el tiempo de viaje
   - Parámetros:
     * distancia_km: distancia en kilómetros
     * velocidad_kmh: velocidad en km/h
   - Retorna: tiempo en minutos (float)
   - Fórmula: tiempo_min = (distancia_km / velocidad_kmh) * 60

4. calcular_costo_ruta(distancia_km, tiempo_min, tipo_ambulancia, costos):
   - Calcula el costo total de una ruta
   - Componentes:
     * Costo fijo por servicio
     * Costo por kilómetro
     * Costo por minuto
   - Parámetros:
     * distancia_km: distancia recorrida
     * tiempo_min: tiempo de viaje
     * tipo_ambulancia: 'basica', 'intermedia', 'grave'
     * costos: dict con estructura de costos
   - Retorna: costo total en COP (float)
   
   FÓRMULA:
   costo_total = costo_fijo + (distancia * costo_km) + (tiempo * costo_min)

5. calcular_distancia_ruta(grafo, lista_nodos):
   - Calcula la distancia total de una ruta (lista de nodos)
   - Suma las longitudes de todas las aristas en la ruta
   - Parámetros:
     * grafo: NetworkX graph
     * lista_nodos: [nodo1, nodo2, ..., nodoN]
   - Retorna: distancia total en kilómetros (float)

6. calcular_tiempo_ruta(grafo, lista_nodos):
   - Calcula el tiempo total de una ruta
   - Considera velocidad en cada arista
   - Retorna: tiempo total en minutos (float)

7. convertir_metros_a_km(metros):
   - Conversión simple de unidades
   - Retorna: kilómetros (float)

8. convertir_kmh_a_ms(velocidad_kmh):
   - Convierte km/h a m/s
   - Útil para algunos cálculos
   - Retorna: velocidad en m/s (float)

9. calcular_velocidad_promedio(distancia_km, tiempo_min):
   - Calcula velocidad promedio de una ruta
   - Retorna: velocidad en km/h (float)
   - Fórmula: v = (distancia / tiempo) * 60

10. calcular_centro_masa(coordenadas):
    - Calcula el centroide de un conjunto de coordenadas
    - Útil para encontrar centro de una zona
    - Parámetros: lista de tuplas [(lat1, lon1), (lat2, lon2), ...]
    - Retorna: tupla (lat_centro, lon_centro)

11. calcular_bounding_box(coordenadas):
    - Calcula el rectángulo delimitador de un conjunto de puntos
    - Retorna: dict {'north': lat_max, 'south': lat_min, 
                     'east': lon_max, 'west': lon_min}

12. interpolar_coordenadas(lat1, lon1, lat2, lon2, num_puntos):
    - Genera puntos intermedios entre dos coordenadas
    - Útil para visualización de rutas
    - Retorna: lista de tuplas con coordenadas interpoladas

13. calcular_bearing(lat1, lon1, lat2, lon2):
    - Calcula la dirección (bearing) entre dos puntos
    - Retorna: ángulo en grados (0-360)
    - 0° = Norte, 90° = Este, 180° = Sur, 270° = Oeste

14. estimar_consumo_combustible(distancia_km, tipo_ambulancia):
    - Estima el consumo de combustible
    - Consumo típico de ambulancias: 15-25 km/L
    - Retorna: litros de combustible (float)

CONSTANTES ÚTILES:
------------------
RADIO_TIERRA_KM = 6371.0
VELOCIDAD_LUZ_KMH = 299792.458  # Límite teórico (por si acaso 😄)
FACTOR_CONGESTION_DEFAULT = 0.8  # 80% de velocidad libre

NOTAS MATEMÁTICAS:
------------------
- Haversine es preciso para distancias cortas-medias (< 500 km)
- Para distancias muy cortas, euclidiana puede ser suficiente
- Considerar usar geopy o shapely para cálculos complejos
- math y numpy son las librerías principales

EJEMPLO DE USO:
---------------
from src.utils.calculations import (
    calcular_distancia_haversine,
    calcular_tiempo_viaje,
    calcular_costo_ruta
)

# Calcular distancia entre dos puntos
dist = calcular_distancia_haversine(6.2442, -75.5812, 6.2087, -75.5666)
print(f"Distancia: {dist:.2f} km")

# Calcular tiempo a 60 km/h
tiempo = calcular_tiempo_viaje(dist, 60)
print(f"Tiempo: {tiempo:.2f} minutos")

# Calcular costo
costo = calcular_costo_ruta(dist, tiempo, 'grave', COSTOS)
print(f"Costo: ${costo:,.0f} COP")
"""

