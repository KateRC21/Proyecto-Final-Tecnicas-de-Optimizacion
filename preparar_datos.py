"""
Script principal para preparar todos los datos necesarios para la optimización.
Ejecuta todo el pipeline: descarga OSM → procesa grafo → genera emergencias → convierte a GeoDataFrames

Ejecutar desde la raíz del proyecto: python preparar_datos.py
"""

import sys
from pathlib import Path
import pickle

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar todos los módulos necesarios
from src.data.osm_loader import cargar_o_descargar_grafo
from src.data.graph_processor import (
    preparar_grafo_para_optimizacion,
    convertir_grafo_a_geodataframes,
    obtener_estadisticas_grafo,
    guardar_geodataframes
)
from config.parametros import (
    GRAFO_PARAMS,
    CENTRO_LATITUD, CENTRO_LONGITUD,
    C_MIN, C_MAX,
    RANDOM_SEED,
    set_random_seed,
    generar_conjunto_emergencias,
    CIUDAD
)

def guardar_datos_modelo(grafo, nodo_origen, emergencias, nombre_archivo="datos_modelo"):
    """
    Guarda todos los datos necesarios para el modelo de optimización.
    
    Args:
        grafo: Grafo procesado
        nodo_origen: ID del nodo de origen
        emergencias: Lista de emergencias con nodos
        nombre_archivo: Nombre base para los archivos
    """
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    datos_modelo = {
        'grafo': grafo,
        'nodo_origen': nodo_origen,
        'emergencias': emergencias,
        'parametros': {
            'centro_lat': CENTRO_LATITUD,
            'centro_lon': CENTRO_LONGITUD,
            'c_min': C_MIN,
            'c_max': C_MAX,
            'random_seed': RANDOM_SEED
        }
    }
    
    # Guardar en pickle
    ruta_pkl = output_dir / f"{nombre_archivo}.pkl"
    with open(ruta_pkl, 'wb') as f:
        pickle.dump(datos_modelo, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"\n💾 Datos del modelo guardados en: {ruta_pkl}")
    
    return ruta_pkl

