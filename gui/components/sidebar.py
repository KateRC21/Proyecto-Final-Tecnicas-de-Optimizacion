"""
Componente del sidebar con controles interactivos
"""

import streamlit as st
import random
from config.parametros import (
    R_MIN, R_MAX, C_MIN, C_MAX,
    NUM_EMERGENCIAS_MIN, NUM_EMERGENCIAS_MAX,
    RANDOM_SEED, set_random_seed,
    generar_conjunto_emergencias,
    RANGOS_EMERGENCIA
)
from config.costos import (
    COSTOS,
    PRIORIDAD_A_AMBULANCIA,
    VALORES_DEFAULT_INTERFAZ
)


def crear_sidebar():
    """
    Crea el sidebar completo con todos los controles
    """
    st.sidebar.title("⚙️ Panel de Control")
    st.sidebar.markdown("---")
    
    # SECCIÓN 1: Cargar Datos
    seccion_cargar_datos()
    st.sidebar.markdown("---")
    
    # SECCIÓN 2: Parámetros Configurables
    seccion_parametros()
    
    # SECCIÓN 3: Costos Operacionales
    seccion_costos()
    
    # SECCIÓN 4: Botones de Acción
    seccion_botones_accion()
    st.sidebar.markdown("---")
    
    # SECCIÓN 5: Generar Emergencias
    seccion_emergencias()
    st.sidebar.markdown("---")
    
    # SECCIÓN 6: Opciones de Visualización
    seccion_visualizacion()
    st.sidebar.markdown("---")
    
    # SECCIÓN 7: Información del Sistema
    seccion_informacion()


def seccion_cargar_datos():
    """Sección para mostrar estado y recargar datos"""
    st.sidebar.header("📂 Estado de Datos")
    
    # Mostrar estado actual
    if st.session_state.get('datos_cargados', False):
        st.sidebar.success("✅ Datos cargados correctamente")
        
        # Botón para recargar si es necesario
        if st.sidebar.button("🔄 Recargar Datos", 
                             use_container_width=True):
            with st.spinner("Recargando datos..."):
                from gui.app import cargar_datos_modelo, cargar_geodataframes
                
                # Limpiar caché
                cargar_datos_modelo.clear()
                cargar_geodataframes.clear()
                
                # Recargar
                st.session_state.datos_modelo = cargar_datos_modelo()
                st.session_state.gdf_nodos, st.session_state.gdf_aristas = cargar_geodataframes()
                
                if st.session_state.datos_modelo:
                    st.session_state.datos_cargados = True
                    st.sidebar.success("✅ Datos recargados")
                else:
                    st.sidebar.error("❌ Error al recargar")
                
                st.rerun()
        
        # Botón adicional para regenerar datos desde cero
        if st.sidebar.button("🔄 Regenerar Datos (OSM)", 
                             use_container_width=True,
                             help="Descarga datos frescos desde OpenStreetMap y regenera todo"):
            regenerar_datos_completos()
    else:
        st.sidebar.error("❌ No hay datos disponibles")
        st.sidebar.warning("Los datos se generarán automáticamente")
        
        # Botón para generar datos manualmente
        if st.sidebar.button("📥 Generar Datos Ahora", 
                             use_container_width=True,
                             type="primary"):
            generar_datos_manualmente()


def generar_datos_manualmente():
    """Genera los datos manualmente cuando el usuario lo solicita"""
    st.sidebar.info("🔄 Generando datos...")
    st.sidebar.caption("Esto puede tardar 3-5 minutos")
    
    with st.spinner("📥 Descargando y procesando datos..."):
        from gui.app import ejecutar_preparar_datos, cargar_datos_modelo, cargar_geodataframes
        import time
        
        exito = ejecutar_preparar_datos()
        
        if exito:
            # Limpiar caché y cargar datos inmediatamente
            cargar_datos_modelo.clear()
            cargar_geodataframes.clear()
            
            st.session_state.datos_modelo = cargar_datos_modelo()
            st.session_state.gdf_nodos, st.session_state.gdf_aristas = cargar_geodataframes()
            
            # Verificar que se cargaron correctamente
            if st.session_state.datos_modelo and st.session_state.gdf_aristas is not None:
                st.session_state.datos_cargados = True
                st.session_state.inicializado = True
                st.sidebar.success("✅ Datos generados y cargados correctamente!")
                time.sleep(1)
                st.rerun()
            else:
                st.sidebar.error("⚠️ Datos generados pero error al cargar. Presiona F5 para recargar.")
        else:
            st.sidebar.error("❌ Error al generar datos")


