# config/parametros.py
# Parámetros configurables del modelo de optimización

"""
PROPÓSITO:
-----------
Define todos los parámetros ajustables del modelo, incluyendo valores por defecto
que se usarán en la interfaz gráfica y en ejecuciones por línea de comandos.

SISTEMA DE VELOCIDADES:
-----------------------
1. CAPACIDADES DE VÍAS: Valores aleatorios dentro de [C_MIN, C_MAX]
2. VELOCIDADES REQUERIDAS: Divididas en tres niveles de emergencia:
   - Leve: [R_MIN, R_MIN + tercio]
   - Media: [R_MIN + tercio, R_MIN + 2*tercio]
   - Grave: [R_MIN + 2*tercio, R_MAX]
"""

import random

# ============================================================================
# 1. RANGOS DE VELOCIDADES REQUERIDAS (por nivel de emergencia)
# ============================================================================

# Rango configurado por el usuario
R_MIN = 30  # Velocidad mínima requerida (km/h)
R_MAX = 90  # Velocidad máxima requerida (km/h)

# Cálculo automático de tercios para niveles de emergencia
RANGO_TOTAL = R_MAX - R_MIN
TERCIO = RANGO_TOTAL / 3

# Sub-rangos por severidad de emergencia
RANGOS_EMERGENCIA = {
    'leve': {
        'min': R_MIN,
        'max': R_MIN + TERCIO,
        'descripcion': 'Emergencia de baja prioridad'
    },
    'media': {
        'min': R_MIN + TERCIO,
        'max': R_MIN + 2 * TERCIO,
        'descripcion': 'Emergencia de prioridad media'
    },
    'grave': {
        'min': R_MIN + 2 * TERCIO,
        'max': R_MAX,
        'descripcion': 'Emergencia de alta prioridad'
    }
}


def generar_velocidad_emergencia(severidad):
    """
    Genera una velocidad requerida aleatoria según la severidad de la emergencia.
    
    Args:
        severidad (str): 'leve', 'media' o 'grave'
    
    Returns:
        float: Velocidad requerida en km/h
    """
    if severidad not in RANGOS_EMERGENCIA:
        raise ValueError(f"Severidad '{severidad}' no válida. Use: 'leve', 'media' o 'grave'")
    
    rango = RANGOS_EMERGENCIA[severidad]
    return random.uniform(rango['min'], rango['max'])


# ============================================================================
# 2. RANGOS DE CAPACIDADES DE VÍAS (velocidad máxima permitida)
# ============================================================================

C_MIN = 30   # Capacidad mínima de una vía (km/h)
C_MAX = 100  # Capacidad máxima de una vía (km/h)


def generar_capacidad_via():
    """
    Genera una capacidad (velocidad máxima) aleatoria para una vía.
    
    Returns:
        float: Capacidad de la vía en km/h
    """
    return random.uniform(C_MIN, C_MAX)


def generar_severidad_aleatoria():
    """
    Genera una severidad aleatoria para una emergencia.
    Cada severidad tiene igual probabilidad (33.33% cada una).
    
    Returns:
        str: 'leve', 'media' o 'grave'
    """
    return random.choice(['leve', 'media', 'grave'])


def generar_conjunto_emergencias(num_emergencias=None):
    """
    Genera un conjunto de emergencias con sus características.
    Cada emergencia tendrá una ambulancia correspondiente del mismo tipo.
    
    Args:
        num_emergencias (int, optional): Número de emergencias a generar.
                                         Si es None, se genera aleatoriamente.
    
    Returns:
        list: Lista de diccionarios con información de cada emergencia:
              - id: Identificador de la emergencia
              - severidad: 'leve', 'media' o 'grave'
              - velocidad_requerida: Velocidad en km/h según la severidad
              - ambulancia_id: ID de la ambulancia asignada (mismo número que la emergencia)
    """
    if num_emergencias is None:
        num_emergencias = generar_num_emergencias()
    
    emergencias = []
    for i in range(num_emergencias):
        severidad = generar_severidad_aleatoria()
        velocidad = generar_velocidad_emergencia(severidad)
        
        emergencias.append({
            'id': i + 1,
            'severidad': severidad,
            'velocidad_requerida': velocidad,
            'ambulancia_id': i + 1,  # Relación 1:1
            'origen': 'Clínica Medellín - Sede El Poblado'
        })
    
    return emergencias


