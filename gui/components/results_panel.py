# gui/components/results_panel.py
# Componente para mostrar resultados y estadísticas

"""
Componente para visualizar estadísticas, gráficos y tablas de datos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def mostrar_metricas_generales(grafo, gdf_aristas=None):
    """
    Muestra métricas generales del grafo en cards
    
    Args:
        grafo: Grafo de NetworkX
        gdf_aristas: GeoDataFrame de aristas (opcional)
    """
    st.subheader("📈 Métricas Generales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nodos Totales", f"{len(grafo.nodes()):,}")
    
    with col2:
        st.metric("Aristas Totales", f"{len(grafo.edges()):,}")
    
    with col3:
        longitud_total = sum([data['length'] for u, v, key, data in grafo.edges(keys=True, data=True)])
        st.metric("Longitud Total", f"{longitud_total/1000:.2f} km")
    
    with col4:
        if gdf_aristas is not None and 'capacity' in gdf_aristas.columns:
            cap_promedio = gdf_aristas['capacity'].mean()
            st.metric("Capacidad Promedio", f"{cap_promedio:.2f} km/h")
        else:
            st.metric("Capacidad Promedio", "N/A")


def graficar_distribucion_capacidades(gdf_aristas):
    """
    Crea gráfico de distribución de capacidades
    
    Args:
        gdf_aristas: GeoDataFrame de aristas
    
    Returns:
        plotly.graph_objects.Figure: Figura de Plotly
    """
    if gdf_aristas is None or 'capacity' not in gdf_aristas.columns:
        return None
    
    fig = px.histogram(
        gdf_aristas,
        x='capacity',
        nbins=30,
        title="Distribución de Capacidades de Vías",
        labels={'capacity': 'Capacidad (km/h)', 'count': 'Frecuencia'},
        color_discrete_sequence=['#667eea']
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Capacidad (km/h)",
        yaxis_title="Frecuencia"
    )
    
    return fig


def graficar_distribucion_tiempos(gdf_aristas):
    """
    Crea gráfico de distribución de tiempos de viaje
    
    Args:
        gdf_aristas: GeoDataFrame de aristas
    
    Returns:
        plotly.graph_objects.Figure: Figura de Plotly
    """
    if gdf_aristas is None or 'travel_time' not in gdf_aristas.columns:
        return None
    
    fig = px.histogram(
        gdf_aristas,
        x='travel_time',
        nbins=30,
        title="Distribución de Tiempos de Viaje",
        labels={'travel_time': 'Tiempo (minutos)', 'count': 'Frecuencia'},
        color_discrete_sequence=['#764ba2']
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Tiempo (minutos)",
        yaxis_title="Frecuencia"
    )
    
    return fig


def mostrar_estadisticas_capacidades(gdf_aristas):
    """
    Muestra estadísticas de capacidades en columnas
    
    Args:
        gdf_aristas: GeoDataFrame de aristas
    """
    if gdf_aristas is None or 'capacity' not in gdf_aristas.columns:
        st.warning("No hay datos de capacidad disponibles")
        return
    
    st.subheader("🚗 Estadísticas de Capacidades")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = graficar_distribucion_capacidades(gdf_aristas)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Estadísticas")
        st.metric("Mínima", f"{gdf_aristas['capacity'].min():.2f} km/h")
        st.metric("Máxima", f"{gdf_aristas['capacity'].max():.2f} km/h")
        st.metric("Promedio", f"{gdf_aristas['capacity'].mean():.2f} km/h")
        st.metric("Desv. Estándar", f"{gdf_aristas['capacity'].std():.2f} km/h")


def mostrar_estadisticas_tiempos(gdf_aristas):
    """
    Muestra estadísticas de tiempos de viaje
    
    Args:
        gdf_aristas: GeoDataFrame de aristas
    """
    if gdf_aristas is None or 'travel_time' not in gdf_aristas.columns:
        st.warning("No hay datos de tiempo de viaje disponibles")
        return
    
    st.subheader("⏱️ Estadísticas de Tiempos de Viaje")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = graficar_distribucion_tiempos(gdf_aristas)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Estadísticas")
        st.metric("Mínimo", f"{gdf_aristas['travel_time'].min():.3f} min")
        st.metric("Máximo", f"{gdf_aristas['travel_time'].max():.3f} min")
        st.metric("Promedio", f"{gdf_aristas['travel_time'].mean():.3f} min")
        st.metric("Total", f"{gdf_aristas['travel_time'].sum():.2f} min")


def mostrar_tabla_aristas(gdf_aristas, num_filas=50):
    """
    Muestra tabla de datos de aristas
    
    Args:
        gdf_aristas: GeoDataFrame de aristas
        num_filas (int): Número de filas a mostrar
    """
    if gdf_aristas is None:
        st.warning("No hay datos de aristas disponibles")
        return
    
    st.subheader("📋 Datos de Aristas (Muestra)")
    
    # Seleccionar columnas a mostrar (solo columnas simples, sin listas)
    columnas_disponibles = []
    
    # Verificar columnas comunes
    columnas_posibles = ['length', 'capacity', 'travel_time', 'highway', 'name', 'maxspeed', 'lanes']
    
    for col in columnas_posibles:
        if col in gdf_aristas.columns:
            # Verificar que no sea una columna de listas/objetos complejos
            try:
                primer_valor = gdf_aristas[col].iloc[0]
                # Solo incluir si no es lista, dict o similar
                if not isinstance(primer_valor, (list, dict)):
                    columnas_disponibles.append(col)
            except:
                pass
    
    if not columnas_disponibles:
        columnas_disponibles = ['length']  # Al menos mostrar length
    
    # Mostrar tabla
    df_muestra = gdf_aristas[columnas_disponibles].head(num_filas).copy()
    
    # Convertir a tipos simples para evitar errores de PyArrow
    for col in df_muestra.columns:
        if df_muestra[col].dtype == 'object':
            # Convertir a string si es object
            df_muestra[col] = df_muestra[col].astype(str)
    
    st.dataframe(df_muestra, use_container_width=True, height=400)
    
    # Botón de descarga
    csv = df_muestra.to_csv(index=False)
    st.download_button(
        label="📥 Descargar Muestra CSV",
        data=csv,
        file_name="aristas_muestra.csv",
        mime="text/csv",
        use_container_width=True
    )


def mostrar_resumen_emergencias(emergencias):
    """
    Muestra resumen de emergencias en métricas
    
    Args:
        emergencias: Lista de diccionarios con emergencias
    """
    if not emergencias:
        st.info("No hay emergencias para mostrar")
        return
    
    st.subheader("📈 Resumen de Emergencias")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Emergencias", len(emergencias))
    
    with col2:
        leves = sum(1 for e in emergencias if e['severidad'] == 'leve')
        st.metric("🟢 Leves", leves)
    
    with col3:
        medias = sum(1 for e in emergencias if e['severidad'] == 'media')
        st.metric("🟠 Medias", medias)
    
    with col4:
        graves = sum(1 for e in emergencias if e['severidad'] == 'grave')
        st.metric("🔴 Graves", graves)


def mostrar_tabla_emergencias(emergencias):
    """
    Muestra tabla detallada de emergencias
    
    Args:
        emergencias: Lista de diccionarios con emergencias
    """
    if not emergencias:
        st.info("No hay emergencias para mostrar")
        return
    
    st.subheader("📋 Detalles de Emergencias")
    
    # Crear DataFrame
    df_emergencias = pd.DataFrame(emergencias)
    
    # Seleccionar y formatear columnas
    columnas_mostrar = ['id', 'severidad', 'velocidad_requerida', 'ambulancia_id']
    if 'nodo_destino' in df_emergencias.columns:
        columnas_mostrar.extend(['nodo_destino', 'latitud', 'longitud'])
    
    df_mostrar = df_emergencias[columnas_mostrar].copy()
    
    # Formatear números
    if 'velocidad_requerida' in df_mostrar.columns:
        df_mostrar['velocidad_requerida'] = df_mostrar['velocidad_requerida'].round(2)
    if 'latitud' in df_mostrar.columns:
        df_mostrar['latitud'] = df_mostrar['latitud'].round(6)
    if 'longitud' in df_mostrar.columns:
        df_mostrar['longitud'] = df_mostrar['longitud'].round(6)
    
    # Función para colorear filas
    def colorear_fila(row):
        if row['severidad'] == 'grave':
            return ['background-color: #ffcccc'] * len(row)
        elif row['severidad'] == 'media':
            return ['background-color: #ffe6cc'] * len(row)
        else:
            return ['background-color: #ccffcc'] * len(row)
    
    # Mostrar tabla con estilo
    st.dataframe(
        df_mostrar.style.apply(colorear_fila, axis=1),
        use_container_width=True,
        height=400
    )
    
    # Botón de descarga
    csv = df_mostrar.to_csv(index=False)
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="emergencias.csv",
        mime="text/csv",
        use_container_width=True
    )


def graficar_emergencias_por_severidad(emergencias):
    """
    Crea gráfico de barras de emergencias por severidad
    
    Args:
        emergencias: Lista de diccionarios con emergencias
    
    Returns:
        plotly.graph_objects.Figure: Figura de Plotly
    """
    if not emergencias:
        return None
    
    # Contar por severidad
    conteo = {}
    for e in emergencias:
        sev = e['severidad']
        conteo[sev] = conteo.get(sev, 0) + 1
    
    # Ordenar
    orden = ['leve', 'media', 'grave']
    labels = []
    values = []
    colors = []
    
    color_map = {
        'leve': '#27ae60',
        'media': '#f39c12',
        'grave': '#e74c3c'
    }
    
    for sev in orden:
        if sev in conteo:
            labels.append(sev.capitalize())
            values.append(conteo[sev])
            colors.append(color_map[sev])
    
    # Crear gráfico
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Distribución de Emergencias por Severidad",
        xaxis_title="Severidad",
        yaxis_title="Cantidad",
        showlegend=False,
        height=400
    )
    
    return fig
