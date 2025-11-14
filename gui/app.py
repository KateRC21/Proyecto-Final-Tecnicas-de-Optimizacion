# gui/app.py
# Aplicación principal de Streamlit

"""
Sistema de Visualización de Datos de Optimización de Rutas de Ambulancias
Medellín, Colombia
"""

import streamlit as st
import pickle
import sys
from pathlib import Path
import geopandas as gpd

# Agregar paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Imports del proyecto
from config.parametros import CIUDAD, CENTRO_LATITUD, CENTRO_LONGITUD

# Imports de componentes
from gui.components.sidebar import crear_sidebar
from gui.components.map_display import (
    crear_mapa_base,
    agregar_grafo_al_mapa,
    agregar_nodos_al_mapa,
    agregar_origen_al_mapa,
    agregar_emergencias_al_mapa,
    mostrar_mapa_streamlit,
    mostrar_leyenda_mapa
)
from gui.components.results_panel import (
    mostrar_metricas_generales,
    mostrar_estadisticas_capacidades,
    mostrar_estadisticas_tiempos,
    mostrar_tabla_aristas,
    mostrar_resumen_emergencias,
    mostrar_tabla_emergencias,
    graficar_emergencias_por_severidad
)

# Configuración de la página
st.set_page_config(
    page_title="Optimización de Ambulancias - Medellín",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #E74C3C;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================

@st.cache_data
def cargar_datos_modelo():
    """Carga los datos procesados del modelo"""
    ruta = BASE_DIR / "data" / "processed" / "datos_modelo.pkl"
    if ruta.exists():
        with open(ruta, 'rb') as f:
            return pickle.load(f)
    return None


@st.cache_data
def cargar_geodataframes():
    """Carga los GeoDataFrames de nodos y aristas"""
    try:
        import pandas as pd
        
        ruta_nodos = BASE_DIR / "data" / "processed" / "medellin_poblado_nodos.pkl"
        ruta_aristas = BASE_DIR / "data" / "processed" / "medellin_poblado_aristas.pkl"
        
        if not ruta_nodos.exists() or not ruta_aristas.exists():
            return None, None
        
        # Usar pandas.read_pickle() para cargar GeoDataFrames
        gdf_nodos = pd.read_pickle(ruta_nodos)
        gdf_aristas = pd.read_pickle(ruta_aristas)
        
        return gdf_nodos, gdf_aristas
    except Exception as e:
        st.error(f"Error cargando GeoDataFrames: {e}")
        return None, None


# ============================================================================
# INICIALIZACIÓN DE SESSION STATE
# ============================================================================

def inicializar_session_state():
    """Inicializa las variables de estado de la sesión y carga datos automáticamente"""
    
    # Inicializar flags de control
    if 'inicializado' not in st.session_state:
        st.session_state.inicializado = False
    
    if 'datos_cargados' not in st.session_state:
        st.session_state.datos_cargados = False
    
    if 'datos_modelo' not in st.session_state:
        st.session_state.datos_modelo = None
    
    if 'gdf_nodos' not in st.session_state:
        st.session_state.gdf_nodos = None
    
    if 'gdf_aristas' not in st.session_state:
        st.session_state.gdf_aristas = None
    
    if 'emergencias_generadas' not in st.session_state:
        st.session_state.emergencias_generadas = None
    
    if 'mostrar_capacidades' not in st.session_state:
        st.session_state.mostrar_capacidades = False
    
    if 'mostrar_nodos' not in st.session_state:
        st.session_state.mostrar_nodos = False
    
    # CARGA AUTOMÁTICA DE DATOS AL INICIO (solo una vez)
    if not st.session_state.inicializado:
        with st.spinner('🔄 Cargando datos iniciales...'):
            try:
                # Cargar datos del modelo
                st.session_state.datos_modelo = cargar_datos_modelo()
                
                # Cargar GeoDataFrames
                st.session_state.gdf_nodos, st.session_state.gdf_aristas = cargar_geodataframes()
                
                # Verificar si se cargaron correctamente
                if st.session_state.datos_modelo and st.session_state.gdf_aristas is not None:
                    st.session_state.datos_cargados = True
                    st.session_state.inicializado = True
                else:
                    st.session_state.datos_cargados = False
                    st.error("⚠️ No se encontraron datos procesados. Ejecuta: `python preparar_datos.py`")
            except Exception as e:
                st.error(f"❌ Error al cargar datos: {e}")
                st.session_state.datos_cargados = False


# ============================================================================
# TABS
# ============================================================================

def mostrar_tab_inicio():
    """Tab de inicio con información general"""
    st.header("Bienvenido al Sistema de Optimización")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Información del Proyecto")
        st.info(f"""
        **Ciudad:** {CIUDAD}
        
        **Centro:** Clínica Medellín - Sede El Poblado
        
        **Coordenadas:** ({CENTRO_LATITUD}, {CENTRO_LONGITUD})
        
        **Área de estudio:** 1 km x 1 km (red vehicular)
        """)
        
        st.subheader("✨ Características")
        st.success("""
        ✅ Visualización de red vial real (OSM)
        
        ✅ Generación de emergencias aleatorias
        
        ✅ Asignación de capacidades a vías
        
        ✅ Cálculo de tiempos de viaje
        
        ✅ Mapas interactivos con Folium
        
        ✅ Estadísticas y gráficos detallados
        """)
    
    with col2:
        st.subheader("🚀 Guía Rápida")
        
        if st.session_state.get('datos_cargados', False):
            st.success("""
            ✅ **Datos cargados automáticamente**
            
            La aplicación ya tiene todo listo para usar.
            """)
            
            st.markdown("""
            ### 🗺️ Explorar el Mapa
            Ve al tab **"🗺️ Mapa Interactivo"** para ver:
            - Red vial de Medellín (1km²)
            - Punto de origen (Clínica)
            - Emergencias con colores por severidad
            
            ### 🎲 Generar Nuevas Emergencias
            👈 En el sidebar, click en **"🎲 Generar Nuevas Emergencias"**
            para crear un nuevo escenario aleatorio
            
            ### 📊 Ver Estadísticas
            Explora los tabs:
            - **📊 Datos**: Capacidades, tiempos, gráficos
            - **🚑 Emergencias**: Detalles y descargas
            """)
        else:
            st.error("""
            ❌ **No hay datos disponibles**
            
            Los datos no se encontraron automáticamente.
            """)
            st.markdown("""
            ### Solución:
            Ejecuta en la terminal:
            ```bash
            python preparar_datos.py
            ```
            Luego recarga la aplicación.
            """)
        
        st.subheader("📁 Estado de Archivos")
        archivos_requeridos = [
            ("data/processed/datos_modelo.pkl", "Modelo"),
            ("data/processed/medellin_poblado_nodos.pkl", "Nodos"),
            ("data/processed/medellin_poblado_aristas.pkl", "Aristas")
        ]
        
        for archivo, desc in archivos_requeridos:
            ruta = BASE_DIR / archivo
            if ruta.exists():
                st.success(f"✅ {desc}")
            else:
                st.error(f"❌ {desc}")
        
        if not all((BASE_DIR / archivo).exists() for archivo, _ in archivos_requeridos):
            st.warning("""
            ⚠️ **Faltan datos procesados**
            
            Ejecuta en la terminal:
            ```bash
            python preparar_datos.py
            ```
            """)


def mostrar_tab_mapa():
    """Tab del mapa interactivo"""
    st.header("🗺️ Mapa Interactivo de Medellín")
    
    if not st.session_state.get('datos_cargados', False):
        st.error("❌ **No hay datos disponibles**")
        st.info("Los datos se cargan automáticamente al abrir la aplicación. Si ves este mensaje, ejecuta `python preparar_datos.py` y recarga la página.")
        return
    
    # Crear mapa
    with st.spinner("Generando mapa..."):
        mapa = crear_mapa_base(CENTRO_LATITUD, CENTRO_LONGITUD, zoom=15)
        
        # Agregar grafo
        if st.session_state.gdf_aristas is not None:
            mapa = agregar_grafo_al_mapa(
                mapa, 
                st.session_state.gdf_aristas,
                mostrar_capacidades=st.session_state.mostrar_capacidades
            )
        
        # Agregar nodos si está activado
        if st.session_state.mostrar_nodos and st.session_state.gdf_nodos is not None:
            mapa = agregar_nodos_al_mapa(mapa, st.session_state.gdf_nodos, max_nodos=100)
        
        # Agregar origen
        if st.session_state.datos_modelo:
            nodo_origen = st.session_state.datos_modelo['nodo_origen']
            grafo = st.session_state.datos_modelo['grafo']
            nodo_data = grafo.nodes[nodo_origen]
            mapa = agregar_origen_al_mapa(mapa, nodo_data['y'], nodo_data['x'])
        
        # Agregar emergencias
        emergencias_a_mostrar = st.session_state.emergencias_generadas or \
                                st.session_state.datos_modelo.get('emergencias', [])
        
        if emergencias_a_mostrar:
            mapa = agregar_emergencias_al_mapa(mapa, emergencias_a_mostrar)
        
        # Agregar rutas optimizadas si existen
        if 'resultado_optimizacion' in st.session_state:
            resultado = st.session_state.resultado_optimizacion
            if resultado is not None and resultado.get('estado') == 'Optimal':
                from gui.components.map_display import agregar_rutas_optimizadas_al_mapa
                mapa = agregar_rutas_optimizadas_al_mapa(mapa, grafo, resultado)
    
    # Mostrar mapa
    mostrar_mapa_streamlit(mapa, width=1400, height=700)
    
    # Leyenda
    mostrar_leyenda_mapa()


def mostrar_tab_datos():
    """Tab de datos y estadísticas"""
    st.header("📊 Datos y Estadísticas del Grafo")
    
    if not st.session_state.get('datos_cargados', False):
        st.error("❌ **No hay datos disponibles**")
        st.info("Los datos se cargan automáticamente. Recarga la página si ves este mensaje.")
        return
    
    grafo = st.session_state.datos_modelo['grafo']
    gdf_aristas = st.session_state.gdf_aristas
    
    # Métricas generales
    mostrar_metricas_generales(grafo, gdf_aristas)
    
    st.markdown("---")
    
    # Estadísticas de capacidades
    if gdf_aristas is not None and 'capacity' in gdf_aristas.columns:
        mostrar_estadisticas_capacidades(gdf_aristas)
        st.markdown("---")
    
    # Estadísticas de tiempos
    if gdf_aristas is not None and 'travel_time' in gdf_aristas.columns:
        mostrar_estadisticas_tiempos(gdf_aristas)
        st.markdown("---")
    
    # Tabla de datos
    mostrar_tabla_aristas(gdf_aristas, num_filas=50)


def mostrar_tab_emergencias():
    """Tab de emergencias"""
    st.header("🚑 Emergencias del Sistema")
    
    if not st.session_state.get('datos_cargados', False):
        st.error("❌ **No hay datos disponibles**")
        st.info("Los datos se cargan automáticamente. Recarga la página si ves este mensaje.")
        return
    
    # Priorizar emergencias generadas manualmente, sino usar las del modelo
    emergencias = st.session_state.emergencias_generadas or \
                  st.session_state.datos_modelo.get('emergencias', [])
    
    if not emergencias:
        st.warning("⚠️ No hay emergencias disponibles. Genera nuevas desde el sidebar.")
        return
    
    # Resumen
    mostrar_resumen_emergencias(emergencias)
    
    st.markdown("---")
    
    # Gráfico de distribución
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = graficar_emergencias_por_severidad(emergencias)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Información")
        st.info("""
        **Severidades:**
        
        🟢 **Leve**: 30-50 km/h
        
        🟠 **Media**: 50-70 km/h
        
        🔴 **Grave**: 70-90 km/h
        
        ---
        
        **Relación:** 1 ambulancia por emergencia
        
        **Origen:** Clínica Medellín
        """)
    
    st.markdown("---")
    
    # Tabla detallada
    mostrar_tabla_emergencias(emergencias)


def mostrar_tab_resultados_optimizacion():
    """Tab de resultados de optimización"""
    st.header("🎯 Resultados de la Optimización")
    
    # Verificar si hay resultados
    if 'resultado_optimizacion' not in st.session_state or st.session_state.resultado_optimizacion is None:
        st.info("📢 **¿Cómo usar?**")
        st.markdown("""
        1. Configura los parámetros en el **Panel de Control** (sidebar izquierdo)
        2. Genera emergencias con el botón **"🎲 Generar Nuevas Emergencias"**
        3. Presiona **"🎯 Calcular Rutas"** para ejecutar la optimización
        4. Los resultados aparecerán aquí automáticamente
        """)
        
        st.divider()
        
        st.markdown("### ℹ️ Información del Modelo")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Tipo de modelo:**
            - Multi-Commodity Flow Problem
            - Cada emergencia = un flujo independiente
            - Minimización de costos operacionales
            """)
        
        with col2:
            st.markdown("""
            **Restricciones:**
            - Conservación de flujo en cada nodo
            - Capacidades de vías respetadas
            - Una ambulancia por emergencia
            """)
        
        return
    
    resultado = st.session_state.resultado_optimizacion
    
    # Si no es óptimo, mostrar mensaje de error
    if resultado['estado'] != 'Optimal':
        st.error(f"❌ **Optimización no exitosa: {resultado['estado']}**")
        
        if resultado['estado'] == 'Infeasible':
            st.warning("""
            **No se encontró solución factible.** Esto puede deberse a:
            
            1. **Velocidades requeridas > Capacidades de vías**
               - Las emergencias necesitan más velocidad de la que las calles pueden ofrecer
               - Solución: Aumenta C_MAX o disminuye R_MAX
            
            2. **Cuello de botella**
               - Múltiples ambulancias intentan usar la misma vía con capacidad insuficiente
               - Solución: Ajusta los parámetros o genera menos emergencias
            
            3. **Grafo desconectado**
               - No existe camino desde el origen a algún destino
               - Solución: Regenera las emergencias
            """)
        
        if 'mensaje' in resultado:
            with st.expander("📋 Detalles técnicos"):
                st.text(resultado['mensaje'])
        
        return
    
    # MÉTRICAS PRINCIPALES
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Costo Total", f"${resultado['costo_total']:,.0f}", 
                  delta="COP", delta_color="off")
    
    with col2:
        st.metric("🚑 Ambulancias", len(resultado['rutas']))
    
    with col3:
        dist_total = sum(d['distancia_km'] for d in resultado['detalles'])
        st.metric("📏 Distancia Total", f"{dist_total:.1f} km")
    
    with col4:
        st.metric("⏱️ Tiempo Resolución", f"{resultado['tiempo_resolucion']:.1f}s")
    
    st.markdown("---")
    
    # DETALLES POR EMERGENCIA
    st.subheader("📋 Detalles por Emergencia")
    
    import pandas as pd
    
    df_detalles = pd.DataFrame([
        {
            'ID': d['emergencia_id'],
            'Severidad': d['severidad'].capitalize(),
            'Ambulancia': d['tipo_ambulancia'][:20] + '...' if len(d['tipo_ambulancia']) > 20 else d['tipo_ambulancia'],
            'Vel. Req. (km/h)': f"{d['velocidad_requerida']:.1f}",
            'Distancia (km)': f"{d['distancia_km']:.2f}",
            'Aristas': d['num_aristas'],
            'Costo Fijo': f"${d['costo_fijo']:,.0f}",
            'Costo Variable': f"${d['costo_variable']:,.0f}",
            'Costo Total': f"${d['costo_total']:,.0f}"
        }
        for d in resultado['detalles']
    ])
    
    # Aplicar colores según severidad
    def colorear_severidad(row):
        if row['Severidad'] == 'Leve':
            return ['background-color: #d4edda'] * len(row)
        elif row['Severidad'] == 'Media':
            return ['background-color: #fff3cd'] * len(row)
        elif row['Severidad'] == 'Grave':
            return ['background-color: #f8d7da'] * len(row)
        return [''] * len(row)
    
    st.dataframe(df_detalles, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # GRÁFICOS
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribución de Costos")
        
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Costo Fijo',
            x=[f"E{d['emergencia_id']}" for d in resultado['detalles']],
            y=[d['costo_fijo'] for d in resultado['detalles']],
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            name='Costo Variable',
            x=[f"E{d['emergencia_id']}" for d in resultado['detalles']],
            y=[d['costo_variable'] for d in resultado['detalles']],
            marker_color='darkblue'
        ))
        fig.update_layout(
            barmode='stack',
            xaxis_title='Emergencia',
            yaxis_title='Costo (COP)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📏 Distancias por Emergencia")
        
        fig2 = go.Figure(data=[
            go.Bar(
                x=[f"E{d['emergencia_id']}" for d in resultado['detalles']],
                y=[d['distancia_km'] for d in resultado['detalles']],
                marker_color=['green' if d['severidad'] == 'leve' 
                              else 'orange' if d['severidad'] == 'media' 
                              else 'red' for d in resultado['detalles']],
                text=[f"{d['distancia_km']:.2f}" for d in resultado['detalles']],
                textposition='auto'
            )
        ])
        fig2.update_layout(
            xaxis_title='Emergencia',
            yaxis_title='Distancia (km)',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # USO DE VÍAS
    st.subheader("🚦 Análisis de Uso de Vías")
    
    uso_aristas = resultado['uso_aristas']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Vías Utilizadas", len(uso_aristas))
    
    with col2:
        compartidas = sum(1 for u in uso_aristas.values() if u['num_flujos'] > 1)
        st.metric("Vías Compartidas", compartidas)
    
    with col3:
        if uso_aristas:
            util_promedio = sum(u['utilizacion'] for u in uso_aristas.values()) / len(uso_aristas)
            st.metric("Utilización Promedio", f"{util_promedio*100:.1f}%")
        else:
            st.metric("Utilización Promedio", "N/A")
    
    with col4:
        sobrecargadas = sum(1 for u in uso_aristas.values() if u['utilizacion'] > 1.0)
        color = "normal" if sobrecargadas == 0 else "inverse"
        st.metric("Vías Sobrecargadas", sobrecargadas, 
                  delta="⚠️" if sobrecargadas > 0 else "✓")
    
    # Top vías más utilizadas
    if uso_aristas:
        st.markdown("#### 🔝 Top 10 Vías Más Utilizadas")
        
        top_vias = sorted(
            uso_aristas.items(),
            key=lambda x: x[1]['utilizacion'],
            reverse=True
        )[:10]
        
        df_vias = pd.DataFrame([
            {
                'Vía': f"{i} → {j}",
                'Flujos': info['num_flujos'],
                'Emergencias': ', '.join([f"#{fid}" for fid in info['flujos_ids']]),
                'Carga (km/h)': f"{info['carga_total']:.1f}",
                'Capacidad (km/h)': f"{info['capacidad']:.1f}",
                'Utilización': f"{info['utilizacion']*100:.1f}%",
                'Estado': '🔴 Sobrecargada' if info['utilizacion'] > 1.0 
                         else '🟡 Alta' if info['utilizacion'] > 0.7 
                         else '🟢 Normal'
            }
            for (i, j), info in top_vias
        ])
        
        st.dataframe(df_vias, use_container_width=True, hide_index=True)
        
        if sobrecargadas > 0:
            st.warning(f"⚠️ **Atención:** {sobrecargadas} vía(s) están sobrecargadas (utilización > 100%). "
                      "Esto puede indicar congestión en esas rutas.")
    
    st.markdown("---")
    
    # MÉTRICAS AGREGADAS
    st.subheader("📈 Métricas Agregadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Costos**")
        costo_promedio = resultado['costo_total'] / len(resultado['detalles'])
        st.metric("Costo promedio/emergencia", f"${costo_promedio:,.0f}")
        
        costo_fijo_total = sum(d['costo_fijo'] for d in resultado['detalles'])
        costo_variable_total = sum(d['costo_variable'] for d in resultado['detalles'])
        st.caption(f"Fijo: ${costo_fijo_total:,.0f} ({costo_fijo_total/resultado['costo_total']*100:.1f}%)")
        st.caption(f"Variable: ${costo_variable_total:,.0f} ({costo_variable_total/resultado['costo_total']*100:.1f}%)")
    
    with col2:
        st.markdown("**Distancias**")
        distancia_promedio = dist_total / len(resultado['detalles'])
        st.metric("Distancia promedio", f"{distancia_promedio:.2f} km")
        
        distancia_min = min(d['distancia_km'] for d in resultado['detalles'])
        distancia_max = max(d['distancia_km'] for d in resultado['detalles'])
        st.caption(f"Mínima: {distancia_min:.2f} km")
        st.caption(f"Máxima: {distancia_max:.2f} km")
    
    with col3:
        st.markdown("**Eficiencia**")
        aristas_totales = sum(d['num_aristas'] for d in resultado['detalles'])
        aristas_promedio = aristas_totales / len(resultado['detalles'])
        st.metric("Aristas promedio/ruta", f"{aristas_promedio:.1f}")
        
        st.caption(f"Total aristas usadas: {aristas_totales}")
        st.caption(f"Vías únicas: {len(uso_aristas)}")


# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal de la aplicación"""
    inicializar_session_state()
    
    # Header
    st.markdown('<div class="main-header">🚑 Sistema de Optimización de Rutas de Ambulancias</div>', 
                unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #555;'>📍 {CIUDAD}</h3>", 
                unsafe_allow_html=True)
    
    # Indicador de estado
    if st.session_state.get('datos_cargados', False):
        grafo = st.session_state.datos_modelo['grafo']
        emergencias = st.session_state.datos_modelo.get('emergencias', [])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Estado", "✅ Operativo", delta="Datos cargados")
        with col2:
            st.metric("Nodos", f"{len(grafo.nodes()):,}")
        with col3:
            st.metric("Aristas", f"{len(grafo.edges()):,}")
        with col4:
            st.metric("Emergencias", len(emergencias))
    else:
        st.error("⚠️ **Sistema no operativo** - No se encontraron datos procesados")
    
    st.markdown("---")
    
    # Sidebar
    crear_sidebar()
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Inicio",
        "🗺️ Mapa Interactivo",
        "📊 Datos y Estadísticas",
        "🚑 Emergencias",
        "🎯 Resultados Optimización"
    ])
    
    with tab1:
        mostrar_tab_inicio()
    
    with tab2:
        mostrar_tab_mapa()
    
    with tab3:
        mostrar_tab_datos()
    
    with tab4:
        mostrar_tab_emergencias()
    
    with tab5:
        mostrar_tab_resultados_optimizacion()


if __name__ == "__main__":
    main()