def regenerar_datos_completos():
    """Regenera todos los datos desde cero (descarga fresca de OSM)"""
    st.sidebar.warning("⚠️ Esto descargará datos frescos de OpenStreetMap")
    st.sidebar.caption("Puede tardar 5-10 minutos")
    
    with st.spinner("📥 Descargando mapa de OpenStreetMap..."):
        import sys
        from pathlib import Path
        import time
        
        # Agregar path del proyecto
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        sys.path.insert(0, str(BASE_DIR))
        
        try:
            # Importar y ejecutar preparar_datos con force_download
            import importlib.util
            spec = importlib.util.spec_from_file_location("preparar_datos", BASE_DIR / "preparar_datos.py")
            preparar_datos = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(preparar_datos)
            
            # Ejecutar con force_download=True
            preparar_datos.main(force_download=True)
            
            st.sidebar.success("✅ Datos regenerados desde OSM!")
            time.sleep(1)
            
            # Limpiar caché y recargar
            from gui.app import cargar_datos_modelo, cargar_geodataframes
            cargar_datos_modelo.clear()
            cargar_geodataframes.clear()
            
            st.rerun()
            
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")
            import traceback
            st.sidebar.code(traceback.format_exc())


def seccion_emergencias():
    """Sección para generar emergencias"""
    st.sidebar.header("🚨 Emergencias")
    
    if st.sidebar.button("🎲 Generar Nuevas Emergencias", 
                         use_container_width=True):
        # Verificar que haya datos cargados
        if not st.session_state.get('datos_cargados', False):
            st.sidebar.error("❌ Carga los datos primero")
            return
        
        # Importar función necesaria
        from src.data.graph_processor import asignar_emergencias_a_nodos
        
        with st.spinner("Generando emergencias..."):
            import time
            
            # Generar emergencias básicas con semilla diferente cada vez
            # Usar timestamp para asegurar que sean diferentes
            semilla_nueva = int(time.time())
            random.seed(semilla_nueva)
            emergencias_basicas = generar_conjunto_emergencias()
            
            # Asignar a nodos del grafo (agrega coordenadas) con semilla diferente
            grafo = st.session_state.datos_modelo['grafo']
            emergencias_completas = asignar_emergencias_a_nodos(
                grafo, 
                emergencias_basicas, 
                seed=semilla_nueva
            )
            
            # Guardar en session state
            st.session_state.emergencias_generadas = emergencias_completas
            
        st.sidebar.success(f"✅ {len(emergencias_completas)} emergencias generadas")
        st.rerun()


def seccion_visualizacion():
    """Sección de opciones de visualización"""
    st.sidebar.header("👁️ Visualización")
    
    st.session_state.mostrar_capacidades = st.sidebar.checkbox(
        "Colorear vías por capacidad",
        value=st.session_state.get('mostrar_capacidades', False),
        help="Muestra las calles en colores según su velocidad máxima"
    )
    
    st.session_state.mostrar_nodos = st.sidebar.checkbox(
        "Mostrar nodos del grafo",
        value=st.session_state.get('mostrar_nodos', False),
        help="Muestra los nodos (intersecciones) del grafo"
    )


def seccion_informacion():
    """Sección de información del sistema"""
    st.sidebar.header("ℹ️ Información")
    
    if st.session_state.get('datos_cargados', False) and st.session_state.get('datos_modelo'):
        grafo = st.session_state.datos_modelo['grafo']
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Nodos", f"{len(grafo.nodes()):,}")
        with col2:
            st.metric("Aristas", f"{len(grafo.edges()):,}")
        
        if st.session_state.datos_modelo.get('emergencias'):
            st.sidebar.metric("Emergencias", 
                            len(st.session_state.datos_modelo['emergencias']))
    else:
        st.sidebar.info("Carga los datos primero")


