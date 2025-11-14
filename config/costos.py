# config/costos.py
# Definición de costos operacionales por tipo de ambulancia

"""
PROPÓSITO:
-----------
Define los costos operativos REALES de cada tipo de ambulancia basados en:
- Costos de depreciación y mantenimiento prorrateados
- Consumo de combustible real
- Costos de personal según equipo médico
- Insumos médicos según nivel de urgencia

DATOS CALCULADOS PARA MEDELLÍN, COLOMBIA (COP)

TIPOS DE AMBULANCIA:
--------------------
1. TAB (Transporte Asistencial Básico) - Urgencia LEVE
   - Personal: Conductor + Auxiliar de enfermería
   - Equipo: Básico (camilla, oxígeno, inmovilizadores, tensiómetro)
   - Costo total: $5.585 COP/km + $35.000 activación

2. TAM (Transporte Asistencial Medicalizado) - Urgencia MODERADA
   - Personal: Conductor + Auxiliar + Enfermero
   - Equipo: Intermedio (monitor signos vitales, desfibrilador, medicamentos)
   - Costo total: $10.534 COP/km + $60.000 activación

3. TAM (Transporte Asistencial Medicalizado) - Urgencia GRAVE
   - Personal: Conductor + Médico general + Enfermero
   - Equipo: Avanzado (monitor completo, medicamentos de urgencia, ventilador)
   - Costo total: $20.396 COP/km + $85.000 activación

FUENTE DE COSTOS:
-----------------
Calculados con base en:
- Depreciación de vehículo (vida útil 5 años, 100.000 km totales)
- Mantenimiento preventivo y correctivo
- Consumo de combustible real (15.52 km/galón promedio)
- Salarios del personal médico de Medellín
- Costos de insumos según protocolo de atención
"""

# ============================================================================
# CONFIGURACIÓN DE COSTOS OPERACIONALES
# ============================================================================

COSTOS = {
    'TAB_leve': {
        # Identificación
        'nombre': 'TAB - Transporte Asistencial Básico',
        'tipo_ambulancia': 'TAB',
        'nivel_urgencia': 'leve',
        'prioridad_asignada': 'leve',
        'nivel': 1,
        
        # Personal
        'equipo_medico': ['conductor', 'auxiliar_enfermeria'],
        
        # Costos operacionales
        'costo_fijo_activacion': 35000,  # $35.000 COP (cubre tiempo mínimo 30 min)
        'costo_por_km': 5585,            # $5.585 COP por kilómetro
        
        # Desglose detallado por kilómetro (para transparencia)
        'desglose_km': {
            'depreciacion_mantenimiento': 1910,  # Depreciación + mantenimiento
            'combustible': 1031,                  # Basado en consumo real
            'personal': 769,                      # Conductor + Auxiliar
            'insumos': 1875                       # Insumos médicos básicos
        },
        
        # Rangos de velocidad requerida (km/h)
        'velocidad_min_requerida': 30,
        'velocidad_max_requerida': 50,
        
        # Configuración
        'editable': True,  # Usuario puede modificar en GUI
        'color_visualizacion': 'green'  # Color en mapas
    },
    
    'TAM_moderada': {
        # Identificación
        'nombre': 'TAM - Transporte Asistencial Medicalizado (Moderada)',
        'tipo_ambulancia': 'TAM',
        'nivel_urgencia': 'moderada',
        'prioridad_asignada': 'media',
        'nivel': 2,
        
        # Personal
        'equipo_medico': ['conductor', 'auxiliar_enfermeria', 'enfermero'],
        
        # Costos operacionales
        'costo_fijo_activacion': 60000,  # $60.000 COP
        'costo_por_km': 10534,           # $10.534 COP por kilómetro
        
        # Desglose detallado por kilómetro
        'desglose_km': {
            'depreciacion_mantenimiento': 2524,
            'combustible': 1031,
            'personal': 1354,                     # Conductor + Auxiliar + Enfermero
            'insumos': 5625                       # Insumos médicos intermedios
        },
        
        # Rangos de velocidad requerida (km/h)
        'velocidad_min_requerida': 50,
        'velocidad_max_requerida': 70,
        
        # Configuración
        'editable': True,
        'color_visualizacion': 'blue'
    },
    
    'TAM_grave': {
        # Identificación
        'nombre': 'TAM - Transporte Asistencial Medicalizado (Grave)',
        'tipo_ambulancia': 'TAM',
        'nivel_urgencia': 'grave',
        'prioridad_asignada': 'grave',
        'nivel': 3,
        
        # Personal
        'equipo_medico': ['conductor', 'medico_general', 'enfermero'],
        
        # Costos operacionales
        'costo_fijo_activacion': 85000,  # $85.000 COP
        'costo_por_km': 20396,           # $20.396 COP por kilómetro
        
        # Desglose detallado por kilómetro
        'desglose_km': {
            'depreciacion_mantenimiento': 2524,
            'combustible': 1031,
            'personal': 1841,                     # Conductor + Médico + Enfermero
            'insumos': 15000                      # Insumos médicos avanzados
        },
        
        # Rangos de velocidad requerida (km/h)
        'velocidad_min_requerida': 70,
        'velocidad_max_requerida': 90,
        
        # Configuración
        'editable': True,
        'color_visualizacion': 'darkred'
    }
}

