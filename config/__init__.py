# config/__init__.py
# Módulo de configuración del sistema

"""
Este módulo centraliza todas las configuraciones del sistema:
- Parámetros de optimización
- Costos operacionales
- Ubicaciones geográficas
- Valores por defecto

Permite importar configuraciones fácilmente desde cualquier parte del proyecto:
    from config import PARAMETROS, COSTOS, HOSPITALES
    
EJEMPLO DE USO:
---------------
from config import COSTOS, PRIORIDAD_A_AMBULANCIA, calcular_costo_servicio

# Obtener configuración de ambulancia
config_tab = COSTOS['TAB_leve']
print(f"Costo por km: ${config_tab['costo_por_km']}")

# Calcular costo de un servicio
costo_total = calcular_costo_servicio('TAB_leve', distancia_km=15)
print(f"Costo total: ${costo_total:,.0f} COP")

# Obtener tipo de ambulancia según prioridad
tipo_amb = PRIORIDAD_A_AMBULANCIA['grave']
print(f"Para urgencia grave: {tipo_amb}")
"""

# Importar desde submódulos
# Nota: Descomentar estas líneas cuando implementes los archivos

# from config.parametros import PARAMETROS
# from config.costos import (
#     COSTOS,
#     PRIORIDAD_A_AMBULANCIA,
#     AMBULANCIA_A_PRIORIDAD,
#     NIVEL_A_AMBULANCIA,
#     VALORES_DEFAULT_INTERFAZ,
#     calcular_costo_servicio,
#     obtener_desglose_costo,
#     validar_tipo_ambulancia_para_prioridad,
#     calcular_costo_con_valores_usuario,
#     obtener_info_ambulancia_por_prioridad
# )
# from config.ubicaciones import HOSPITALES, ZONAS_EMERGENCIA, LIMITES_CIUDAD

# Exportar todo para acceso fácil
__all__ = [
    # Parámetros
    'PARAMETROS',
    
    # Costos
    'COSTOS',
    'PRIORIDAD_A_AMBULANCIA',
    'AMBULANCIA_A_PRIORIDAD',
    'NIVEL_A_AMBULANCIA',
    'VALORES_DEFAULT_INTERFAZ',
    'calcular_costo_servicio',
    'obtener_desglose_costo',
    'validar_tipo_ambulancia_para_prioridad',
    'calcular_costo_con_valores_usuario',  # Nueva función para GUI
    'obtener_info_ambulancia_por_prioridad',  # Nueva función helper
    
    # Ubicaciones
    'HOSPITALES',
    'ZONAS_EMERGENCIA',
    'LIMITES_CIUDAD'
]

