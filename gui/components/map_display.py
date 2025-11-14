# gui/components/map_display.py
# Componente para mostrar el mapa en la interfaz

"""
Componente especializado para renderizar mapas con Folium en Streamlit
"""

import streamlit as st
import folium
from streamlit_folium import folium_static


def crear_mapa_base(centro_lat, centro_lon, zoom=15):
    """
    Crea el mapa base de Folium
    
    Args:
        centro_lat (float): Latitud del centro
        centro_lon (float): Longitud del centro
        zoom (int): Nivel de zoom inicial
    
    Returns:
        folium.Map: Mapa base
    """
    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    return mapa


def agregar_grafo_al_mapa(mapa, gdf_aristas, mostrar_capacidades=False):
    """
    Agrega las calles del grafo al mapa
    
    Args:
        mapa: Mapa de Folium
        gdf_aristas: GeoDataFrame de aristas
        mostrar_capacidades (bool): Si True, colorea por capacidad
    
    Returns:
        folium.Map: Mapa con el grafo agregado
    """
    if gdf_aristas is None:
        return mapa
    
    # Estilo básico
    style_function = lambda x: {
        'color': '#3388ff',
        'weight': 2,
        'opacity': 0.6
    }
    
    # Estilo con capacidades
    if mostrar_capacidades and 'capacity' in gdf_aristas.columns:
        def style_with_capacity(feature):
            capacity = feature['properties'].get('capacity', 50)
            if capacity < 40:
                color = '#e74c3c'  # Rojo - baja
            elif capacity < 70:
                color = '#f39c12'  # Naranja - media
            else:
                color = '#27ae60'  # Verde - alta
            return {
                'color': color,
                'weight': 2,
                'opacity': 0.7
            }
        style_function = style_with_capacity
    
    # Campos para tooltip
    campos_tooltip = []
    aliases_tooltip = []
    
    if 'length' in gdf_aristas.columns:
        campos_tooltip.append('length')
        aliases_tooltip.append('Longitud (m)')
    
    if 'capacity' in gdf_aristas.columns:
        campos_tooltip.append('capacity')
        aliases_tooltip.append('Capacidad (km/h)')
    
    if 'travel_time' in gdf_aristas.columns:
        campos_tooltip.append('travel_time')
        aliases_tooltip.append('Tiempo (min)')
    
    # Agregar al mapa
    folium.GeoJson(
        gdf_aristas,
        name='Red Vial',
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=campos_tooltip,
            aliases=aliases_tooltip,
            localize=True
        ) if campos_tooltip else None
    ).add_to(mapa)
    
    return mapa


def agregar_nodos_al_mapa(mapa, gdf_nodos, max_nodos=100):
    """
    Agrega los nodos del grafo al mapa
    
    Args:
        mapa: Mapa de Folium
        gdf_nodos: GeoDataFrame de nodos
        max_nodos (int): Máximo de nodos a mostrar
    
    Returns:
        folium.Map: Mapa con nodos agregados
    """
    if gdf_nodos is None:
        return mapa
    
    # Limitar cantidad para rendimiento
    nodos_muestra = gdf_nodos.head(max_nodos) if len(gdf_nodos) > max_nodos else gdf_nodos
    
    for idx, nodo in nodos_muestra.iterrows():
        folium.CircleMarker(
            location=[nodo.geometry.y, nodo.geometry.x],
            radius=3,
            color='gray',
            fill=True,
            fillColor='gray',
            fillOpacity=0.4,
            weight=1
        ).add_to(mapa)
    
    return mapa


def agregar_origen_al_mapa(mapa, lat, lon, nombre="Clínica Medellín - Sede El Poblado"):
    """
    Agrega el punto de origen (Clínica) al mapa
    
    Args:
        mapa: Mapa de Folium
        lat (float): Latitud
        lon (float): Longitud
        nombre (str): Nombre del punto
    
    Returns:
        folium.Map: Mapa con origen agregado
    """
    # Marcador principal
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>🏥 ORIGEN</b><br>{nombre}",
        tooltip=nombre,
        icon=folium.Icon(color='blue', icon='plus', prefix='fa')
    ).add_to(mapa)
    
    # Círculo alrededor
    folium.Circle(
        location=[lat, lon],
        radius=50,
        color='blue',
        fill=True,
        fillColor='blue',
        fillOpacity=0.2,
        popup=nombre
    ).add_to(mapa)
    
    return mapa