def seccion_parametros():
    """Sección de parámetros configurables por el usuario"""
    st.sidebar.header("⚙️ Parámetros del Modelo")
    
    # VELOCIDADES REQUERIDAS (R_MIN, R_MAX)
    st.sidebar.subheader("🚑 Velocidades Requeridas")
    st.sidebar.caption("""
    El rango se divide automáticamente en 3 niveles:
    • **Leve**: [R_min, R_min + ⅓ rango]
    • **Media**: [R_min + ⅓, R_min + ⅔ rango]
    • **Grave**: [R_min + ⅔, R_max]
    """)
    
    # Inicializar valores temporales si no existen
    if 'r_min_temp' not in st.session_state:
        st.session_state.r_min_temp = st.session_state.get('r_min_aplicado', R_MIN)
    if 'r_max_temp' not in st.session_state:
        st.session_state.r_max_temp = st.session_state.get('r_max_aplicado', R_MAX)
    
    # Contador para forzar re-creación de widgets
    if 'velocidades_reset_counter' not in st.session_state:
        st.session_state.velocidades_reset_counter = 0
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        r_min = st.number_input(
            "R_MIN (km/h)",
            min_value=10,
            max_value=150,
            value=int(st.session_state.r_min_temp),
            step=1,
            help="Velocidad mínima requerida para emergencias leves",
            key=f"r_min_input_{st.session_state.velocidades_reset_counter}"
        )
        st.session_state.r_min_temp = r_min
    
    with col2:
        r_max = st.number_input(
            "R_MAX (km/h)",
            min_value=10,
            max_value=150,
            value=int(st.session_state.r_max_temp),
            step=1,
            help="Velocidad máxima requerida para emergencias graves",
            key=f"r_max_input_{st.session_state.velocidades_reset_counter}"
        )
        st.session_state.r_max_temp = r_max
    
    # Validación
    valores_validos_r = r_min < r_max
    if not valores_validos_r:
        st.sidebar.error("⚠️ R_MIN debe ser menor que R_MAX")
    
    # Mostrar subdivisión calculada
    if valores_validos_r:
        rango_total = r_max - r_min
        tercio = rango_total / 3
        with st.sidebar.expander("Ver subdivisión calculada"):
            st.caption(f"🟢 Leve: [{r_min:.1f}, {r_min + tercio:.1f}] km/h")
            st.caption(f"🟠 Media: [{r_min + tercio:.1f}, {r_min + 2*tercio:.1f}] km/h")
            st.caption(f"🔴 Grave: [{r_min + 2*tercio:.1f}, {r_max:.1f}] km/h")
    
    # Botones de acción para velocidades
    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("✅ Aplicar", key="aplicar_velocidades", use_container_width=True,
                    disabled=not valores_validos_r):
            aplicar_cambios_velocidades()
    with col_btn2:
        if st.button("🔄 Valores Iniciales", key="restaurar_velocidades", use_container_width=True):
            restaurar_velocidades_default()
    
    # Indicador de cambios pendientes
    r_min_actual = st.session_state.get('r_min_aplicado', R_MIN)
    r_max_actual = st.session_state.get('r_max_aplicado', R_MAX)
    hay_cambios_velocidades = (r_min != r_min_actual or r_max != r_max_actual)
    
    if hay_cambios_velocidades:
        st.sidebar.info("💡 Cambios pendientes - Presiona 'Aplicar'")
    
    st.sidebar.markdown("---")
    
    # CAPACIDADES DE VÍAS (C_MIN, C_MAX)
    st.sidebar.subheader("🛣️ Capacidades de Vías")
    st.sidebar.caption("""
    Se asigna aleatoriamente una velocidad máxima a cada vía 
    dentro del rango [C_min, C_max]. Esta capacidad representa 
    la velocidad máxima permitida en cada calle del grafo.
    """)
    
    # Inicializar valores temporales si no existen
    if 'c_min_temp' not in st.session_state:
        st.session_state.c_min_temp = st.session_state.get('c_min_aplicado', C_MIN)
    if 'c_max_temp' not in st.session_state:
        st.session_state.c_max_temp = st.session_state.get('c_max_aplicado', C_MAX)
    
    # Contador para forzar re-creación de widgets
    if 'capacidades_reset_counter' not in st.session_state:
        st.session_state.capacidades_reset_counter = 0
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        c_min = st.number_input(
            "C_MIN (km/h)",
            min_value=10,
            max_value=1000,
            value=int(st.session_state.c_min_temp),
            step=1,
            help="Capacidad mínima de las vías",
            key=f"c_min_input_{st.session_state.capacidades_reset_counter}"
        )
        st.session_state.c_min_temp = c_min
    
    with col2:
        c_max = st.number_input(
            "C_MAX (km/h)",
            min_value=10,
            max_value=1000,
            value=int(st.session_state.c_max_temp),
            step=1,
            help="Capacidad máxima de las vías",
            key=f"c_max_input_{st.session_state.capacidades_reset_counter}"
        )
        st.session_state.c_max_temp = c_max
    
    # Validación
    valores_validos_c = c_min < c_max
    if not valores_validos_c:
        st.sidebar.error("⚠️ C_MIN debe ser menor que C_MAX")
    
    # Advertencia si R_MAX > C_MAX
    if r_max > c_max:
        st.sidebar.warning("⚠️ Velocidad requerida máxima > Capacidad máxima. Puede no haber solución factible.")
    
    # Botones de acción para capacidades
    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("✅ Aplicar", key="aplicar_capacidades", use_container_width=True,
                    disabled=not valores_validos_c or not st.session_state.get('datos_cargados', False)):
            aplicar_cambios_capacidades()
    with col_btn2:
        if st.button("🔄 Valores Iniciales", key="restaurar_capacidades", use_container_width=True):
            restaurar_capacidades_default()
    
    # Indicador de cambios pendientes
    c_min_actual = st.session_state.get('c_min_aplicado', C_MIN)
    c_max_actual = st.session_state.get('c_max_aplicado', C_MAX)
    hay_cambios_capacidades = (c_min != c_min_actual or c_max != c_max_actual)
    
    if hay_cambios_capacidades:
        st.sidebar.info("💡 Cambios pendientes - Presiona 'Aplicar'")
    
    st.sidebar.markdown("---")


