# src/data/graph_processor.py
# Procesamiento y enriquecimiento del grafo de calles

"""
PROPÓSITO:
-----------
Procesa el grafo cargado para agregar información necesaria para la optimización:
- Asigna capacidades (velocidades máximas) aleatorias a las vías
- Calcula tiempos de viaje
- Identifica nodos más cercanos a ubicaciones específicas
- Prepara el grafo para el modelo de optimización
- Convierte grafo a GeoDataFrames para análisis y visualización
"""

import random
import numpy as np
import networkx as nx
import osmnx as ox
import geopandas as gpd
from math import radians, cos, sin, asin, sqrt
from pathlib import Path

# Importar parámetros
import sys
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia real entre dos puntos geográficos usando la fórmula de Haversine.
    
    Args:
        lat1, lon1: Coordenadas del primer punto
        lat2, lon2: Coordenadas del segundo punto
    
    Returns:
        float: Distancia en kilómetros
    """
    # Convertir grados a radianes
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radio de la Tierra en kilómetros
    r = 6371
    
    return c * r


def asignar_capacidades_aleatorias(grafo, c_min=30, c_max=100, seed=None):
    """
    Asigna una capacidad (velocidad máxima) aleatoria a cada arista del grafo.
    
    Args:
        grafo: NetworkX MultiDiGraph
        c_min (float): Velocidad mínima en km/h
        c_max (float): Velocidad máxima en km/h
        seed (int): Semilla para reproducibilidad
    
    Returns:
        grafo: Grafo modificado con atributo 'capacity' en cada arista
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    print(f"\n{'='*70}")
    print(f"ASIGNANDO CAPACIDADES ALEATORIAS A LAS VÍAS")
    print(f"{'='*70}")
    print(f"Rango de velocidades: [{c_min}, {c_max}] km/h")
    
    num_aristas = 0
    capacidades = []
    
    for u, v, key, data in grafo.edges(keys=True, data=True):
        # Generar capacidad aleatoria
        capacidad = random.uniform(c_min, c_max)
        grafo[u][v][key]['capacity'] = capacidad
        capacidades.append(capacidad)
        num_aristas += 1
    
    print(f"✓ Capacidades asignadas a {num_aristas} aristas")
    print(f"  - Capacidad mínima: {min(capacidades):.2f} km/h")
    print(f"  - Capacidad máxima: {max(capacidades):.2f} km/h")
    print(f"  - Capacidad promedio: {np.mean(capacidades):.2f} km/h")
    print(f"{'='*70}\n")
    
    return grafo


def calcular_tiempos_viaje(grafo):
    """
    Calcula el tiempo de viaje para cada arista.
    Fórmula: tiempo (min) = distancia (m) / (velocidad (km/h) * 1000/60)
    
    Args:
        grafo: NetworkX MultiDiGraph con atributos 'length' y 'capacity'
    
    Returns:
        grafo: Grafo modificado con atributo 'travel_time' en minutos
    """
    print(f"\n{'='*70}")
    print(f"CALCULANDO TIEMPOS DE VIAJE")
    print(f"{'='*70}")
    
    num_aristas = 0
    tiempos = []
    aristas_sin_datos = 0
    
    for u, v, key, data in grafo.edges(keys=True, data=True):
        # Verificar que existan los atributos necesarios
        if 'length' not in data or 'capacity' not in data:
            aristas_sin_datos += 1
            continue
        
        longitud_m = data['length']  # metros
        velocidad_kmh = data['capacity']  # km/h
        
        # Convertir velocidad a m/min: km/h * 1000/60 = m/min
        velocidad_m_min = velocidad_kmh * 1000.0 / 60.0
        
        # Calcular tiempo en minutos
        tiempo_min = longitud_m / velocidad_m_min
        
        grafo[u][v][key]['travel_time'] = tiempo_min
        tiempos.append(tiempo_min)
        num_aristas += 1
    
    print(f"✓ Tiempos calculados para {num_aristas} aristas")
    if aristas_sin_datos > 0:
        print(f"⚠ {aristas_sin_datos} aristas sin datos suficientes")
    print(f"  - Tiempo mínimo: {min(tiempos):.3f} min")
    print(f"  - Tiempo máximo: {max(tiempos):.3f} min")
    print(f"  - Tiempo promedio: {np.mean(tiempos):.3f} min")
    print(f"{'='*70}\n")
    
    return grafo