def main(force_download=False):
    """
    Ejecuta el pipeline completo de preparación de datos.
    
    Args:
        force_download (bool): Si True, fuerza descarga desde OSM aunque exista caché
    """
    print(f"\n{'#'*70}")
    print(f"# PREPARACIÓN COMPLETA DE DATOS - {CIUDAD}")
    print(f"{'#'*70}\n")
    
    try:
        # ====================================================================
        # PASO 1: CONFIGURACIÓN INICIAL
        # ====================================================================
        print("\n" + "="*70)
        print("PASO 1: CONFIGURACIÓN INICIAL")
        print("="*70)
        
        set_random_seed(RANDOM_SEED)
        print(f"✓ Semilla aleatoria configurada: {RANDOM_SEED}")
        print(f"✓ Ciudad: {CIUDAD}")
        print(f"✓ Centro: ({CENTRO_LATITUD}, {CENTRO_LONGITUD})")
        print(f"✓ Área: 1km x 1km")
        print(f"✓ Rango de capacidades: [{C_MIN}, {C_MAX}] km/h")
        
        # ====================================================================
        # PASO 2: DESCARGA/CARGA DEL GRAFO
        # ====================================================================
        print("\n" + "="*70)
        print("PASO 2: DESCARGA/CARGA DEL GRAFO")
        print("="*70)
        
        grafo = cargar_o_descargar_grafo(
            **GRAFO_PARAMS, 
            use_cache=True, 
            force_download=force_download
        )
        print(f"✓ Grafo cargado: {len(grafo.nodes())} nodos, {len(grafo.edges())} aristas")
        
        # ====================================================================
        # PASO 3: GENERACIÓN DE EMERGENCIAS
        # ====================================================================
        print("\n" + "="*70)
        print("PASO 3: GENERACIÓN DE EMERGENCIAS")
        print("="*70)
        
        emergencias = generar_conjunto_emergencias()
        print(f"✓ {len(emergencias)} emergencias generadas:")
        for e in emergencias:
            print(f"   #{e['id']}: {e['severidad']:8s} | "
                  f"Vel: {e['velocidad_requerida']:5.2f} km/h | "
                  f"Ambulancia: #{e['ambulancia_id']}")
        
        # ====================================================================
        # PASO 4: PROCESAMIENTO DEL GRAFO
        # ====================================================================
        print("\n" + "="*70)
        print("PASO 4: PROCESAMIENTO DEL GRAFO")
        print("="*70)
        
        grafo, nodo_origen, emergencias_con_nodos = preparar_grafo_para_optimizacion(
            grafo=grafo,
            centro_lat=CENTRO_LATITUD,
            centro_lon=CENTRO_LONGITUD,
            emergencias=emergencias,
            c_min=C_MIN,
            c_max=C_MAX,
            seed=RANDOM_SEED
        )
        
        # ====================================================================
        # PASO 5: CONVERSIÓN A GEODATAFRAMES
        # ====================================================================
        print("\n" + "="*70)
        print("PASO 5: CONVERSIÓN A GEODATAFRAMES")
        print("="*70)
        
        gdf_nodos, gdf_aristas = convertir_grafo_a_geodataframes(grafo)
        
        # ====================================================================
        # PASO 6: ESTADÍSTICAS
        # ====================================================================
        print("\n" + "="*70)
        print("PASO 6: ESTADÍSTICAS DEL GRAFO")
        print("="*70)
        
        stats = obtener_estadisticas_grafo(grafo)
        
        # ====================================================================
        # PASO 7: GUARDAR DATOS
        # ====================================================================
        print("\n" + "="*70)
        print("PASO 7: GUARDANDO DATOS")
        print("="*70)
        
        # Guardar GeoDataFrames
        archivos_geo = guardar_geodataframes(gdf_nodos, gdf_aristas)
        
        # Guardar datos del modelo
        archivo_modelo = guardar_datos_modelo(grafo, nodo_origen, emergencias_con_nodos)
        
        # ====================================================================
        # RESUMEN FINAL
        # ====================================================================
        print(f"\n{'#'*70}")
        print(f"# ✓✓✓ PREPARACIÓN COMPLETADA EXITOSAMENTE ✓✓✓")
        print(f"{'#'*70}")
        
        print(f"\n📊 RESUMEN GENERAL:")
        print(f"   {'='*66}")
        print(f"   {'Parámetro':<30} {'Valor':<35}")
        print(f"   {'='*66}")
        print(f"   {'Ciudad':<30} {CIUDAD:<35}")
        print(f"   {'Nodos totales':<30} {len(grafo.nodes()):<35}")
        print(f"   {'Aristas totales':<30} {len(grafo.edges()):<35}")
        print(f"   {'Nodo origen':<30} {nodo_origen:<35}")
        print(f"   {'Número de emergencias':<30} {len(emergencias_con_nodos):<35}")
        print(f"   {'Capacidad vías (promedio)':<30} {stats.get('capacidad_promedio', 0):.2f} km/h")
        print(f"   {'Tiempo viaje (promedio)':<30} {stats.get('tiempo_promedio', 0):.3f} min")
        print(f"   {'Longitud total red':<30} {stats.get('longitud_total_km', 0):.2f} km")
        print(f"   {'='*66}")
        
        print(f"\n🚑 EMERGENCIAS:")
        print(f"   {'ID':<5} {'Severidad':<10} {'Vel.Req':<10} {'Nodo':<15} {'Ambulancia':<12}")
        print(f"   {'-'*66}")
        for e in emergencias_con_nodos:
            print(f"   #{e['id']:<4} {e['severidad']:<10} "
                  f"{e['velocidad_requerida']:5.2f} km/h  "
                  f"{str(e['nodo_destino']):<15} #{e['ambulancia_id']:<11}")
        
        print(f"\n💾 ARCHIVOS GENERADOS:")
        print(f"   Directorio: data/processed/")
        print(f"   {'-'*66}")
        for nombre, ruta in archivos_geo.items():
            print(f"   - {nombre}: {Path(ruta).name}")
        print(f"   - Datos modelo: {Path(archivo_modelo).name}")
        
        print(f"\n🚀 SIGUIENTE PASO:")
        print(f"   Los datos están listos para el modelo de optimización")
        print(f"   Puedes cargar los datos usando:")
        print(f"   >>> import pickle")
        print(f"   >>> with open('data/processed/datos_modelo.pkl', 'rb') as f:")
        print(f"   >>>     datos = pickle.load(f)")
        
        print(f"\n{'#'*70}\n")
        
        return {
            'grafo': grafo,
            'nodo_origen': nodo_origen,
            'emergencias': emergencias_con_nodos,
            'gdf_nodos': gdf_nodos,
            'gdf_aristas': gdf_aristas,
            'stats': stats
        }
        
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"✗ ERROR EN LA PREPARACIÓN DE DATOS")
        print(f"{'='*70}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'='*70}\n")
        raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Preparar datos para optimización')
    parser.add_argument('--force-download', action='store_true',
                       help='Forzar descarga desde OSM (ignora caché)')
    
    args = parser.parse_args()
    
    datos = main(force_download=args.force_download)