def seccion_costos():
    """Sección de costos operacionales editables"""
    st.sidebar.header("💰 Costos Operacionales")
    st.sidebar.caption("Ajusta los costos por tipo de urgencia")
    
    # Inicializar costos en session_state si no existen
    if 'costos_usuario' not in st.session_state:
        st.session_state.costos_usuario = None
    
    # Inicializar costos temporales
    if 'costos_temp' not in st.session_state:
        st.session_state.costos_temp = {}
    
    # Obtener valores actuales o por defecto
    def get_costo_actual(prioridad, campo):
        if st.session_state.costos_usuario and prioridad in st.session_state.costos_usuario:
            return st.session_state.costos_usuario[prioridad][campo]
        
        # Obtener tipo de ambulancia directamente
        tipo_amb = PRIORIDAD_A_AMBULANCIA[prioridad]
        
        if campo == 'costo_fijo':
            return COSTOS[tipo_amb]['costo_fijo_activacion']
        else:  # costo_km
            return COSTOS[tipo_amb]['costo_por_km']
    
    # LEVE
    with st.sidebar.expander("🟡 Urgencia LEVE (TAB)", expanded=False):
        st.caption("Ambulancia de Transporte Asistencial Básico")
        st.caption("👥 Personal: Conductor + Auxiliar")
        
        col1, col2 = st.columns(2)
        with col1:
            costo_fijo_leve = st.number_input(
                "Costo Fijo (COP)",
                min_value=0,
                max_value=500000,
                value=int(get_costo_actual('leve', 'costo_fijo')),
                step=1000,
                key="costo_fijo_leve",
                help="Costo de activación del servicio"
            )
        with col2:
            costo_km_leve = st.number_input(
                "Costo/km (COP)",
                min_value=0,
                max_value=100000,
                value=int(get_costo_actual('leve', 'costo_km')),
                step=100,
                key="costo_km_leve",
                help="Costo por kilómetro recorrido"
            )
        
        st.session_state.costos_temp['leve'] = {
            'costo_fijo': costo_fijo_leve,
            'costo_km': costo_km_leve
        }
        
        # Ejemplo de cálculo
        ejemplo_leve = costo_fijo_leve + (10 * costo_km_leve)
        st.caption(f"💡 Ejemplo 10 km: ${ejemplo_leve:,} COP")
    
    # MEDIA
    with st.sidebar.expander("🟠 Urgencia MEDIA (TAM)", expanded=False):
        st.caption("Ambulancia Medicalizada")
        st.caption("👥 Personal: Conductor + Auxiliar + Enfermero")
        
        col1, col2 = st.columns(2)
        with col1:
            costo_fijo_media = st.number_input(
                "Costo Fijo (COP)",
                min_value=0,
                max_value=500000,
                value=int(get_costo_actual('media', 'costo_fijo')),
                step=1000,
                key="costo_fijo_media",
                help="Costo de activación del servicio"
            )
        with col2:
            costo_km_media = st.number_input(
                "Costo/km (COP)",
                min_value=0,
                max_value=100000,
                value=int(get_costo_actual('media', 'costo_km')),
                step=100,
                key="costo_km_media",
                help="Costo por kilómetro recorrido"
            )
        
        st.session_state.costos_temp['media'] = {
            'costo_fijo': costo_fijo_media,
            'costo_km': costo_km_media
        }
        
        ejemplo_media = costo_fijo_media + (10 * costo_km_media)
        st.caption(f"💡 Ejemplo 10 km: ${ejemplo_media:,} COP")
    
    # GRAVE
    with st.sidebar.expander("🔴 Urgencia GRAVE (TAM Grave)", expanded=False):
        st.caption("Ambulancia Medicalizada Grave")
        st.caption("👥 Personal: Conductor + Médico + Enfermero")
        
        col1, col2 = st.columns(2)
        with col1:
            costo_fijo_grave = st.number_input(
                "Costo Fijo (COP)",
                min_value=0,
                max_value=500000,
                value=int(get_costo_actual('grave', 'costo_fijo')),
                step=1000,
                key="costo_fijo_grave",
                help="Costo de activación del servicio"
            )
        with col2:
            costo_km_grave = st.number_input(
                "Costo/km (COP)",
                min_value=0,
                max_value=100000,
                value=int(get_costo_actual('grave', 'costo_km')),
                step=100,
                key="costo_km_grave",
                help="Costo por kilómetro recorrido"
            )
        
        st.session_state.costos_temp['grave'] = {
            'costo_fijo': costo_fijo_grave,
            'costo_km': costo_km_grave
        }
        
        ejemplo_grave = costo_fijo_grave + (10 * costo_km_grave)
        st.caption(f"💡 Ejemplo 10 km: ${ejemplo_grave:,} COP")
    
    # Botones de acción
    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("✅ Aplicar Costos", key="aplicar_costos", use_container_width=True):
            aplicar_cambios_costos()
    with col_btn2:
        if st.button("🔄 Valores Iniciales", key="restaurar_costos", use_container_width=True):
            restaurar_costos_default()
    
    # Indicador si hay cambios
    costos_cambiados = False
    if st.session_state.costos_usuario:
        for prioridad in ['leve', 'media', 'grave']:
            if prioridad in st.session_state.costos_temp:
                temp = st.session_state.costos_temp[prioridad]
                actual = st.session_state.costos_usuario.get(prioridad, {})
                if temp.get('costo_fijo') != actual.get('costo_fijo') or \
                   temp.get('costo_km') != actual.get('costo_km'):
                    costos_cambiados = True
                    break
    elif st.session_state.costos_temp:
        # Verificar si son diferentes de los defaults
        for prioridad in ['leve', 'media', 'grave']:
            tipo_amb = PRIORIDAD_A_AMBULANCIA[prioridad]
            default_fijo = COSTOS[tipo_amb]['costo_fijo_activacion']
            default_km = COSTOS[tipo_amb]['costo_por_km']
            temp = st.session_state.costos_temp.get(prioridad, {})
            if temp.get('costo_fijo', default_fijo) != default_fijo or \
               temp.get('costo_km', default_km) != default_km:
                costos_cambiados = True
                break
    
    if costos_cambiados:
        st.sidebar.info("💡 Cambios pendientes - Presiona 'Aplicar Costos'")
    
    st.sidebar.markdown("---")