# ============================================================================
# MAPEOS Y REFERENCIAS
# ============================================================================

# Mapeo de prioridad clínica a tipo de ambulancia
PRIORIDAD_A_AMBULANCIA = {
    'leve': 'TAB_leve',
    'media': 'TAM_moderada',
    'grave': 'TAM_grave'
}

# Alias inverso (para búsquedas)
AMBULANCIA_A_PRIORIDAD = {
    'TAB_leve': 'leve',
    'TAM_moderada': 'media',
    'TAM_grave': 'grave'
}

# Mapeo por nivel numérico (útil para comparaciones)
NIVEL_A_AMBULANCIA = {
    1: 'TAB_leve',
    2: 'TAM_moderada',
    3: 'TAM_grave'
}

# ============================================================================
# VALORES POR DEFECTO PARA LA INTERFAZ GRÁFICA
# ============================================================================

VALORES_DEFAULT_INTERFAZ = {
    'Ambulancia TAB - Urgencia Leve': {
        'costo_activacion': 35000,
        'costo_por_km': 5585,
        'velocidad_requerida_min': 30,
        'velocidad_requerida_max': 50,
        'editable': True,
        'descripcion': 'Para emergencias leves. Equipo: Conductor + Auxiliar'
    },
    
    'Ambulancia TAM - Urgencia Moderada': {
        'costo_activacion': 60000,
        'costo_por_km': 10534,
        'velocidad_requerida_min': 50,
        'velocidad_requerida_max': 70,
        'editable': True,
        'descripcion': 'Para emergencias moderadas. Equipo: Conductor + Auxiliar + Enfermero'
    },
    
    'Ambulancia TAM - Urgencia Grave': {
        'costo_activacion': 85000,
        'costo_por_km': 20396,
        'velocidad_requerida_min': 70,
        'velocidad_requerida_max': 90,
        'editable': True,
        'descripcion': 'Para emergencias graves. Equipo: Conductor + Médico + Enfermero'
    }
}

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def calcular_costo_servicio(tipo_ambulancia, distancia_km, tiempo_min=None):
    """
    Calcula el costo total de un servicio de ambulancia.
    
    Args:
        tipo_ambulancia (str): 'TAB_leve', 'TAM_moderada', 'TAM_grave'
        distancia_km (float): Distancia recorrida en kilómetros
        tiempo_min (float, optional): Tiempo de servicio (no usado actualmente)
    
    Returns:
        float: Costo total del servicio en COP
    
    Ejemplo:
        >>> calcular_costo_servicio('TAB_leve', 10)
        90850  # 35000 + (10 * 5585)
    """
    if tipo_ambulancia not in COSTOS:
        raise ValueError(f"Tipo de ambulancia '{tipo_ambulancia}' no reconocido")
    
    config = COSTOS[tipo_ambulancia]
    costo_fijo = config['costo_fijo_activacion']
    costo_variable = distancia_km * config['costo_por_km']
    
    return costo_fijo + costo_variable


def obtener_desglose_costo(tipo_ambulancia, distancia_km):
    """
    Obtiene el desglose detallado del costo de un servicio.
    
    Args:
        tipo_ambulancia (str): Tipo de ambulancia
        distancia_km (float): Distancia recorrida
    
    Returns:
        dict: Desglose de costos por categoría
    """
    if tipo_ambulancia not in COSTOS:
        raise ValueError(f"Tipo de ambulancia '{tipo_ambulancia}' no reconocido")
    
    config = COSTOS[tipo_ambulancia]
    desglose = config['desglose_km']
    
    return {
        'costo_fijo': config['costo_fijo_activacion'],
        'depreciacion_mantenimiento': desglose['depreciacion_mantenimiento'] * distancia_km,
        'combustible': desglose['combustible'] * distancia_km,
        'personal': desglose['personal'] * distancia_km,
        'insumos': desglose['insumos'] * distancia_km,
        'total': calcular_costo_servicio(tipo_ambulancia, distancia_km)
    }