def encontrar_nodo_mas_cercano(grafo, lat, lon):
    """
    Encuentra el nodo del grafo más cercano a una coordenada geográfica.
    
    Args:
        grafo: NetworkX MultiDiGraph
        lat (float): Latitud
        lon (float): Longitud
    
    Returns:
        int: ID del nodo más cercano
    """
    return ox.distance.nearest_nodes(grafo, lon, lat)


def encontrar_nodos_cercanos_multiple(grafo, ubicaciones):
    """
    Encuentra los nodos más cercanos para múltiples ubicaciones.
    
    Args:
        grafo: NetworkX MultiDiGraph
        ubicaciones: Lista de tuplas [(lat1, lon1), (lat2, lon2), ...]
    
    Returns:
        list: Lista de IDs de nodos más cercanos
    """
    nodos = []
    for lat, lon in ubicaciones:
        nodo = encontrar_nodo_mas_cercano(grafo, lat, lon)
        nodos.append(nodo)
    return nodos


def encontrar_nodo_origen(grafo, centro_lat, centro_lon):
    """
    Encuentra el nodo de origen (más cercano al centro del grafo/clínica).
    
    Args:
        grafo: NetworkX MultiDiGraph
        centro_lat (float): Latitud del centro
        centro_lon (float): Longitud del centro
    
    Returns:
        int: ID del nodo de origen
    """
    print(f"\n{'='*70}")
    print(f"IDENTIFICANDO NODO DE ORIGEN")
    print(f"{'='*70}")
    print(f"Centro (Clínica): ({centro_lat}, {centro_lon})")
    
    nodo_origen = encontrar_nodo_mas_cercano(grafo, centro_lat, centro_lon)
    
    # Obtener información del nodo
    nodo_data = grafo.nodes[nodo_origen]
    print(f"✓ Nodo de origen encontrado: {nodo_origen}")
    print(f"  - Coordenadas: ({nodo_data['y']}, {nodo_data['x']})")
    
    # Calcular distancia real
    distancia = calcular_distancia_haversine(
        centro_lat, centro_lon,
        nodo_data['y'], nodo_data['x']
    )
    print(f"  - Distancia al centro: {distancia*1000:.2f} metros")
    print(f"{'='*70}\n")
    
    return nodo_origen


def filtrar_nodos_internos(grafo, min_salidas=3, min_entradas=3):
    """
    Filtra nodos con buena conectividad (nodos internos, no del borde).
    
    Esto evita asignar emergencias a nodos mal conectados que podrían
    hacer el modelo infactible.
    
    Args:
        grafo: NetworkX MultiDiGraph
        min_salidas (int): Mínimo de aristas salientes requeridas
        min_entradas (int): Mínimo de aristas entrantes requeridas
    
    Returns:
        list: Lista de nodos con buena conectividad
    """
    nodos_internos = []
    
    for nodo in grafo.nodes():
        # Contar aristas entrantes y salientes
        num_entrantes = len(list(grafo.predecessors(nodo)))
        num_salientes = len(list(grafo.successors(nodo)))
        
        # Solo incluir nodos con suficientes conexiones
        if num_entrantes >= min_entradas and num_salientes >= min_salidas:
            nodos_internos.append(nodo)
    
    return nodos_internos


