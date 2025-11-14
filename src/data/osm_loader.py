# src/data/osm_loader.py
# Carga de mapas usando OSMnx

"""
PROPÓSITO:
-----------
Encargado de descargar y cargar el grafo de calles de Medellín usando OSMnx.
Implementa sistema de caché para evitar descargas repetidas.
"""

import osmnx as ox
import networkx as nx
import os
import pickle
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = BASE_DIR / "data" / "graphs"
CACHE_FILE = CACHE_DIR / "medellin_poblado_graph.graphml"
CACHE_FILE_PICKLE = CACHE_DIR / "medellin_poblado_graph.pkl"

# Crear directorio de caché si no existe
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de OSMnx
ox.settings.log_console = True
ox.settings.use_cache = True


def descargar_grafo_desde_punto(center_point, dist, network_type='drive', simplify=True):
    """
    Descarga un grafo desde OSM usando un punto central y un radio.
    
    Args:
        center_point (tuple): (latitud, longitud) del centro
        dist (float): Distancia en metros desde el centro
        network_type (str): Tipo de red ('drive', 'walk', 'bike', 'all')
        simplify (bool): Simplificar el grafo
    
    Returns:
        networkx.MultiDiGraph: Grafo de la red vial
    """
    print(f"\n{'='*70}")
    print(f"DESCARGANDO GRAFO DESDE OSM")
    print(f"{'='*70}")
    print(f"Centro: {center_point}")
    print(f"Radio: {dist} metros")
    print(f"Tipo de red: {network_type}")
    print(f"Simplificar: {simplify}")
    print(f"{'='*70}\n")
    
    try:
        # Descargar el grafo
        grafo = ox.graph_from_point(
            center_point,
            dist=dist,
            network_type=network_type,
            simplify=simplify
        )
        
        print(f"✓ Grafo descargado exitosamente")
        print(f"  - Nodos: {len(grafo.nodes())}")
        print(f"  - Aristas: {len(grafo.edges())}")
        
        return grafo
        
    except Exception as e:
        print(f"✗ Error al descargar el grafo: {e}")
        raise


def descargar_grafo(lugar, network_type='drive', simplify=True):
    """
    Descarga un grafo desde OSM usando el nombre de un lugar.
    
    Args:
        lugar (str): Nombre del lugar (ej: "Medellín, Colombia")
        network_type (str): Tipo de red ('drive', 'walk', 'bike', 'all')
        simplify (bool): Simplificar el grafo
    
    Returns:
        networkx.MultiDiGraph: Grafo de la red vial
    """
    print(f"\n{'='*70}")
    print(f"DESCARGANDO GRAFO DESDE OSM")
    print(f"{'='*70}")
    print(f"Lugar: {lugar}")
    print(f"Tipo de red: {network_type}")
    print(f"{'='*70}\n")
    
    try:
        grafo = ox.graph_from_place(
            lugar,
            network_type=network_type,
            simplify=simplify
        )
        
        print(f"✓ Grafo descargado exitosamente")
        print(f"  - Nodos: {len(grafo.nodes())}")
        print(f"  - Aristas: {len(grafo.edges())}")
        
        return grafo
        
    except Exception as e:
        print(f"✗ Error al descargar el grafo: {e}")
        raise


def guardar_grafo(grafo, nombre_archivo=None, formato='both'):
    """
    Guarda el grafo en disco.
    
    Args:
        grafo: Grafo de NetworkX
        nombre_archivo (str, optional): Nombre del archivo (sin extensión)
        formato (str): 'graphml', 'pickle' o 'both'
    
    Returns:
        list: Rutas de los archivos guardados
    """
    if nombre_archivo is None:
        nombre_archivo = "medellin_poblado_graph"
    
    archivos_guardados = []
    
    try:
        if formato in ['graphml', 'both']:
            ruta_graphml = CACHE_DIR / f"{nombre_archivo}.graphml"
            ox.save_graphml(grafo, filepath=ruta_graphml)
            archivos_guardados.append(ruta_graphml)
            print(f"✓ Grafo guardado en: {ruta_graphml}")
        
        if formato in ['pickle', 'both']:
            ruta_pickle = CACHE_DIR / f"{nombre_archivo}.pkl"
            with open(ruta_pickle, 'wb') as f:
                pickle.dump(grafo, f, protocol=pickle.HIGHEST_PROTOCOL)
            archivos_guardados.append(ruta_pickle)
            print(f"✓ Grafo guardado en: {ruta_pickle}")
        
        return archivos_guardados
        
    except Exception as e:
        print(f"✗ Error al guardar el grafo: {e}")
        raise