def agregar_emergencias_al_mapa(mapa, emergencias):
    """
    Agrega las emergencias al mapa con marcadores coloreados
    
    Args:
        mapa: Mapa de Folium
        emergencias: Lista de diccionarios con info de emergencias
    
    Returns:
        folium.Map: Mapa con emergencias agregadas
    """
    if not emergencias:
        return mapa
    
    # Configuración de colores e iconos por severidad
    colores = {
        'leve': 'green',
        'media': 'orange',
        'grave': 'red'
    }
    
    iconos = {
        'leve': 'info-sign',
        'media': 'warning-sign',
        'grave': 'exclamation-sign'
    }
    
    # Agregar cada emergencia
    for e in emergencias:
        color = colores.get(e['severidad'], 'gray')
        icono = iconos.get(e['severidad'], 'info-sign')
        
        # HTML del popup
        popup_html = f"""
        <div style="width:220px; font-family: Arial, sans-serif;">
            <h4 style="margin:0 0 10px 0; color: {color};">🚨 Emergencia #{e['id']}</h4>
            <table style="width:100%; font-size:12px;">
                <tr><td><b>Severidad:</b></td><td style="text-transform:uppercase;">{e['severidad']}</td></tr>
                <tr><td><b>Vel. Req.:</b></td><td>{e['velocidad_requerida']:.2f} km/h</td></tr>
                <tr><td><b>Ambulancia:</b></td><td>#{e['ambulancia_id']}</td></tr>
                <tr><td><b>Nodo:</b></td><td>{e.get('nodo_destino', 'N/A')}</td></tr>
                <tr><td><b>Lat:</b></td><td>{e.get('latitud', 0):.6f}</td></tr>
                <tr><td><b>Lon:</b></td><td>{e.get('longitud', 0):.6f}</td></tr>
            </table>
        </div>
        """
        
        # Agregar marcador
        folium.Marker(
            location=[e.get('latitud', 0), e.get('longitud', 0)],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Emergencia #{e['id']} - {e['severidad'].upper()}",
            icon=folium.Icon(color=color, icon=icono, prefix='glyphicon')
        ).add_to(mapa)
    
    return mapa


def mostrar_mapa_streamlit(mapa, width=1400, height=700):
    """
    Renderiza el mapa en Streamlit
    
    Args:
        mapa: Mapa de Folium
        width (int): Ancho en píxeles
        height (int): Alto en píxeles
    """
    # Agregar control de capas
    folium.LayerControl().add_to(mapa)
    
    # Mostrar en Streamlit
    folium_static(mapa, width=width, height=height)