def asignar_emergencias_a_nodos(grafo, emergencias, seed=None):
    """
    Asigna las emergencias generadas a nodos aleatorios del grafo.
    Usa las emergencias generadas por config.parametros.generar_conjunto_emergencias()
    
    IMPORTANTE: Solo asigna a nodos internos con buena conectividad
    para evitar problemas de infactibilidad.
    
    Args:
        grafo: NetworkX MultiDiGraph
        emergencias: Lista de diccionarios con info de emergencias (de parametros.py)
        seed (int): Semilla para reproducibilidad
    
    Returns:
        list: Lista de diccionarios con emergencias y sus nodos asignados
    """
    if seed is not None:
        random.seed(seed)
    
    print(f"\n{'='*70}")
    print(f"ASIGNANDO EMERGENCIAS A NODOS DEL GRAFO")
    print(f"{'='*70}")
    print(f"Número de emergencias: {len(emergencias)}")
    
    # Filtrar solo nodos internos con buena conectividad
    print(f"Filtrando nodos internos...")
    nodos_internos = filtrar_nodos_internos(grafo, min_salidas=3, min_entradas=3)
    
    print(f"  - Nodos totales en grafo: {len(grafo.nodes())}")
    print(f"  - Nodos internos (bien conectados): {len(nodos_internos)}")
    print(f"  - Porcentaje interno: {len(nodos_internos)/len(grafo.nodes())*100:.1f}%")
    
    # Verificar que haya suficientes nodos internos
    if len(nodos_internos) < len(emergencias):
        print(f"  ⚠️  ADVERTENCIA: Pocos nodos internos ({len(nodos_internos)} < {len(emergencias)})")
        print(f"  Usando todos los nodos disponibles...")
        nodos_a_usar = list(grafo.nodes())
    else:
        nodos_a_usar = nodos_internos
        print(f"  ✅ Suficientes nodos internos disponibles")
    
    # Seleccionar nodos aleatorios de los nodos internos
    nodos_seleccionados = random.sample(nodos_a_usar, len(emergencias))
    
    # Asignar nodos a cada emergencia
    emergencias_con_nodos = []
    for i, (emergencia, nodo) in enumerate(zip(emergencias, nodos_seleccionados)):
        nodo_data = grafo.nodes[nodo]
        
        emergencia_completa = emergencia.copy()
        emergencia_completa['nodo_destino'] = nodo
        emergencia_completa['latitud'] = nodo_data['y']
        emergencia_completa['longitud'] = nodo_data['x']
        
        emergencias_con_nodos.append(emergencia_completa)
        
        print(f"  Emergencia #{emergencia['id']}:")
        print(f"    - Severidad: {emergencia['severidad']:8s}")
        print(f"    - Velocidad requerida: {emergencia['velocidad_requerida']:.2f} km/h")
        print(f"    - Ambulancia: #{emergencia['ambulancia_id']}")
        print(f"    - Nodo destino: {nodo}")
        print(f"    - Coordenadas: ({nodo_data['y']:.6f}, {nodo_data['x']:.6f})")
    
    print(f"{'='*70}\n")
    
    return emergencias_con_nodos


def preparar_grafo_para_optimizacion(grafo, centro_lat, centro_lon, 
                                     emergencias, c_min=30, c_max=100, seed=None):
    """
    Prepara el grafo completo para la optimización:
    1. Asigna capacidades aleatorias a las vías
    2. Calcula tiempos de viaje
    3. Identifica nodo de origen (clínica)
    4. Asigna emergencias a nodos del grafo
    
    Args:
        grafo: NetworkX MultiDiGraph
        centro_lat, centro_lon: Coordenadas del centro (clínica)
        emergencias: Lista de diccionarios con info de emergencias (de parametros.py)
        c_min, c_max: Rango de capacidades de vías
        seed: Semilla para reproducibilidad
    
    Returns:
        tuple: (grafo_procesado, nodo_origen, emergencias_con_nodos)
    """
    print(f"\n{'#'*70}")
    print(f"# PREPARANDO GRAFO PARA OPTIMIZACIÓN")
    print(f"{'#'*70}\n")
    
    # 1. Asignar capacidades aleatorias a las vías
    grafo = asignar_capacidades_aleatorias(grafo, c_min, c_max, seed)
    
    # 2. Calcular tiempos de viaje
    grafo = calcular_tiempos_viaje(grafo)
    
    # 3. Identificar nodo de origen (clínica)
    nodo_origen = encontrar_nodo_origen(grafo, centro_lat, centro_lon)
    
    # 4. Asignar emergencias a nodos del grafo
    emergencias_con_nodos = asignar_emergencias_a_nodos(grafo, emergencias, seed)
    
    # 5. Marcar nodos especiales en el grafo
    nodos_destino = [e['nodo_destino'] for e in emergencias_con_nodos]
    
    for nodo in grafo.nodes():
        grafo.nodes[nodo]['is_origin'] = (nodo == nodo_origen)
        grafo.nodes[nodo]['is_destination'] = (nodo in nodos_destino)
    
    print(f"\n{'='*70}")
    print(f"✓ GRAFO PREPARADO EXITOSAMENTE")
    print(f"{'='*70}")
    print(f"  - Nodo de origen: {nodo_origen}")
    print(f"  - Nodos de destino: {len(nodos_destino)}")
    print(f"  - Emergencias asignadas: {len(emergencias_con_nodos)}")
    print(f"  - Aristas con capacidades: {len(grafo.edges())}")
    print(f"{'='*70}\n")
    
    return grafo, nodo_origen, emergencias_con_nodos