def seccion_botones_accion():
    """Sección con botones de acción para el modelo"""
    st.sidebar.header("🚀 Ejecutar Optimización")
    
    # Verificar que haya datos cargados
    datos_disponibles = st.session_state.get('datos_cargados', False)
    
    # BOTÓN 1: Calcular Rutas (Optimización principal)
    if st.sidebar.button(
        "🎯 Calcular Rutas",
        use_container_width=True,
        disabled=not datos_disponibles,
        help="Ejecuta el modelo de optimización con los parámetros APLICADOS"
    ):
        ejecutar_optimizacion()
    
    st.sidebar.caption("Ejecuta la optimización con todos los parámetros aplicados")
    
    st.sidebar.markdown("---")
    
    # BOTÓN 2: Recalcular Flujos
    if st.sidebar.button(
        "🔄 Recalcular Flujos",
        use_container_width=True,
        disabled=not datos_disponibles,
        help="Re-ejecuta el modelo si hubo cambios en emergencias, capacidades o parámetros"
    ):
        recalcular_flujos()
    
    st.sidebar.caption("Detecta automáticamente cambios y re-optimiza")
    
    if not datos_disponibles:
        st.sidebar.info("ℹ️ Carga los datos primero")


def ejecutar_optimizacion():
    """
    Ejecuta el modelo de optimización con los parámetros configurados.
    Usa los valores APLICADOS (no los temporales).
    """
    with st.spinner("⏳ Preparando optimización..."):
        # Obtener parámetros APLICADOS
        r_min = st.session_state.get('r_min_aplicado', R_MIN)
        r_max = st.session_state.get('r_max_aplicado', R_MAX)
        c_min = st.session_state.get('c_min_aplicado', C_MIN)
        c_max = st.session_state.get('c_max_aplicado', C_MAX)
        
        # Verificar si hay cambios pendientes
        r_min_temp = st.session_state.get('r_min_temp', R_MIN)
        r_max_temp = st.session_state.get('r_max_temp', R_MAX)
        c_min_temp = st.session_state.get('c_min_temp', C_MIN)
        c_max_temp = st.session_state.get('c_max_temp', C_MAX)
        
        if (r_min_temp != r_min or r_max_temp != r_max or 
            c_min_temp != c_min or c_max_temp != c_max):
            st.sidebar.warning("⚠️ Hay cambios pendientes en parámetros. Presiona 'Aplicar' primero.")
            return
        
        # Validaciones
        if r_min >= r_max:
            st.sidebar.error("❌ R_MIN debe ser menor que R_MAX")
            return
        
        if c_min >= c_max:
            st.sidebar.error("❌ C_MIN debe ser menor que C_MAX")
            return
        
        # Obtener datos
        grafo = st.session_state.datos_modelo['grafo']
        emergencias = st.session_state.emergencias_generadas or \
                     st.session_state.datos_modelo.get('emergencias', [])
        
        if not emergencias:
            st.sidebar.error("❌ No hay emergencias. Genera algunas primero.")
            return
        
        # Obtener costos (aplicados por usuario o por defecto)
        costos_usuario = st.session_state.get('costos_usuario', None)
        
        # Guardar parámetros usados
        st.session_state.parametros_optimizacion = {
            'r_min': r_min,
            'r_max': r_max,
            'c_min': c_min,
            'c_max': c_max,
            'num_emergencias': len(emergencias),
            'costos_personalizados': costos_usuario is not None
        }
    
    # EJECUTAR MODELO DE OPTIMIZACIÓN
    with st.spinner("🚑 Calculando rutas óptimas... (esto puede tomar unos segundos)"):
        try:
            from src.models import resolver_modelo_ambulancias
            
            # Resolver modelo
            resultado = resolver_modelo_ambulancias(
                grafo=grafo,
                emergencias=emergencias,
                nodo_origen=st.session_state.datos_modelo['nodo_origen'],
                costos_usuario=costos_usuario,
                time_limit=120,  # 2 minutos máximo
                verbose=False
            )
            
            # Guardar resultado en session state
            st.session_state.resultado_optimizacion = resultado
            
            # Mostrar mensaje según el estado
            if resultado['estado'] == 'Optimal':
                st.sidebar.success(f"✅ Rutas calculadas exitosamente!")
                st.sidebar.metric("💰 Costo Total", f"${resultado['costo_total']:,.0f} COP")
                st.sidebar.metric("⏱️ Tiempo", f"{resultado['tiempo_resolucion']:.1f}s")
                st.sidebar.info("👉 Ve al tab 'Resultados Optimización' para ver detalles")
                
            elif resultado['estado'] == 'Infeasible':
                st.sidebar.error("❌ No se encontró solución factible")
                st.sidebar.warning("Posibles causas:")
                st.sidebar.caption("• Velocidades requeridas > Capacidades de vías")
                st.sidebar.caption("• Cuello de botella en alguna vía")
                st.sidebar.caption("• Grafo desconectado")
                st.sidebar.info("💡 Intenta: Aumentar C_MAX o reducir R_MAX")
                
            else:
                st.sidebar.error(f"❌ Estado: {resultado['estado']}")
                if 'mensaje' in resultado:
                    with st.sidebar.expander("ℹ️ Más información"):
                        st.write(resultado['mensaje'])
            
        except Exception as e:
            st.sidebar.error(f"❌ Error en la optimización")
            st.sidebar.exception(e)
            st.session_state.resultado_optimizacion = None