def mostrar_leyenda_mapa():
    """Muestra la leyenda del mapa"""
    st.markdown("---")
    st.markdown("### 📍 Leyenda del Mapa")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("🔵 **Origen**")
        st.caption("Clínica Medellín")
    
    with col2:
        st.markdown("🟢 **Emergencia Leve**")
        st.caption("30-50 km/h")
    
    with col3:
        st.markdown("🟠 **Emergencia Media**")
        st.caption("50-70 km/h")
    
    with col4:
        st.markdown("🔴 **Emergencia Grave**")
        st.caption("70-90 km/h")
    
    if st.session_state.get('mostrar_capacidades', False):
        st.markdown("---")
        st.markdown("### 🚗 Colores de Vías (por capacidad)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("🔴 **< 40 km/h**: Baja capacidad")
        with col2:
            st.markdown("🟠 **40-70 km/h**: Media capacidad")
        with col3:
            st.markdown("🟢 **> 70 km/h**: Alta capacidad")
    
    if st.session_state.get('resultado_optimizacion'):
        resultado = st.session_state.resultado_optimizacion
        if resultado is not None and resultado.get('estado') == 'Optimal':
            st.markdown("---")
            st.markdown("### 🎯 Rutas Optimizadas")
            st.caption("Las líneas de colores muestran las rutas calculadas para cada emergencia")


def agregar_rutas_optimizadas_al_mapa(mapa, grafo, resultado):
    """
    Agrega las rutas optimizadas al mapa con colores diferenciados.
    
    Args:
        mapa: Objeto folium.Map
        grafo: NetworkX MultiDiGraph
        resultado: Diccionario con resultados de la optimización
    
    Returns:
        mapa: Mapa con rutas agregadas
    """
    if resultado['estado'] != 'Optimal':
        return mapa
    
    # Paleta de colores para diferentes rutas
    colores = [
        '#e74c3c',  # Rojo
        '#3498db',  # Azul
        '#2ecc71',  # Verde
        '#9b59b6',  # Morado
        '#f39c12',  # Naranja
        '#1abc9c',  # Turquesa
        '#e67e22',  # Naranja oscuro
        '#34495e',  # Azul oscuro
        '#16a085',  # Verde azulado
        '#c0392b'   # Rojo oscuro
    ]
    
    # Agregar cada ruta al mapa
    for idx, detalle in enumerate(resultado['detalles']):
        ruta_nodos = detalle['ruta_nodos']
        color = colores[idx % len(colores)]
        
        # Obtener coordenadas de la ruta
        coords = []
        for nodo in ruta_nodos:
            if nodo in grafo.nodes():
                nodo_data = grafo.nodes[nodo]
                coords.append((nodo_data['y'], nodo_data['x']))
        
        if len(coords) < 2:
            continue
        
        # Información del popup
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px;">
            <h4 style="margin: 0; color: {color};">🚑 Emergencia #{detalle['emergencia_id']}</h4>
            <hr style="margin: 5px 0;">
            <b>Tipo:</b> {detalle['severidad'].capitalize()}<br>
            <b>Ambulancia:</b> {detalle['tipo_ambulancia'][:30]}{'...' if len(detalle['tipo_ambulancia']) > 30 else ''}<br>
            <b>Distancia:</b> {detalle['distancia_km']:.2f} km<br>
            <b>Aristas:</b> {detalle['num_aristas']}<br>
            <b>Velocidad req.:</b> {detalle['velocidad_requerida']:.1f} km/h<br>
            <hr style="margin: 5px 0;">
            <b>Costo Total:</b> ${detalle['costo_total']:,.0f} COP<br>
            <small>Fijo: ${detalle['costo_fijo']:,.0f} | Variable: ${detalle['costo_variable']:,.0f}</small>
        </div>
        """
        
        # Crear línea de ruta
        folium.PolyLine(
            coords,
            color=color,
            weight=5,
            opacity=0.8,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Ruta Emergencia #{detalle['emergencia_id']} ({detalle['severidad']})"
        ).add_to(mapa)
        
        # Marcar puntos intermedios cada N nodos (para rutas largas)
        if len(ruta_nodos) > 5:
            # Marcar nodo intermedio
            nodo_medio = ruta_nodos[len(ruta_nodos)//2]
            if nodo_medio in grafo.nodes():
                nodo_data = grafo.nodes[nodo_medio]
                folium.CircleMarker(
                    location=(nodo_data['y'], nodo_data['x']),
                    radius=4,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    popup=f"Punto medio Emerg #{detalle['emergencia_id']}",
                    tooltip="Punto intermedio"
                ).add_to(mapa)
        
        # Marcar nodo final con círculo más grande del mismo color
        nodo_final = ruta_nodos[-1]
        if nodo_final in grafo.nodes():
            nodo_data = grafo.nodes[nodo_final]
            folium.CircleMarker(
                location=(nodo_data['y'], nodo_data['x']),
                radius=10,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.6,
                weight=2,
                popup=folium.Popup(f"<b>Destino Emergencia #{detalle['emergencia_id']}</b><br>"
                                   f"{detalle['severidad'].capitalize()}<br>"
                                   f"{detalle['distancia_km']:.2f} km", max_width=200),
                tooltip=f"Destino Emerg #{detalle['emergencia_id']}"
            ).add_to(mapa)
            
            # Agregar etiqueta con número de emergencia
            folium.Marker(
                location=(nodo_data['y'], nodo_data['x']),
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 14px; font-weight: bold; color: {color}; '
                         f'text-shadow: 1px 1px 2px white, -1px -1px 2px white;">#{detalle["emergencia_id"]}</div>'
                )
            ).add_to(mapa)
    
    return mapa