# ============================================================================
# 3. PARÁMETROS DEL GRAFO (Medellín, Colombia)
# ============================================================================

# Ubicación: Clínica Medellín - Sede El Poblado
CENTRO_LATITUD = 6.19082795
CENTRO_LONGITUD = -75.5777409611334

# Configuración de la red
CIUDAD = "Medellín, Colombia"
NETWORK_TYPE = "drive"  # Red vehicular
SIMPLIFY = True  # Simplificar el grafo para mejor rendimiento

# Dimensiones del área de estudio (1km x 1km)
AREA_SIZE = 1000  # metros (1km)

# Parámetros para OSMnx
GRAFO_PARAMS = {
    'center_point': (CENTRO_LATITUD, CENTRO_LONGITUD),
    'dist': AREA_SIZE / 2,  # Radio desde el centro (500m para cubrir 1km²)
    'network_type': NETWORK_TYPE,
    'simplify': SIMPLIFY
}


# ============================================================================
# 4. PARÁMETROS DE SIMULACIÓN
# ============================================================================

# Rango de emergencias a generar (mantener el modelo manejable)
NUM_EMERGENCIAS_MIN = 3
NUM_EMERGENCIAS_MAX = 5

# Valor por defecto (puede ser modificado por el usuario o generado aleatoriamente)
NUM_EMERGENCIAS_DEFAULT = 4  # Valor medio del rango

# Relación 1:1 - Cada emergencia tendrá su ambulancia correspondiente
# Todas las ambulancias parten de la Clínica Medellín - Sede El Poblado
NUM_AMBULANCIAS_DEFAULT = NUM_EMERGENCIAS_DEFAULT

TIEMPO_MAX_RESPUESTA = 15     # Tiempo máximo de respuesta permitido (minutos)

# NOTA: La severidad de cada emergencia se asigna COMPLETAMENTE ALEATORIA
# No se usa distribución de probabilidades, cada emergencia tiene igual
# probabilidad de ser 'leve', 'media' o 'grave'


def generar_num_emergencias():
    """
    Genera un número aleatorio de emergencias entre el rango permitido.
    
    Returns:
        int: Número de emergencias (entre 3 y 5)
    """
    return random.randint(NUM_EMERGENCIAS_MIN, NUM_EMERGENCIAS_MAX)


# ============================================================================
# 5. PESOS DE LA FUNCIÓN OBJETIVO
# ============================================================================

PESO_TIEMPO = 0.5        # Peso del tiempo de respuesta
PESO_COSTO = 0.3         # Peso del costo operativo
PESO_PRIORIDAD = 0.2     # Peso de la prioridad clínica


# ============================================================================
# 6. OTROS PARÁMETROS
# ============================================================================

RANDOM_SEED = 42                    # Semilla para reproducibilidad
TOLERANCIA_OPTIMIZACION = 0.01      # Gap de optimalidad (1%)
TIEMPO_LIMITE_SOLVER = 300          # Tiempo límite del solver (segundos)


# ============================================================================
# DICCIONARIO CONSOLIDADO DE PARÁMETROS
# ============================================================================