def cargar_grafo_desde_archivo(nombre_archivo=None, formato='graphml'):
    """
    Carga un grafo previamente guardado.
    
    Args:
        nombre_archivo (str, optional): Nombre del archivo
        formato (str): 'graphml' o 'pickle'
    
    Returns:
        networkx.MultiDiGraph: Grafo cargado o None si no existe
    """
    if nombre_archivo is None:
        nombre_archivo = "medellin_poblado_graph"
    
    try:
        if formato == 'graphml':
            ruta = CACHE_DIR / f"{nombre_archivo}.graphml"
            if ruta.exists():
                print(f"Cargando grafo desde: {ruta}")
                grafo = ox.load_graphml(filepath=ruta)
                print(f"✓ Grafo cargado exitosamente")
                print(f"  - Nodos: {len(grafo.nodes())}")
                print(f"  - Aristas: {len(grafo.edges())}")
                return grafo
        
        elif formato == 'pickle':
            ruta = CACHE_DIR / f"{nombre_archivo}.pkl"
            if ruta.exists():
                print(f"Cargando grafo desde: {ruta}")
                with open(ruta, 'rb') as f:
                    grafo = pickle.load(f)
                print(f"✓ Grafo cargado exitosamente")
                print(f"  - Nodos: {len(grafo.nodes())}")
                print(f"  - Aristas: {len(grafo.edges())}")
                return grafo
        
        print(f"⚠ No se encontró el archivo: {nombre_archivo}.{formato}")
        return None
        
    except Exception as e:
        print(f"✗ Error al cargar el grafo: {e}")
        return None


def cargar_o_descargar_grafo(center_point, dist, network_type='drive', 
                              simplify=True, use_cache=True, force_download=False):
    """
    Carga el grafo desde caché o lo descarga si no existe.
    
    Args:
        center_point (tuple): (latitud, longitud) del centro
        dist (float): Distancia en metros desde el centro
        network_type (str): Tipo de red
        simplify (bool): Simplificar el grafo
        use_cache (bool): Usar caché si está disponible
        force_download (bool): Forzar descarga incluso si existe caché
    
    Returns:
        networkx.MultiDiGraph: Grafo de la red vial
    """
    grafo = None
    
    # Intentar cargar desde caché
    if use_cache and not force_download:
        print("\n🔍 Buscando grafo en caché...")
        grafo = cargar_grafo_desde_archivo(formato='pickle')
        
        if grafo is None:
            grafo = cargar_grafo_desde_archivo(formato='graphml')
    
    # Descargar si no existe en caché
    if grafo is None or force_download:
        if force_download:
            print("\n⬇️  Forzando descarga desde OSM...")
        else:
            print("\n⬇️  Caché no encontrado. Descargando desde OSM...")
        
        grafo = descargar_grafo_desde_punto(
            center_point=center_point,
            dist=dist,
            network_type=network_type,
            simplify=simplify
        )
        
    # Guardar en caché
        print("\n💾 Guardando grafo en caché...")
        guardar_grafo(grafo, formato='both')
    
    # Validar grafo
    validar_grafo(grafo)
    
    return grafo