def validar_tipo_ambulancia_para_prioridad(tipo_ambulancia, prioridad):
    """
    Valida si un tipo de ambulancia es apropiado para una prioridad dada.
    
    Args:
        tipo_ambulancia (str): Tipo de ambulancia
        prioridad (str): 'leve', 'media', 'grave'
    
    Returns:
        bool: True si es apropiado, False en caso contrario
    
    Reglas:
        - Urgencia leve: Solo TAB
        - Urgencia media: TAM moderada o TAM grave
        - Urgencia grave: Solo TAM grave
    """
    nivel_ambulancia = COSTOS[tipo_ambulancia]['nivel']
    
    if prioridad == 'leve':
        return nivel_ambulancia == 1
    elif prioridad == 'media':
        return nivel_ambulancia >= 2
    elif prioridad == 'grave':
        return nivel_ambulancia == 3
    
    return False


def calcular_costo_con_valores_usuario(prioridad, distancia_km, costos_usuario=None):
    """
    Calcula el costo usando valores personalizados del usuario o valores por defecto.
    Esta función es útil para usar en el modelo de optimización con la GUI.
    
    Args:
        prioridad (str): 'leve', 'media', 'grave'
        distancia_km (float): Distancia recorrida en kilómetros
        costos_usuario (dict, optional): Diccionario con costos personalizados
            Estructura esperada:
            {
                'leve': {'costo_fijo': X, 'costo_km': Y},
                'media': {'costo_fijo': X, 'costo_km': Y},
                'grave': {'costo_fijo': X, 'costo_km': Y}
            }
    
    Returns:
        float: Costo total del servicio en COP
    
    Ejemplo:
        # Con valores por defecto
        >>> costo = calcular_costo_con_valores_usuario('leve', 10)
        90850
        
        # Con valores personalizados
        >>> costos = {'leve': {'costo_fijo': 40000, 'costo_km': 6000}}
        >>> costo = calcular_costo_con_valores_usuario('leve', 10, costos)
        100000
    """
    # Si el usuario proporcionó costos personalizados, usarlos
    if costos_usuario and prioridad in costos_usuario:
        config = costos_usuario[prioridad]
        costo_fijo = config['costo_fijo']
        costo_km = config['costo_km']
    else:
        # Usar valores por defecto
        tipo_ambulancia = PRIORIDAD_A_AMBULANCIA[prioridad]
        config = COSTOS[tipo_ambulancia]
        costo_fijo = config['costo_fijo_activacion']
        costo_km = config['costo_por_km']
    
    return costo_fijo + (distancia_km * costo_km)


def obtener_info_ambulancia_por_prioridad(prioridad):
    """
    Obtiene información completa de la ambulancia asignada a una prioridad.
    
    Args:
        prioridad (str): 'leve', 'media', 'grave'
    
    Returns:
        dict: Información completa de la ambulancia
    
    Ejemplo:
        >>> info = obtener_info_ambulancia_por_prioridad('grave')
        >>> print(info['nombre'])
        'TAM - Transporte Asistencial Medicalizado (Grave)'
        >>> print(info['equipo_medico'])
        ['conductor', 'medico_general', 'enfermero']
    """
    tipo_ambulancia = PRIORIDAD_A_AMBULANCIA[prioridad]
    return COSTOS[tipo_ambulancia].copy()

# ============================================================================
# NOTAS Y CONSIDERACIONES
# ============================================================================

"""
NOTAS IMPORTANTES:
------------------
1. Los costos están en pesos colombianos (COP)
2. El costo de activación cubre el tiempo mínimo de servicio (30 minutos)
3. Los costos por km incluyen TODOS los componentes operacionales
4. Los valores son editables desde la GUI para experimentación
5. Los rangos de velocidad son referenciales para el modelo de optimización

CÓMO USAR EN EL MODELO:
------------------------
from config.costos import COSTOS, calcular_costo_servicio

# Obtener costo de un servicio
costo = calcular_costo_servicio('TAB_leve', distancia_km=15)

# Verificar que ambulancia sea apropiada
from config.costos import validar_tipo_ambulancia_para_prioridad
es_valido = validar_tipo_ambulancia_para_prioridad('TAB_leve', 'leve')

ACTUALIZACIÓN DE COSTOS:
-------------------------
Para modificar costos:
1. Editar los valores en el diccionario COSTOS
2. Mantener consistencia en el desglose_km
3. Actualizar VALORES_DEFAULT_INTERFAZ si es necesario
4. Verificar que la suma de desglose_km coincida con costo_por_km

FACTORES NO INCLUIDOS (SIMPLIFICACIONES):
------------------------------------------
- No se considera variación de costos por hora del día
- No se incluye costo de oportunidad
- No se considera desgaste adicional por tráfico pesado
- Costos de peajes o vías rápidas no incluidos
- Seguro y aspectos legales no considerados explícitamente
"""

