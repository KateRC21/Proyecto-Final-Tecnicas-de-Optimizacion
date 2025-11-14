# src/models/constraints.py
# Definición detallada de restricciones del modelo

"""
PROPÓSITO:
-----------
Define todas las restricciones del modelo de optimización.
Separa las restricciones en funciones modulares para facilitar
el mantenimiento y comprensión del modelo.

RESTRICCIONES DEL MODELO:
--------------------------

1. restriccion_conservacion_flujo(modelo, grafo, emergencias):
   CONSERVACIÓN DE FLUJO:
   Para cada flujo k y cada nodo i:
   - Si i es el origen de k: salida - entrada = 1
   - Si i es el destino de k: entrada - salida = 1
   - Si i es un nodo intermedio: entrada = salida
   
   Matemáticamente:
   Σ(x[i,j,k]) - Σ(x[j,i,k]) = b[i,k]
   donde b[i,k] = 1 si i es origen, -1 si es destino, 0 en otro caso

2. restriccion_una_ambulancia_por_emergencia(modelo, emergencias, ambulancias):
   ASIGNACIÓN ÚNICA:
   Cada emergencia debe ser atendida por exactamente una ambulancia
   
   Σ(y[k,a]) = 1  para todo k (emergencia)

3. restriccion_tipo_ambulancia_segun_prioridad(modelo, emergencias, ambulancias):
   TIPO ADECUADO DE AMBULANCIA:
   La ambulancia asignada debe ser apropiada para el tipo de emergencia:
   - Emergencia leve → Ambulancia básica o superior
   - Emergencia media → Ambulancia intermedia o superior
   - Emergencia grave → Ambulancia grave (UCI móvil)
   
   Si prioridad[k] = 'grave':
       y[k,a] = 0 para a ≠ ambulancia_grave

4. restriccion_capacidad_ambulancias(modelo, hospitales, ambulancias):
   DISPONIBILIDAD DE AMBULANCIAS:
   No se pueden usar más ambulancias de las disponibles en cada hospital
   
   Σ(y[k,a]) ≤ disponibles[h,a]  
   para cada hospital h y tipo de ambulancia a

5. restriccion_velocidad_en_via(modelo, grafo):
   RESPETO DE CAPACIDADES:
   La velocidad de cada flujo en cada arista no puede exceder la capacidad
   
   v[i,j,k] ≤ capacity[i,j]  para todo i,j,k

6. restriccion_velocidad_minima_requerida(modelo, emergencias):
   VELOCIDAD REQUERIDA:
   Cada flujo debe mantener al menos su velocidad requerida
   (esto puede modelarse como restricción suave con penalización)
   
   v[i,j,k] ≥ R[k] * x[i,j,k]  si x[i,j,k] = 1

7. restriccion_calculo_tiempo(modelo, grafo):
   CÁLCULO DE TIEMPO DE RESPUESTA:
   El tiempo de cada flujo es la suma de tiempos en cada arista
   
   t[k] = Σ( (length[i,j] / v[i,j,k]) * x[i,j,k] )

8. restriccion_tiempo_maximo_respuesta(modelo, emergencias, tiempo_max):
   TIEMPO LÍMITE:
   Las emergencias graves deben atenderse en menos de tiempo_max
   
   t[k] ≤ tiempo_max  si prioridad[k] = 'grave'

9. restriccion_flujo_binario(modelo):
   NATURALEZA BINARIA:
   Una ambulancia usa completamente una arista o no la usa
   
   x[i,j,k] ∈ {0, 1}

10. restriccion_vinculacion_flujo_asignacion(modelo):
    CONSISTENCIA:
    Si una ambulancia a es asignada a emergencia k, 
    debe existir un camino de flujo correspondiente
    
    Si y[k,a] = 1, entonces existe un camino en x[i,j,k]

11. (OPCIONAL) restriccion_no_ciclos(modelo):
    PREVENCIÓN DE CICLOS:
    Las rutas no deben contener ciclos
    (usualmente esto se garantiza automáticamente por conservación de flujo)

12. (OPCIONAL) restriccion_capacidad_vial_compartida(modelo):
    CAPACIDAD COMPARTIDA:
    Si múltiples flujos usan la misma arista, la suma de sus requerimientos
    no debe exceder la capacidad
    
    Σ(v[i,j,k] * x[i,j,k]) ≤ capacity[i,j]

ESTRUCTURA DE CADA FUNCIÓN:
---------------------------
def restriccion_XXX(modelo, parametros...):
    '''
    Descripción de la restricción
    
    Args:
        modelo: Objeto del modelo PuLP/Gurobi
        parametros: Datos necesarios
    
    Returns:
        None (modifica el modelo in-place)
    '''
    # Implementación de la restricción
    pass

NOTAS IMPORTANTES:
------------------
- Algunas restricciones pueden relajarse si el modelo es infactible
- La restricción de velocidad mínima puede ser "suave" (penalización)
- Considerar big-M para algunas restricciones lógicas
- Validar que las restricciones no sean contradictorias
- Testear con casos pequeños primero

LINEARIZACIÓN:
--------------
Si aparecen productos de variables (ej: v[i,j,k] * x[i,j,k]):
- Usar técnicas de linearización estándar
- Introducir variables auxiliares si es necesario
- Consultar literatura de optimización lineal entera mixta
"""