def validar_grafo(grafo):
    """
    Valida que el grafo tenga la estructura esperada.
    
    Args:
        grafo: Grafo de NetworkX
    
    Returns:
        bool: True si es válido, False en caso contrario
    """
    print(f"\n{'='*70}")
    print(f"VALIDANDO GRAFO")
    print(f"{'='*70}")
    
    # Verificar que no esté vacío
    if len(grafo.nodes()) == 0:
        print("✗ El grafo está vacío (sin nodos)")
        return False
    
    if len(grafo.edges()) == 0:
        print("✗ El grafo no tiene aristas")
        return False
    
    print(f"✓ Nodos: {len(grafo.nodes())}")
    print(f"✓ Aristas: {len(grafo.edges())}")
    
    # Verificar conectividad
    if nx.is_strongly_connected(grafo):
        print(f"✓ El grafo es fuertemente conexo")
    else:
        componentes = list(nx.strongly_connected_components(grafo))
        print(f"⚠ El grafo tiene {len(componentes)} componentes fuertemente conexos")
        print(f"  Componente principal: {len(componentes[0])} nodos")
    
    # Verificar atributos de aristas
    arista_ejemplo = list(grafo.edges(data=True))[0]
    atributos = arista_ejemplo[2].keys()
    print(f"✓ Atributos de aristas: {list(atributos)[:10]}...")
    
    # Verificar atributos importantes
    tiene_length = 'length' in atributos
    tiene_geometry = 'geometry' in atributos
    
    if tiene_length:
        print(f"✓ Las aristas tienen atributo 'length'")
    else:
        print(f"⚠ Las aristas NO tienen atributo 'length'")
    
    if tiene_geometry:
        print(f"✓ Las aristas tienen atributo 'geometry'")
    else:
        print(f"⚠ Las aristas NO tienen atributo 'geometry'")
    
    # Estadísticas básicas
    longitudes = [data['length'] for u, v, data in grafo.edges(data=True) if 'length' in data]
    if longitudes:
        print(f"\n📊 Estadísticas de longitudes de aristas:")
        print(f"   - Mínima: {min(longitudes):.2f} m")
        print(f"   - Máxima: {max(longitudes):.2f} m")
        print(f"   - Promedio: {sum(longitudes)/len(longitudes):.2f} m")
    
    print(f"{'='*70}\n")
    
    return True


def obtener_info_grafo(grafo):
    """
    Obtiene información detallada del grafo.
    
    Args:
        grafo: Grafo de NetworkX
    
    Returns:
        dict: Diccionario con información del grafo
    """
    info = {
        'num_nodos': len(grafo.nodes()),
        'num_aristas': len(grafo.edges()),
        'es_dirigido': grafo.is_directed(),
        'es_multigrafo': grafo.is_multigraph(),
    }
    
    # Conectividad
    if nx.is_strongly_connected(grafo):
        info['es_conexo'] = True
        info['num_componentes'] = 1
    else:
        info['es_conexo'] = False
        componentes = list(nx.strongly_connected_components(grafo))
        info['num_componentes'] = len(componentes)
        info['tamano_componente_principal'] = len(componentes[0])
    
    # Estadísticas de grados
    grados_out = [d for n, d in grafo.out_degree()]
    grados_in = [d for n, d in grafo.in_degree()]
    
    info['grado_out_promedio'] = sum(grados_out) / len(grados_out)
    info['grado_in_promedio'] = sum(grados_in) / len(grados_in)
    
    # Estadísticas de longitudes
    longitudes = [data['length'] for u, v, data in grafo.edges(data=True) if 'length' in data]
    if longitudes:
        info['longitud_min'] = min(longitudes)
        info['longitud_max'] = max(longitudes)
        info['longitud_promedio'] = sum(longitudes) / len(longitudes)
        info['longitud_total'] = sum(longitudes)
    
    return info


if __name__ == "__main__":
    # Importar parámetros
    import sys
    sys.path.append(str(BASE_DIR))
    from config.parametros import GRAFO_PARAMS, CIUDAD, CENTRO_LATITUD, CENTRO_LONGITUD
    
    print(f"\n{'#'*70}")
    print(f"# DESCARGA DE RED VIAL - {CIUDAD}")
    print(f"{'#'*70}\n")
    
    # Cargar o descargar el grafo
    grafo = cargar_o_descargar_grafo(
        center_point=GRAFO_PARAMS['center_point'],
        dist=GRAFO_PARAMS['dist'],
        network_type=GRAFO_PARAMS['network_type'],
        simplify=GRAFO_PARAMS['simplify'],
        use_cache=True,
        force_download=False  # Cambiar a True para forzar descarga
    )
    
    # Mostrar información
    print(f"\n{'='*70}")
    print(f"INFORMACIÓN DEL GRAFO")
    print(f"{'='*70}")
    
    info = obtener_info_grafo(grafo)
    for clave, valor in info.items():
        print(f"{clave:30s}: {valor}")
    
    print(f"\n{'='*70}")
    print(f"✓ Red descargada y guardada exitosamente")
    print(f"{'='*70}\n")
