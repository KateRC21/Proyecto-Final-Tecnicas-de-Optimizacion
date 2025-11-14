# src/models/optimization_model.py
# Modelo de optimización Multi-Commodity Flow para ruteo de ambulancias

"""
MODELO MATEMÁTICO: RUTEO ÓPTIMO DE AMBULANCIAS
Multi-Commodity Flow Problem con Restricciones de Capacidad

Implementación basada en PuLP para resolver el problema de asignación
y ruteo de ambulancias considerando:
- Múltiples flujos (una ambulancia por emergencia)
- Capacidades de vías (velocidades máximas)
- Velocidades requeridas según severidad
- Minimización de costos operacionales

Autor: Sistema de Optimización de Ambulancias
"""

import time
from typing import Dict, List, Tuple, Optional, Any
import networkx as nx
from pulp import (
    LpProblem, LpMinimize, LpVariable, LpStatus, 
    lpSum, PULP_CBC_CMD, LpStatusOptimal
)

from config.costos import (
    PRIORIDAD_A_AMBULANCIA, 
    COSTOS,
    calcular_costo_con_valores_usuario
)


class AmbulanceOptimizationModel:
    """
    Modelo de optimización para ruteo de ambulancias.
    
    Resuelve un Multi-Commodity Flow Problem donde cada emergencia es un commodity
    (flujo) independiente que debe viajar desde un origen común (clínica) hasta
    su destino específico, respetando capacidades de vías.
    """
    
    def __init__(
        self,
        grafo: nx.MultiDiGraph,
        emergencias: List[Dict],
        nodo_origen: int,
        costos_usuario: Optional[Dict] = None,
        parametros: Optional[Dict] = None
    ):
        """
        Inicializa el modelo de optimización.
        
        Args:
            grafo: NetworkX MultiDiGraph con atributos:
                   - grafo[u][v][key]['length']: distancia en metros
                   - grafo[u][v][key]['capacity']: velocidad máxima en km/h
            
            emergencias: Lista de diccionarios con:
                   - id: identificador
                   - severidad: 'leve', 'media', 'grave'
                   - velocidad_requerida: velocidad mínima en km/h
                   - nodo_destino: nodo destino en el grafo
                   - ambulancia_id: identificador de ambulancia
            
            nodo_origen: ID del nodo origen (clínica)
            
            costos_usuario: (opcional) Diccionario con costos personalizados:
                   {
                       'leve': {'costo_fijo': X, 'costo_km': Y},
                       'media': {'costo_fijo': X, 'costo_km': Y},
                       'grave': {'costo_fijo': X, 'costo_km': Y}
                   }
            
            parametros: (opcional) Parámetros adicionales:
                   - time_limit: tiempo límite del solver en segundos (default: 300)
                   - gap: gap de optimalidad (default: 0.01)
                   - verbose: mostrar output del solver (default: False)
        """
        # Simplificar MultiDiGraph a DiGraph (elimina complejidad de keys)
        print(f"\n{'='*70}")
        print("🔄 SIMPLIFICANDO GRAFO")
        print(f"{'='*70}")
        print(f"Tipo original: {type(grafo)}")
        print(f"Aristas originales (con keys): {len(list(grafo.edges(keys=True)))}")
        
        self.grafo = self._simplificar_a_digraph(grafo)
        
        print(f"Tipo simplificado: {type(self.grafo)}")
        print(f"Aristas simplificadas: {len(list(self.grafo.edges()))}")
        print(f"{'='*70}\n")
        
        self.emergencias = emergencias
        self.nodo_origen = nodo_origen
        self.costos_usuario = costos_usuario
        
        # Parámetros del solver
        self.parametros = parametros or {}
        self.time_limit = self.parametros.get('time_limit', 300)
        self.gap = self.parametros.get('gap', 0.01)
        self.verbose = self.parametros.get('verbose', False)
        
        # Datos derivados
        self.num_emergencias = len(emergencias)
        self.nodos = list(self.grafo.nodes())
        self.aristas = list(self.grafo.edges())  # (u, v) - sin key
        
        # Modelo y variables (se crean al construir)
        self.modelo = None
        self.x = {}  # Variables de decisión
        
        # Resultados (se llenan después de resolver)
        self.estado = None
        self.valor_objetivo = None
        self.tiempo_resolucion = None
        self.rutas = None
        self.detalles_flujos = None
        self.uso_aristas = None
    
    def _simplificar_a_digraph(self, multi_grafo):
        """
        Convierte MultiDiGraph a DiGraph simple.
        
        Si hay múltiples aristas entre el mismo par de nodos (i, j),
        toma la de MAYOR capacidad (mejor opción para el ruteo).
        
        Args:
            multi_grafo: NetworkX MultiDiGraph
        
        Returns:
            nx.DiGraph: Grafo simplificado
        """
        import networkx as nx
        
        grafo_simple = nx.DiGraph()
        
        # Copiar nodos con sus atributos
        for nodo, data in multi_grafo.nodes(data=True):
            grafo_simple.add_node(nodo, **data)
        
        # Para cada par de nodos, tomar la mejor arista
        pares_procesados = set()
        
        for i, j, key, data in multi_grafo.edges(keys=True, data=True):
            if (i, j) not in pares_procesados:
                # Primera vez viendo este par
                pares_procesados.add((i, j))
                
                # Si hay múltiples aristas, elegir la de mayor capacidad
                if multi_grafo.number_of_edges(i, j) > 1:
                    mejor_capacidad = -1
                    mejor_data = None
                    
                    for k, d in multi_grafo[i][j].items():
                        cap = d.get('capacity', 0)
                        if cap > mejor_capacidad:
                            mejor_capacidad = cap
                            mejor_data = d
                    
                    grafo_simple.add_edge(i, j, **mejor_data)
                else:
                    # Solo hay una arista, usarla directamente
                    grafo_simple.add_edge(i, j, **data)
        
        return grafo_simple
    
    def construir_modelo(self):
        """
        Construye el modelo de optimización completo:
        1. Crea variables de decisión
        2. Define función objetivo
        3. Agrega restricciones
        """
        print(f"\n{'='*70}")
        print("CONSTRUYENDO MODELO DE OPTIMIZACIÓN")
        print(f"{'='*70}")
        print(f"Emergencias: {self.num_emergencias}")
        print(f"Nodos: {len(self.nodos)}")
        print(f"Aristas: {len(self.aristas)}")
        
        # Crear problema
        self.modelo = LpProblem("Ruteo_Ambulancias", LpMinimize)
        
        # 1. Crear variables de decisión
        self._crear_variables()
        
        # 2. Definir función objetivo
        self._definir_funcion_objetivo()
        
        # 3. Agregar restricciones
        self._agregar_restricciones()
        
        print(f"✓ Modelo construido exitosamente")
        print(f"  - Variables: {len(self.x)}")
        print(f"  - Restricciones: {len(self.modelo.constraints)}")
        print(f"{'='*70}\n")
    
    def _crear_variables(self):
        """
        Crea las variables de decisión x[i,j,k] ∈ {0,1}
        
        x[i,j,k] = 1 si el flujo k usa la arista (i,j)
        """
        print("  Creando variables de decisión...")
        
        for k in range(self.num_emergencias):
            for (i, j) in self.aristas:
                var_name = f"x_{i}_{j}_{k}"
                self.x[i, j, k] = LpVariable(var_name, cat='Binary')
        
        print(f"  ✓ {len(self.x)} variables binarias creadas")
    
    def _definir_funcion_objetivo(self):
        """
        Define la función objetivo: Minimizar costos totales
        
        Z = Σ CF[tipo_k] + Σ Σ (d_ij/1000) × CK[tipo_k] × x_ijk
   
   Donde:
        - CF[tipo_k]: Costo fijo de activación
        - d_ij: Distancia de arista en metros
        - CK[tipo_k]: Costo por kilómetro
        - x_ijk: Variable binaria de flujo
        """
        print("  Definiendo función objetivo...")
        
        # Costos fijos (una ambulancia por emergencia)
        costo_fijo_total = 0
        for emerg in self.emergencias:
            severidad = emerg['severidad']
            
            # Obtener costo fijo (usuario o default)
            if self.costos_usuario and severidad in self.costos_usuario:
                costo_fijo = self.costos_usuario[severidad]['costo_fijo']
            else:
                tipo_amb = PRIORIDAD_A_AMBULANCIA[severidad]
                costo_fijo = COSTOS[tipo_amb]['costo_fijo_activacion']
            
            costo_fijo_total += costo_fijo
        
        # Costos variables (distancia × costo_km)
        costo_variable = []
        for k, emerg in enumerate(self.emergencias):
            severidad = emerg['severidad']
            
            # Obtener costo por km (usuario o default)
            if self.costos_usuario and severidad in self.costos_usuario:
                costo_km = self.costos_usuario[severidad]['costo_km']
            else:
                tipo_amb = PRIORIDAD_A_AMBULANCIA[severidad]
                costo_km = COSTOS[tipo_amb]['costo_por_km']
            
            # Sumar distancia × costo_km para todas las aristas del flujo k
            for (i, j) in self.aristas:
                distancia_metros = self.grafo[i][j]['length']
                distancia_km = distancia_metros / 1000.0
                costo_arista = distancia_km * costo_km * self.x[i, j, k]
                costo_variable.append(costo_arista)
        
        # Función objetivo total
        self.modelo += costo_fijo_total + lpSum(costo_variable), "Costo_Total"
        
        print(f"  ✓ Función objetivo definida")
        print(f"    - Costo fijo total: ${costo_fijo_total:,.0f} COP")
    
    def _agregar_restricciones(self):
        """
        Agrega todas las restricciones al modelo:
        1. Conservación de flujo
        2. Capacidad de vías
        """
        print("  Agregando restricciones...")
        
        # 1. Restricciones de conservación de flujo
        self._restriccion_conservacion_flujo()
        
        # 2. Restricciones de capacidad de vías
        self._restriccion_capacidad_vias()
        
        print(f"  ✓ {len(self.modelo.constraints)} restricciones agregadas")
    
    def _restriccion_conservacion_flujo(self):
        """
        Restricciones de conservación de flujo para cada flujo k.
        
        Para cada nodo v y flujo k:
        - Origen: flujo_saliente - flujo_entrante = 1
        - Destino k: flujo_entrante - flujo_saliente = 1
        - Intermedios: flujo_entrante - flujo_saliente = 0
        """
        contador = 0
        
        for k, emerg in enumerate(self.emergencias):
            dest_k = emerg['nodo_destino']
            
            for nodo in self.nodos:
                # Aristas que entran al nodo
                entrantes = [
                    self.x[i, nodo, k] 
                    for (i, j) in self.aristas 
                    if j == nodo
                ]
                
                # Aristas que salen del nodo
                salientes = [
                    self.x[nodo, j, k]
                    for (i, j) in self.aristas
                    if i == nodo
                ]
                
                # Determinar tipo de nodo para este flujo
                if nodo == self.nodo_origen:
                    # Origen: genera 1 unidad de flujo
                    self.modelo += (
                        lpSum(salientes) - lpSum(entrantes) == 1,
                        f"Flujo_Origen_k{k}_n{nodo}"
                    )
                    contador += 1
                
                elif nodo == dest_k:
                    # Destino del flujo k: absorbe 1 unidad
                    self.modelo += (
                        lpSum(entrantes) - lpSum(salientes) == 1,
                        f"Flujo_Destino_k{k}_n{nodo}"
                    )
                    contador += 1
                
                else:
                    # Nodo intermedio: conservación
                    self.modelo += (
                        lpSum(entrantes) - lpSum(salientes) == 0,
                        f"Flujo_Conservacion_k{k}_n{nodo}"
                    )
                    contador += 1
        
        print(f"    ✓ {contador} restricciones de conservación de flujo")
    
    def _restriccion_capacidad_vias(self):
        """
        Restricciones de capacidad de vías.
        
        Para cada arista (i,j):
        Σ r_k × x_ijk ≤ c_ij
        
        La suma de velocidades requeridas por todos los flujos que usan la arista
        no puede exceder su capacidad.
        """
        contador = 0
        
        for (i, j) in self.aristas:
            capacidad = self.grafo[i][j]['capacity']  # km/h
            
            # Suma de velocidades requeridas de todos los flujos en esta arista
            demanda_total = []
            for k, emerg in enumerate(self.emergencias):
                velocidad_req = emerg['velocidad_requerida']  # km/h
                demanda_total.append(velocidad_req * self.x[i, j, k])
            
            # La demanda total no puede exceder la capacidad
            self.modelo += (
                lpSum(demanda_total) <= capacidad,
                f"Capacidad_a{i}_{j}"
            )
            contador += 1
        
        print(f"    ✓ {contador} restricciones de capacidad de vías")
    
    def resolver(self) -> str:
        """
        Resuelve el modelo de optimización.
        
        Returns:
            str: Estado de la solución ('Optimal', 'Infeasible', 'Unbounded', etc.)
        """
        if self.modelo is None:
            raise ValueError("El modelo no ha sido construido. Llama a construir_modelo() primero.")
        
        print(f"\n{'='*70}")
        print("RESOLVIENDO MODELO DE OPTIMIZACIÓN")
        print(f"{'='*70}")
        
        # Configurar solver
        solver = PULP_CBC_CMD(
            timeLimit=self.time_limit,
            gapRel=self.gap,
            msg=1 if self.verbose else 0
        )
        
        # Resolver
        inicio = time.time()
        self.modelo.solve(solver)
        fin = time.time()
        
        self.tiempo_resolucion = fin - inicio
        self.estado = LpStatus[self.modelo.status]
        
        # Si es óptimo, extraer valor objetivo
        if self.modelo.status == LpStatusOptimal:
            self.valor_objetivo = self.modelo.objective.value()
        
        print(f"✓ Modelo resuelto")
        print(f"  - Estado: {self.estado}")
        if self.valor_objetivo is not None:
            print(f"  - Valor objetivo: ${self.valor_objetivo:,.2f} COP")
        print(f"  - Tiempo: {self.tiempo_resolucion:.2f} segundos")
        print(f"{'='*70}\n")
        
        return self.estado
    
    def extraer_resultados(self) -> Dict[str, Any]:
        """
        Extrae los resultados del modelo resuelto.
        
        Returns:
            dict: Diccionario con resultados estructurados:
                - estado: Estado de la solución
                - costo_total: Valor objetivo
                - tiempo_resolucion: Tiempo en segundos
                - rutas: Lista de rutas (secuencias de nodos)
                - detalles: Lista con detalles de cada flujo
                - uso_aristas: Diccionario con uso de cada arista
        """
        if self.estado is None:
            raise ValueError("El modelo no ha sido resuelto. Llama a resolver() primero.")
        
        if self.estado != 'Optimal':
            return {
                'estado': self.estado,
                'costo_total': None,
                'tiempo_resolucion': self.tiempo_resolucion,
                'rutas': None,
                'detalles': None,
                'uso_aristas': None,
                'mensaje': self._obtener_mensaje_infactibilidad()
            }
        
        print(f"\n{'='*70}")
        print("EXTRAYENDO RESULTADOS")
        print(f"{'='*70}")
        
        # Extraer rutas
        self.rutas = self._reconstruir_rutas()
        
        # Calcular detalles de cada flujo
        self.detalles_flujos = self._calcular_detalles_flujos()
        
        # Calcular uso de aristas
        self.uso_aristas = self._calcular_uso_aristas()
        
        resultado = {
            'estado': self.estado,
            'costo_total': self.valor_objetivo,
            'tiempo_resolucion': self.tiempo_resolucion,
            'rutas': self.rutas,
            'detalles': self.detalles_flujos,
            'uso_aristas': self.uso_aristas
        }
        
        print(f"✓ Resultados extraídos exitosamente")
        print(f"{'='*70}\n")
        
        return resultado
    
    def _reconstruir_rutas(self) -> List[List[int]]:
        """
        Reconstruye las rutas a partir de las variables x resueltas.
        
        Returns:
            List[List[int]]: Lista de rutas, cada ruta es una secuencia de nodos
        """
        print("  Reconstruyendo rutas...")
        
        rutas = []
        
        for k, emerg in enumerate(self.emergencias):
            dest_k = emerg['nodo_destino']
            ruta = self._reconstruir_ruta_flujo(k, dest_k)
            rutas.append(ruta)
            
            print(f"    Flujo {k+1}: {len(ruta)} nodos, "
                  f"{self.nodo_origen} → {dest_k}")
        
        return rutas
    
    def _reconstruir_ruta_flujo(self, k: int, destino: int) -> List[int]:
        """
        Reconstruye la ruta de un flujo específico.
        
        Args:
            k: Índice del flujo
            destino: Nodo destino del flujo
        
        Returns:
            List[int]: Secuencia de nodos de la ruta
        """
        ruta = [self.nodo_origen]
        nodo_actual = self.nodo_origen
        visitados = set([self.nodo_origen])
        
        # Seguir el flujo hasta llegar al destino
        while nodo_actual != destino:
            # Buscar la arista saliente con x[nodo_actual, j, k] = 1
            siguiente_nodo = None
            
            for (i, j) in self.aristas:
                if i == nodo_actual:
                    if self.x[i, j, k].varValue > 0.5:  # Binario = 1
                        siguiente_nodo = j
                        break
            
            if siguiente_nodo is None:
                # No se encontró arista saliente (problema en el modelo)
                print(f"      ⚠️ Advertencia: No se pudo completar ruta para flujo {k}")
                break
            
            if siguiente_nodo in visitados:
                # Ciclo detectado
                print(f"      ⚠️ Advertencia: Ciclo detectado en flujo {k}")
                break
            
            ruta.append(siguiente_nodo)
            visitados.add(siguiente_nodo)
            nodo_actual = siguiente_nodo
        
        return ruta
    
    def _calcular_detalles_flujos(self) -> List[Dict]:
        """
        Calcula detalles completos de cada flujo.
        
        Returns:
            List[Dict]: Lista con detalles de cada flujo
        """
        print("  Calculando detalles de flujos...")
        
        detalles = []
        
        for k, emerg in enumerate(self.emergencias):
            severidad = emerg['severidad']
            
            # Obtener tipo de ambulancia y costos
            if self.costos_usuario and severidad in self.costos_usuario:
                costo_fijo = self.costos_usuario[severidad]['costo_fijo']
                costo_km = self.costos_usuario[severidad]['costo_km']
                tipo_amb_str = f"Ambulancia {severidad}"
            else:
                tipo_amb = PRIORIDAD_A_AMBULANCIA[severidad]
                costo_fijo = COSTOS[tipo_amb]['costo_fijo_activacion']
                costo_km = COSTOS[tipo_amb]['costo_por_km']
                tipo_amb_str = COSTOS[tipo_amb]['nombre']
            
            # Calcular distancia total de la ruta
            ruta = self.rutas[k]
            distancia_total_m = 0
            aristas_ruta = []
            velocidades_aristas = []
            
            for idx in range(len(ruta) - 1):
                nodo_i = ruta[idx]
                nodo_j = ruta[idx + 1]
                
                # Buscar la arista correspondiente
                for (i, j) in self.aristas:
                    if i == nodo_i and j == nodo_j:
                        if self.x[i, j, k].varValue > 0.5:
                            distancia_total_m += self.grafo[i][j]['length']
                            aristas_ruta.append((i, j))
                            velocidades_aristas.append(self.grafo[i][j]['capacity'])
                            break
            
            distancia_km = distancia_total_m / 1000.0
            
            # Calcular costos
            costo_variable = distancia_km * costo_km
            costo_total = costo_fijo + costo_variable
            
            detalle = {
                'emergencia_id': emerg['id'],
                'tipo_ambulancia': tipo_amb_str,
                'severidad': severidad,
                'nodo_destino': emerg['nodo_destino'],
                'velocidad_requerida': emerg['velocidad_requerida'],
                'distancia_km': distancia_km,
                'num_aristas': len(aristas_ruta),
                'costo_fijo': costo_fijo,
                'costo_variable': costo_variable,
                'costo_total': costo_total,
                'ruta_nodos': ruta,
                'ruta_aristas': aristas_ruta,
                'velocidades_aristas': velocidades_aristas
            }
            
            detalles.append(detalle)
        
        print(f"    ✓ Detalles calculados para {len(detalles)} flujos")
        return detalles
    
    def _calcular_uso_aristas(self) -> Dict[Tuple, Dict]:
        """
        Calcula el uso de cada arista por los flujos.
        
        Returns:
            Dict: Diccionario con uso de cada arista
        """
        print("  Calculando uso de aristas...")
        
        uso = {}
        
        for (i, j) in self.aristas:
            flujos_usando = []
            carga_total = 0
            
            for k, emerg in enumerate(self.emergencias):
                if self.x[i, j, k].varValue > 0.5:
                    flujos_usando.append(k + 1)  # IDs desde 1
                    carga_total += emerg['velocidad_requerida']
            
            if flujos_usando:
                capacidad = self.grafo[i][j]['capacity']
                utilizacion = carga_total / capacidad if capacidad > 0 else 0
                
                uso[(i, j)] = {
                    'num_flujos': len(flujos_usando),
                    'flujos_ids': flujos_usando,
                    'carga_total': carga_total,
                    'capacidad': capacidad,
                    'utilizacion': utilizacion
                }
        
        print(f"    ✓ {len(uso)} aristas utilizadas")
        return uso
    
    def _obtener_mensaje_infactibilidad(self) -> str:
        """
        Genera un mensaje explicativo si el modelo es infactible.
        
        Returns:
            str: Mensaje con posibles causas y soluciones
        """
        if self.estado == 'Infeasible':
            mensaje = """
El modelo no tiene solución factible. Posibles causas:

1. VELOCIDADES REQUERIDAS > CAPACIDADES:
   - Alguna emergencia requiere más velocidad de la que permiten las vías.
   - Solución: Aumentar C_MAX o disminuir R_MAX en los parámetros.

2. GRAFO DESCONECTADO:
   - No existe camino desde el origen a algún destino.
   - Solución: Verificar que el grafo esté conectado.

3. CUELLO DE BOTELLA EN CAPACIDADES:
   - Múltiples flujos comparten vías con capacidad insuficiente.
   - Solución: Aumentar las capacidades de vías o reducir velocidades requeridas.

Sugerencias:
- Revisa los parámetros de velocidades en el Panel de Control
- Genera nuevas emergencias con el botón "🎲 Generar Nuevas Emergencias"
- Ajusta los rangos de capacidades (C_MIN, C_MAX)
"""
        elif self.estado == 'Unbounded':
            mensaje = "El problema está no acotado (error en la formulación)."
        else:
            mensaje = f"Estado del solver: {self.estado}"
        
        return mensaje


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def resolver_modelo_ambulancias(
    grafo: nx.MultiDiGraph,
    emergencias: List[Dict],
    nodo_origen: int,
    costos_usuario: Optional[Dict] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Función de conveniencia para resolver el modelo completo.
    
    Args:
        grafo: Grafo de NetworkX
        emergencias: Lista de emergencias
        nodo_origen: Nodo origen
        costos_usuario: Costos personalizados (opcional)
        **kwargs: Parámetros adicionales para el modelo
    
    Returns:
        dict: Resultados del modelo
    
    Ejemplo:
        >>> resultado = resolver_modelo_ambulancias(
        ...     grafo=grafo,
        ...     emergencias=emergencias,
        ...     nodo_origen=123,
        ...     time_limit=60
        ... )
        >>> print(resultado['estado'])
        'Optimal'
        >>> print(resultado['costo_total'])
        450000.0
    """
    # Crear modelo
    modelo = AmbulanceOptimizationModel(
        grafo=grafo,
        emergencias=emergencias,
        nodo_origen=nodo_origen,
        costos_usuario=costos_usuario,
        parametros=kwargs
    )
    
    # Construir y resolver
    modelo.construir_modelo()
    estado = modelo.resolver()
    
    # Extraer resultados
    if estado == 'Optimal':
        resultados = modelo.extraer_resultados()
    else:
        resultados = {
            'estado': estado,
            'costo_total': None,
            'tiempo_resolucion': modelo.tiempo_resolucion,
            'mensaje': modelo._obtener_mensaje_infactibilidad()
        }
    
    return resultados


if __name__ == "__main__":
    print("Este módulo debe importarse, no ejecutarse directamente.")
    print("Ejemplo de uso:")
    print("""
    from src.models.optimization_model import resolver_modelo_ambulancias
    
    resultado = resolver_modelo_ambulancias(
        grafo=grafo,
        emergencias=emergencias,
        nodo_origen=nodo_origen
    )
    """)