PARAMETROS = {
    'velocidades_requeridas': {
        'min': R_MIN,
        'max': R_MAX,
        'tercios': RANGOS_EMERGENCIA,
        'unidad': 'km/h'
    },
    'capacidades_vias': {
        'min': C_MIN,
        'max': C_MAX,
        'unidad': 'km/h'
    },
    'grafo': {
        'ciudad': CIUDAD,
        'centro': {
            'latitud': CENTRO_LATITUD,
            'longitud': CENTRO_LONGITUD,
            'nombre': 'Clínica Medellín - Sede El Poblado'
        },
        'area_km2': (AREA_SIZE / 1000) ** 2,
        'network_type': NETWORK_TYPE,
        'simplify': SIMPLIFY
    },
    'simulacion': {
        'num_emergencias_min': NUM_EMERGENCIAS_MIN,
        'num_emergencias_max': NUM_EMERGENCIAS_MAX,
        'num_emergencias_default': NUM_EMERGENCIAS_DEFAULT,
        'num_ambulancias_default': NUM_AMBULANCIAS_DEFAULT,
        'tiempo_max_respuesta': TIEMPO_MAX_RESPUESTA,
        'relacion_emergencia_ambulancia': '1:1',
        'asignacion_severidad': 'aleatoria',
        'origen_ambulancias': 'Clínica Medellín - Sede El Poblado'
    },
    'objetivo': {
        'peso_tiempo': PESO_TIEMPO,
        'peso_costo': PESO_COSTO,
        'peso_prioridad': PESO_PRIORIDAD
    },
    'optimizacion': {
        'random_seed': RANDOM_SEED,
        'tolerancia': TOLERANCIA_OPTIMIZACION,
        'tiempo_limite': TIEMPO_LIMITE_SOLVER
    }
}


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def set_random_seed(seed=None):
    """Configura la semilla aleatoria para reproducibilidad."""
    if seed is None:
        seed = RANDOM_SEED
    random.seed(seed)


def mostrar_configuracion():
    """Imprime la configuración actual de parámetros."""
    print("=" * 70)
    print("CONFIGURACIÓN DEL MODELO DE OPTIMIZACIÓN")
    print("=" * 70)
    print(f"\n📍 Ubicación: {CIUDAD}")
    print(f"   Centro: ({CENTRO_LATITUD}, {CENTRO_LONGITUD})")
    print(f"   Área: {AREA_SIZE/1000}km x {AREA_SIZE/1000}km = {(AREA_SIZE/1000)**2}km²")
    
    print(f"\n🚗 Capacidades de vías: [{C_MIN}, {C_MAX}] km/h")
    
    print(f"\n🚑 Velocidades requeridas por emergencia:")
    print(f"   Rango total: [{R_MIN}, {R_MAX}] km/h")
    for sev, rango in RANGOS_EMERGENCIA.items():
        print(f"   - {sev.capitalize():8s}: [{rango['min']:.1f}, {rango['max']:.1f}] km/h")
    
    print(f"\n⚙️  Simulación:")
    print(f"   - Rango emergencias: [{NUM_EMERGENCIAS_MIN}, {NUM_EMERGENCIAS_MAX}]")
    print(f"   - Emergencias por defecto: {NUM_EMERGENCIAS_DEFAULT}")
    print(f"   - Ambulancias: {NUM_AMBULANCIAS_DEFAULT} (relación 1:1 con emergencias)")
    print(f"   - Origen: Clínica Medellín - Sede El Poblado")
    print(f"   - Severidad: Asignación completamente aleatoria (33.33% cada tipo)")
    print(f"   - Tiempo máx. respuesta: {TIEMPO_MAX_RESPUESTA} min")
    
    print(f"\n🎯 Función objetivo:")
    print(f"   - Peso tiempo: {PESO_TIEMPO}")
    print(f"   - Peso costo: {PESO_COSTO}")
    print(f"   - Peso prioridad: {PESO_PRIORIDAD}")
    print("=" * 70)


if __name__ == "__main__":
    # Ejemplo de uso
    set_random_seed()
    mostrar_configuracion()
    
    print("\n\n📊 Ejemplo de generación de valores:")
    print("-" * 70)
    
    # Generar capacidades de vías
    print("\n🚗 Capacidades de vías (5 ejemplos):")
    for i in range(5):
        capacidad = generar_capacidad_via()
        print(f"   Vía {i+1}: {capacidad:.2f} km/h")
    
    # Generar conjunto completo de emergencias
    emergencias = generar_conjunto_emergencias()
    print(f"\n🚑 Conjunto de emergencias generado (n={len(emergencias)}):")
    print(f"   Todas las ambulancias parten de: {emergencias[0]['origen']}\n")
    
    for emerg in emergencias:
        print(f"   Emergencia #{emerg['id']}:")
        print(f"      - Severidad: {emerg['severidad']:8s}")
        print(f"      - Velocidad requerida: {emerg['velocidad_requerida']:.2f} km/h")
        print(f"      - Ambulancia asignada: #{emerg['ambulancia_id']}")
        print()