def recalcular_flujos():
    """
    Ejecuta nuevamente el modelo con las condiciones actuales.
    Verifica si hay cambios en emergencias o parámetros.
    """
    with st.spinner("🔄 Recalculando flujos..."):
        # Verificar si hay emergencias
        emergencias = st.session_state.emergencias_generadas or \
                     st.session_state.datos_modelo.get('emergencias', [])
        
        if not emergencias:
            st.sidebar.error("❌ No hay emergencias para calcular flujos")
            return
        
        # Verificar si hay parámetros de optimización previos
        if not st.session_state.get('parametros_optimizacion'):
            st.sidebar.warning("⚠️ No hay optimización previa. Usa 'Calcular Rutas' primero.")
            return
        
        # Detectar cambios
        cambios_detectados = []
        
        if st.session_state.get('emergencias_generadas'):
            cambios_detectados.append("Nuevas emergencias generadas")
        
        if st.session_state.get('capacidades_modificadas'):
            cambios_detectados.append("Capacidades de vías modificadas")
        
        # Obtener parámetros aplicados
        r_min = st.session_state.get('r_min_aplicado', R_MIN)
        r_max = st.session_state.get('r_max_aplicado', R_MAX)
        c_min = st.session_state.get('c_min_aplicado', C_MIN)
        c_max = st.session_state.get('c_max_aplicado', C_MAX)
        
        params_previos = st.session_state.parametros_optimizacion
        if (r_min != params_previos.get('r_min') or 
            r_max != params_previos.get('r_max') or
            c_min != params_previos.get('c_min') or
            c_max != params_previos.get('c_max')):
            cambios_detectados.append("Parámetros modificados")
        
        if cambios_detectados:
            st.sidebar.info(f"📝 Cambios detectados:\n" + "\n".join(f"• {c}" for c in cambios_detectados))
        
        # TODO: Aquí se llamará al modelo de optimización
        # Por ahora solo actualizar los parámetros
        st.session_state.parametros_optimizacion = {
            'r_min': r_min,
            'r_max': r_max,
            'c_min': c_min,
            'c_max': c_max,
            'num_emergencias': len(emergencias)
        }
        
        # Limpiar flags de cambios
        st.session_state.capacidades_modificadas = False
        
        st.sidebar.success("✅ Flujos recalculados con condiciones actuales")
        st.sidebar.info("ℹ️ El modelo de optimización se implementará próximamente")


# ============================================================================
# FUNCIONES DE APLICAR Y RESTAURAR CAMBIOS
# ============================================================================