def convertir_grafo_a_geodataframes(grafo):
    """
    Convierte el grafo de NetworkX a GeoDataFrames de nodos y aristas.
    
    Args:
        grafo: NetworkX MultiDiGraph
    
    Returns:
        tuple: (gdf_nodos, gdf_aristas)
    """
    print(f"\n{'='*70}")
    print(f"CONVIRTIENDO GRAFO A GEODATAFRAMES")
    print(f"{'='*70}")
    
    # Convertir a GeoDataFrames usando OSMnx
    gdf_nodos, gdf_aristas = ox.graph_to_gdfs(grafo, nodes=True, edges=True)
    
    print(f"✓ Conversión exitosa")
    print(f"  - GeoDataFrame de nodos: {len(gdf_nodos)} nodos")
    print(f"    Columnas: {list(gdf_nodos.columns)[:10]}...")
    print(f"  - GeoDataFrame de aristas: {len(gdf_aristas)} aristas")
    print(f"    Columnas: {list(gdf_aristas.columns)[:10]}...")
    
    # Verificar CRS
    print(f"  - CRS Nodos: {gdf_nodos.crs}")
    print(f"  - CRS Aristas: {gdf_aristas.crs}")
    print(f"{'='*70}\n")
    
    return gdf_nodos, gdf_aristas


def obtener_estadisticas_grafo(grafo):
    """
    Genera estadísticas descriptivas del grafo procesado.
    
    Args:
        grafo: NetworkX MultiDiGraph
    
    Returns:
        dict: Diccionario con estadísticas
    """
    print(f"\n{'='*70}")
    print(f"ESTADÍSTICAS DEL GRAFO")
    print(f"{'='*70}")
    
    stats = {
        'num_nodos': len(grafo.nodes()),
        'num_aristas': len(grafo.edges()),
    }
    
    # Estadísticas de capacidades
    capacidades = [data['capacity'] for u, v, key, data in grafo.edges(keys=True, data=True) 
                   if 'capacity' in data]
    if capacidades:
        stats['capacidad_min'] = min(capacidades)
        stats['capacidad_max'] = max(capacidades)
        stats['capacidad_promedio'] = np.mean(capacidades)
        stats['capacidad_std'] = np.std(capacidades)
    
    # Estadísticas de tiempos
    tiempos = [data['travel_time'] for u, v, key, data in grafo.edges(keys=True, data=True) 
               if 'travel_time' in data]
    if tiempos:
        stats['tiempo_min'] = min(tiempos)
        stats['tiempo_max'] = max(tiempos)
        stats['tiempo_promedio'] = np.mean(tiempos)
        stats['tiempo_total'] = sum(tiempos)
    
    # Estadísticas de longitudes
    longitudes = [data['length'] for u, v, key, data in grafo.edges(keys=True, data=True) 
                  if 'length' in data]
    if longitudes:
        stats['longitud_total_km'] = sum(longitudes) / 1000
        stats['longitud_promedio_m'] = np.mean(longitudes)
    
    # Nodos especiales
    nodos_origen = [n for n, d in grafo.nodes(data=True) if d.get('is_origin', False)]
    nodos_destino = [n for n, d in grafo.nodes(data=True) if d.get('is_destination', False)]
    
    stats['num_nodos_origen'] = len(nodos_origen)
    stats['num_nodos_destino'] = len(nodos_destino)
    
    # Imprimir estadísticas
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key:30s}: {value:.2f}")
        else:
            print(f"  {key:30s}: {value}")
    
    print(f"{'='*70}\n")
    
    return stats


