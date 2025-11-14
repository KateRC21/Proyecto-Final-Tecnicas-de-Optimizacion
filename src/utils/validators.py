# src/utils/validators.py
# Validaciones de datos y parámetros

"""
PROPÓSITO:
-----------
Valida datos de entrada, parámetros y configuraciones para prevenir errores
y asegurar la integridad del sistema.

FUNCIONALIDADES PRINCIPALES:
-----------------------------

1. validar_parametros(parametros):
   - Valida el diccionario de parámetros del modelo
   - Verifica:
     * R_min < R_max
     * C_min < C_max
     * Valores dentro de rangos razonables (ej: 0 < velocidad < 200)
     * Pesos de función objetivo suman a un valor razonable
   - Retorna: (bool_valido, lista_errores)

2. validar_coordenadas(lat, lon):
   - Valida que las coordenadas sean válidas
   - Verifica:
     * -90 <= lat <= 90
     * -180 <= lon <= 180
   - Retorna: (bool_valido, mensaje_error)

3. validar_grafo(grafo):
   - Valida que el grafo tenga la estructura correcta
   - Verifica:
     * No está vacío
     * Tiene atributos necesarios (length, geometry)
     * Es conexo (o tiene componentes grandes)
     * Nodos tienen coordenadas
   - Retorna: (bool_valido, dict_problemas)

4. validar_emergencia(emergencia):
   - Valida estructura de una emergencia
   - Campos requeridos: id, nodo, lat, lon, prioridad, velocidad_requerida
   - Verifica tipos de datos correctos
   - Prioridad debe ser: 'leve', 'media', 'grave'
   - Retorna: (bool_valido, lista_errores)

5. validar_hospital(hospital):
   - Valida estructura de un hospital
   - Campos requeridos: id, nombre, lat, lon, ambulancias_disponibles
   - Verifica disponibilidad >= 0
   - Retorna: (bool_valido, lista_errores)

6. validar_rango(valor, min_val, max_val, nombre_parametro):
   - Validación genérica de rango
   - Verifica: min_val <= valor <= max_val
   - Retorna: (bool_valido, mensaje_error)

7. validar_tipo_ambulancia(tipo):
   - Valida que el tipo de ambulancia sea reconocido
   - Tipos válidos: 'basica', 'intermedia', 'grave'
   - Retorna: bool

8. validar_prioridad(prioridad):
   - Valida que la prioridad sea válida
   - Prioridades válidas: 'leve', 'media', 'grave'
   - También acepta números: 1, 2, 3
   - Retorna: bool

9. validar_resultado_optimizacion(resultado):
   - Valida la estructura del resultado del modelo
   - Verifica que tenga: status, asignaciones, metricas
   - Comprueba consistencia de datos
   - Retorna: (bool_valido, lista_advertencias)

10. validar_ruta(ruta, grafo):
    - Valida que una ruta (lista de nodos) sea válida en el grafo
    - Verifica:
      * Todos los nodos existen en el grafo
      * Existe arista entre nodos consecutivos
      * No hay ciclos innecesarios
    - Retorna: (bool_valida, lista_problemas)

11. validar_costos(dict_costos):
    - Valida estructura del diccionario de costos
    - Verifica que todos los tipos de ambulancia tengan costos definidos
    - Costos deben ser números positivos
    - Retorna: (bool_valido, lista_errores)

12. validar_entrada_usuario(valor, tipo_esperado, rango=None):
    - Validación genérica para entradas de GUI
    - Verifica tipo de dato
    - Opcionalmente verifica rango
    - Retorna: (bool_valido, valor_convertido_o_None, mensaje_error)

13. normalizar_prioridad(prioridad):
    - Normaliza diferentes formas de expresar prioridad
    - Acepta: 'leve', 'LEVE', 'Leve', 1, 'baja', etc.
    - Retorna: string normalizado ('leve', 'media', 'grave') o None si inválido

14. sanitizar_id(id_string):
    - Limpia y valida IDs de objetos
    - Remueve caracteres especiales peligrosos
    - Asegura unicidad si es necesario
    - Retorna: string limpio

EXCEPCIONES PERSONALIZADAS (OPCIONAL):
---------------------------------------
class ValidationError(Exception):
    pass

class InvalidCoordinateError(ValidationError):
    pass

class InvalidParameterError(ValidationError):
    pass

REGLAS DE VALIDACIÓN:
----------------------
RANGOS_VALIDOS = {
    'velocidad': (0, 200),  # km/h
    'distancia': (0, 1000),  # km
    'tiempo': (0, 500),  # minutos
    'costo': (0, 10000000),  # COP
    'num_emergencias': (1, 100),
    'num_ambulancias': (1, 50)
}

PRIORIDADES_VALIDAS = ['leve', 'media', 'grave']
TIPOS_AMBULANCIA_VALIDOS = ['basica', 'intermedia', 'grave']

EJEMPLO DE USO:
---------------
from src.utils.validators import (
    validar_parametros,
    validar_emergencia,
    validar_coordenadas
)

# Validar parámetros
parametros = {'r_min': 40, 'r_max': 80, 'c_min': 30, 'c_max': 100}
valido, errores = validar_parametros(parametros)
if not valido:
    print("Errores encontrados:", errores)
    raise ValueError("Parámetros inválidos")

# Validar coordenadas
valido, msg = validar_coordenadas(6.2442, -75.5812)
if not valido:
    print(f"Coordenadas inválidas: {msg}")

# Validar emergencia
emergencia = {
    'id': 'emerg_001',
    'lat': 6.2442,
    'lon': -75.5812,
    'prioridad': 'grave',
    'velocidad_requerida': 75
}
valido, errores = validar_emergencia(emergencia)
"""