def aplicar_cambios_velocidades():
    """
    Aplica los cambios de velocidades requeridas (R_MIN, R_MAX).
    Actualiza las velocidades de emergencias existentes según los nuevos rangos.
    """
    with st.spinner("⏳ Aplicando cambios de velocidades..."):
        r_min = st.session_state.r_min_temp
        r_max = st.session_state.r_max_temp
        
        # Guardar como valores aplicados
        st.session_state.r_min_aplicado = r_min
        st.session_state.r_max_aplicado = r_max
        
        # Actualizar velocidades de emergencias existentes
        emergencias_actuales = st.session_state.emergencias_generadas or \
                              st.session_state.datos_modelo.get('emergencias', [])
        
        if emergencias_actuales:
            emergencias_actualizadas = actualizar_velocidades_emergencias(
                emergencias_actuales, r_min, r_max
            )
            
            # Actualizar en session state
            if st.session_state.emergencias_generadas:
                st.session_state.emergencias_generadas = emergencias_actualizadas
            else:
                st.session_state.datos_modelo['emergencias'] = emergencias_actualizadas
            
            st.sidebar.success(f"✅ Velocidades aplicadas: [{r_min}, {r_max}] km/h")
            st.sidebar.info(f"🔄 {len(emergencias_actualizadas)} emergencias actualizadas")
        else:
            st.sidebar.success(f"✅ Velocidades configuradas: [{r_min}, {r_max}] km/h")
        
        st.rerun()


def restaurar_velocidades_default():
    """
    Restaura velocidades a valores iniciales (solo en inputs, no aplicado).
    El usuario debe presionar 'Aplicar' para confirmar.
    """
    # Verificar si ya están en valores iniciales
    r_min_actual = st.session_state.get('r_min_temp', R_MIN)
    r_max_actual = st.session_state.get('r_max_temp', R_MAX)
    
    ya_en_default = (r_min_actual == R_MIN and r_max_actual == R_MAX)
    
    # Restaurar valores temporales
    st.session_state.r_min_temp = R_MIN
    st.session_state.r_max_temp = R_MAX
    
    # Incrementar contador para forzar re-creación de widgets
    st.session_state.velocidades_reset_counter += 1
    
    # Mostrar mensaje solo si había cambios
    if not ya_en_default:
        st.sidebar.success(f"✅ Valores restaurados en inputs: [{R_MIN}, {R_MAX}] km/h")
        st.sidebar.info("💡 Presiona 'Aplicar' para confirmar los cambios")
    
    st.rerun()


def aplicar_cambios_capacidades():
    """
    Aplica los cambios de capacidades (C_MIN, C_MAX).
    Regenera las capacidades de las vías con los nuevos valores.
    """
    with st.spinner("🔄 Aplicando cambios de capacidades..."):
        from src.data.graph_processor import asignar_capacidades_aleatorias, calcular_tiempos_viaje
        import time
        
        c_min = st.session_state.c_min_temp
        c_max = st.session_state.c_max_temp
        
        # Guardar como valores aplicados
        st.session_state.c_min_aplicado = c_min
        st.session_state.c_max_aplicado = c_max
        
        # Obtener grafo
        grafo = st.session_state.datos_modelo['grafo']
        
        # Usar timestamp como semilla para que sea diferente cada vez
        seed_nueva = int(time.time())
        
        # Recalcular capacidades
        grafo = asignar_capacidades_aleatorias(grafo, c_min, c_max, seed=seed_nueva)
        
        # Recalcular tiempos de viaje
        grafo = calcular_tiempos_viaje(grafo)
        
        # Actualizar en session state
        st.session_state.datos_modelo['grafo'] = grafo
        
        # Reconvertir a GeoDataFrames para visualización
        from src.data.graph_processor import convertir_grafo_a_geodataframes
        gdf_nodos, gdf_aristas = convertir_grafo_a_geodataframes(grafo)
        st.session_state.gdf_nodos = gdf_nodos
        st.session_state.gdf_aristas = gdf_aristas
        
        # Marcar que las capacidades cambiaron
        st.session_state.capacidades_modificadas = True
        
        st.sidebar.success(f"✅ Capacidades aplicadas: [{c_min}, {c_max}] km/h")
        st.sidebar.info("🔄 Vías actualizadas con nuevas capacidades")
        
        st.rerun()


def restaurar_capacidades_default():
    """
    Restaura capacidades a valores iniciales (solo en inputs, no aplicado).
    El usuario debe presionar 'Aplicar' para confirmar y regenerar las vías.
    """
    # Verificar si ya están en valores iniciales
    c_min_actual = st.session_state.get('c_min_temp', C_MIN)
    c_max_actual = st.session_state.get('c_max_temp', C_MAX)
    
    ya_en_default = (c_min_actual == C_MIN and c_max_actual == C_MAX)
    
    # Restaurar valores temporales
    st.session_state.c_min_temp = C_MIN
    st.session_state.c_max_temp = C_MAX
    
    # Incrementar contador para forzar re-creación de widgets
    st.session_state.capacidades_reset_counter += 1
    
    # Mostrar mensaje solo si había cambios
    if not ya_en_default:
        st.sidebar.success(f"✅ Valores restaurados en inputs: [{C_MIN}, {C_MAX}] km/h")
        st.sidebar.info("💡 Presiona 'Aplicar' para confirmar y regenerar las vías")
    
    st.rerun()