def guardar_geodataframes(gdf_nodos, gdf_aristas, nombre_base="medellin_poblado"):
    """
    Guarda los GeoDataFrames en archivos.
    
    Args:
        gdf_nodos: GeoDataFrame de nodos
        gdf_aristas: GeoDataFrame de aristas
        nombre_base (str): Nombre base para los archivos
    
    Returns:
        dict: Diccionarios con las rutas de los archivos guardados
    """
    from pathlib import Path
    
    # Directorio de salida
    output_dir = BASE_DIR / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    archivos = {}
    
    try:
        # Guardar nodos
        ruta_nodos = output_dir / f"{nombre_base}_nodos.geojson"
        gdf_nodos.to_file(ruta_nodos, driver='GeoJSON')
        archivos['nodos'] = ruta_nodos
        print(f"✓ Nodos guardados en: {ruta_nodos}")
        
        # Guardar aristas
        ruta_aristas = output_dir / f"{nombre_base}_aristas.geojson"
        gdf_aristas.to_file(ruta_aristas, driver='GeoJSON')
        archivos['aristas'] = ruta_aristas
        print(f"✓ Aristas guardadas en: {ruta_aristas}")
        
        # También guardar en formato pickle para acceso rápido
        ruta_nodos_pkl = output_dir / f"{nombre_base}_nodos.pkl"
        gdf_nodos.to_pickle(ruta_nodos_pkl)
        archivos['nodos_pkl'] = ruta_nodos_pkl
        
        ruta_aristas_pkl = output_dir / f"{nombre_base}_aristas.pkl"
        gdf_aristas.to_pickle(ruta_aristas_pkl)
        archivos['aristas_pkl'] = ruta_aristas_pkl
        
        print(f"✓ GeoDataFrames también guardados en formato Pickle")
        
    except Exception as e:
        print(f"✗ Error al guardar GeoDataFrames: {e}")
    
    return archivos


if __name__ == "__main__":
    from config.parametros import (
        CENTRO_LATITUD, CENTRO_LONGITUD, 
        C_MIN, C_MAX, 
        RANDOM_SEED,
        set_random_seed,
        generar_conjunto_emergencias
    )
    from src.data.osm_loader import cargar_o_descargar_grafo, GRAFO_PARAMS
    
    print(f"\n{'#'*70}")
    print(f"# PROCESAMIENTO COMPLETO DEL GRAFO")
    print(f"{'#'*70}\n")
    
    # 0. Configurar semilla para reproducibilidad
    set_random_seed(RANDOM_SEED)
    
    # 1. Cargar el grafo
    print("1️⃣  CARGANDO GRAFO...")
    grafo = cargar_o_descargar_grafo(**GRAFO_PARAMS, use_cache=True)
    
    # 2. Generar emergencias con sus características
    print("\n2️⃣  GENERANDO EMERGENCIAS...")
    emergencias = generar_conjunto_emergencias()  # Genera entre 3-5 emergencias aleatorias
    print(f"✓ {len(emergencias)} emergencias generadas con severidades y velocidades")
    
    # 3. Preparar grafo para optimización
    print("\n3️⃣  PROCESANDO GRAFO...")
    grafo, nodo_origen, emergencias_con_nodos = preparar_grafo_para_optimizacion(
        grafo=grafo,
        centro_lat=CENTRO_LATITUD,
        centro_lon=CENTRO_LONGITUD,
        emergencias=emergencias,
        c_min=C_MIN,
        c_max=C_MAX,
        seed=RANDOM_SEED
    )
    
    # 4. Convertir a GeoDataFrames
    print("\n4️⃣  CONVIRTIENDO A GEODATAFRAMES...")
    gdf_nodos, gdf_aristas = convertir_grafo_a_geodataframes(grafo)
    
    # 5. Obtener estadísticas
    print("\n5️⃣  GENERANDO ESTADÍSTICAS...")
    stats = obtener_estadisticas_grafo(grafo)
    
    # 6. Guardar GeoDataFrames
    print(f"\n6️⃣  GUARDANDO GEODATAFRAMES...")
    archivos = guardar_geodataframes(gdf_nodos, gdf_aristas)
    
    print(f"\n{'#'*70}")
    print(f"# ✓ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
    print(f"{'#'*70}")
    print(f"\nRESUMEN:")
    print(f"  - Grafo procesado con {len(grafo.nodes())} nodos y {len(grafo.edges())} aristas")
    print(f"  - Nodo de origen (Clínica): {nodo_origen}")
    print(f"  - Número de emergencias: {len(emergencias_con_nodos)}")
    print(f"\n  EMERGENCIAS ASIGNADAS:")
    for emerg in emergencias_con_nodos:
        print(f"    #{emerg['id']} - {emerg['severidad']:8s} - Nodo {emerg['nodo_destino']} - Ambulancia #{emerg['ambulancia_id']}")
    print(f"\n  - GeoDataFrames guardados en: data/processed/")
    print(f"{'#'*70}\n")