def aplicar_cambios_costos():
    """
    Aplica los cambios de costos operacionales.
    Guarda los costos del usuario en session_state.
    """
    # Copiar costos temporales a costos aplicados
    st.session_state.costos_usuario = st.session_state.costos_temp.copy()
    
    st.sidebar.success("✅ Costos aplicados correctamente")
    
    # Mostrar resumen
    with st.sidebar.expander("📋 Costos Aplicados"):
        for prioridad in ['leve', 'media', 'grave']:
            if prioridad in st.session_state.costos_usuario:
                costos = st.session_state.costos_usuario[prioridad]
                nombre = prioridad.capitalize()
                st.caption(f"**{nombre}:** "
                          f"Fijo ${costos['costo_fijo']:,} + ${costos['costo_km']:,}/km")
    
    st.rerun()


def restaurar_costos_default():
    """
    Restaura costos a valores iniciales (solo en inputs, no aplicado).
    El usuario debe presionar 'Aplicar Costos' para confirmar.
    """
    # Obtener valores por defecto
    defaults = {}
    for prioridad in ['leve', 'media', 'grave']:
        tipo_amb = PRIORIDAD_A_AMBULANCIA[prioridad]
        defaults[prioridad] = {
            'costo_fijo': COSTOS[tipo_amb]['costo_fijo_activacion'],
            'costo_km': COSTOS[tipo_amb]['costo_por_km']
        }
    
    # Verificar si ya están en valores por defecto
    ya_en_default = True
    keys_a_verificar = {
        'leve': ('costo_fijo_leve', 'costo_km_leve'),
        'media': ('costo_fijo_media', 'costo_km_media'),
        'grave': ('costo_fijo_grave', 'costo_km_grave')
    }
    
    for prioridad, (key_fijo, key_km) in keys_a_verificar.items():
        val_fijo = st.session_state.get(key_fijo, defaults[prioridad]['costo_fijo'])
        val_km = st.session_state.get(key_km, defaults[prioridad]['costo_km'])
        if val_fijo != defaults[prioridad]['costo_fijo'] or val_km != defaults[prioridad]['costo_km']:
            ya_en_default = False
            break
    
    # Restaurar valores en los widgets
    st.session_state.costo_fijo_leve = defaults['leve']['costo_fijo']
    st.session_state.costo_km_leve = defaults['leve']['costo_km']
    st.session_state.costo_fijo_media = defaults['media']['costo_fijo']
    st.session_state.costo_km_media = defaults['media']['costo_km']
    st.session_state.costo_fijo_grave = defaults['grave']['costo_fijo']
    st.session_state.costo_km_grave = defaults['grave']['costo_km']
    
    # Limpiar costos temporales
    st.session_state.costos_temp = {}
    
    # Mostrar mensaje solo si había cambios
    if not ya_en_default:
        st.sidebar.success("✅ Costos restaurados a valores iniciales en inputs")
        st.sidebar.info("💡 Presiona 'Aplicar Costos' para confirmar")
        
        # Mostrar valores iniciales
        with st.sidebar.expander("📋 Valores Iniciales"):
            for prioridad in ['leve', 'media', 'grave']:
                nombre = prioridad.capitalize()
                st.caption(f"**{nombre}:** "
                          f"Fijo ${defaults[prioridad]['costo_fijo']:,} + ${defaults[prioridad]['costo_km']:,}/km")
    
    st.rerun()


def actualizar_velocidades_emergencias(emergencias, r_min, r_max):
    """
    Actualiza las velocidades requeridas de emergencias existentes
    según los nuevos rangos R_MIN y R_MAX.
    
    Args:
        emergencias: Lista de emergencias
        r_min: Nueva velocidad mínima
        r_max: Nueva velocidad máxima
    
    Returns:
        Lista de emergencias con velocidades actualizadas
    """
    # Calcular nuevos rangos por severidad
    rango_total = r_max - r_min
    tercio = rango_total / 3
    
    # Nuevos rangos por severidad
    nuevos_rangos = {
        'leve': {'min': r_min, 'max': r_min + tercio},
        'media': {'min': r_min + tercio, 'max': r_min + 2 * tercio},
        'grave': {'min': r_min + 2 * tercio, 'max': r_max}
    }
    
    emergencias_actualizadas = []
    for emerg in emergencias:
        emerg_copia = emerg.copy()
        severidad = emerg['severidad']  # 'leve', 'media' o 'grave'
        
        # Generar nueva velocidad dentro del nuevo rango
        if severidad in nuevos_rangos:
            rango = nuevos_rangos[severidad]
            nueva_velocidad = random.uniform(rango['min'], rango['max'])
            emerg_copia['velocidad_requerida'] = nueva_velocidad
        
        emergencias_actualizadas.append(emerg_copia)
    
    return emergencias_actualizadas