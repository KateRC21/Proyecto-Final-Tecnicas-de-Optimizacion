# 🚑 Interfaz Gráfica - Sistema de Optimización de Ambulancias

## 📋 Descripción

Aplicación web interactiva desarrollada con Streamlit para visualizar y explorar el sistema de optimización de rutas de ambulancias en Medellín, Colombia.

## ✨ Características Principales

### Carga Automática de Datos
- ✅ **Los datos se cargan AUTOMÁTICAMENTE al abrir la aplicación**
- ✅ No requiere intervención manual del usuario
- ✅ Indicadores visuales claros del estado
- ✅ Experiencia profesional lista para producción

### 🏠 Tab de Inicio
- Información general del proyecto
- Guía de uso paso a paso
- Estado de los archivos de datos
- Parámetros configurados

### 🗺️ Mapa Interactivo
- **Visualización del grafo vial** (calles de Medellín)
- **Punto de origen** marcado (Clínica Medellín - Sede El Poblado)
- **Emergencias** con colores según severidad:
  - 🟢 Verde: Emergencias leves (30-50 km/h)
  - 🟠 Naranja: Emergencias medias (50-70 km/h)
  - 🔴 Rojo: Emergencias críticas (70-90 km/h)
- **Coloración opcional de vías** según capacidad
- **Tooltips informativos** con datos de cada elemento
- **Zoom y navegación interactiva**

### 📊 Datos y Estadísticas
- Métricas generales del grafo (nodos, aristas, longitudes)
- Distribución de capacidades de vías (histogramas)
- Distribución de tiempos de viaje
- Tabla de datos de aristas con opción de descarga
- Visualizaciones con Plotly

### 🚑 Emergencias
- Resumen de emergencias por severidad
- Tabla detallada con toda la información
- Coloración por tipo de severidad
- Descarga de datos en formato CSV
- Generación dinámica de nuevas emergencias

---

## 🚀 Inicio Rápido (3 pasos)

### Paso 1: Instalar Dependencias

```bash
pip install streamlit streamlit-folium scikit-learn
```

O instalar todos los requirements:

```bash
pip install -r requirements.txt
```

### Paso 2: Generar Datos (Solo primera vez)

```bash
python preparar_datos.py
```

Esto creará:
- `data/processed/datos_modelo.pkl`
- `data/processed/medellin_poblado_nodos.pkl`
- `data/processed/medellin_poblado_aristas.pkl`

### Paso 3: Ejecutar la Aplicación

```bash
python ejecutar_app.py
```

O directamente:

```bash
streamlit run gui/app.py
```

**¡Eso es todo!** La aplicación se abrirá en: `http://localhost:8501`

---

## 📖 Guía de Uso Detallada

### Al Abrir la Aplicación

1. **Pantalla de carga** (2-3 segundos):
   ```
   🔄 Cargando datos iniciales...
   ```

2. **Header con métricas** (visible inmediatamente):
   ```
   🚑 Sistema de Optimización de Rutas de Ambulancias
   📍 Medellín, Colombia
   
   ✅ Operativo | 347 Nodos | 891 Aristas | 4 Emergencias
   ```

3. **Sidebar muestra**:
   ```
   ⚙️ Panel de Control
   
   📂 Estado de Datos
     ✅ Datos cargados correctamente
   
   🚨 Emergencias
     [🎲 Generar Nuevas Emergencias]
   
   👁️ Visualización
     ☐ Colorear vías por capacidad
     ☐ Mostrar nodos del grafo
   ```

4. **Tabs disponibles**:
   - 🏠 Inicio
   - 🗺️ Mapa Interactivo ← **Ya funciona al abrir!**
   - 📊 Datos y Estadísticas
   - 🚑 Emergencias

### Explorar el Mapa

1. Ve al tab **"🗺️ Mapa Interactivo"**
2. Verás:
   - 🔵 Punto azul: Origen (Clínica)
   - 🟢🟠🔴 Marcadores: Emergencias según severidad
   - Líneas azules: Red vial (1km² alrededor de la clínica)
3. **Interacción**:
   - Click en marcadores → Ver información detallada
   - Scroll → Zoom in/out
   - Arrastrar → Mover mapa

### Generar Nuevas Emergencias

1. En el sidebar → Click **"🎲 Generar Nuevas Emergencias"**
2. Verás: "✅ X emergencias generadas"
3. El mapa se actualiza automáticamente con nuevos marcadores
4. Los tabs de Datos y Emergencias muestran la nueva información

### Opciones de Visualización

En el sidebar → **"👁️ Visualización"**:

#### ☑️ Colorear vías por capacidad:
- 🔴 Rojo: < 40 km/h (baja capacidad)
- 🟠 Naranja: 40-70 km/h (media capacidad)
- 🟢 Verde: > 70 km/h (alta capacidad)

#### ☑️ Mostrar nodos del grafo:
- Muestra los nodos (intersecciones) como puntos grises

### Ver Estadísticas

Tab **"📊 Datos y Estadísticas"**:
- Métricas generales: Nodos, aristas, longitud total, capacidad promedio
- Histograma de capacidades: Distribución de velocidades máximas
- Histograma de tiempos: Distribución de tiempos de viaje
- Tabla de aristas: Datos tabulares con opción de descarga

### Ver Emergencias

Tab **"🚑 Emergencias"**:
- Resumen: Contador por severidad (leve/media/crítica)
- Gráfico de barras: Distribución de emergencias
- Tabla detallada: Todos los datos de cada emergencia
- Descarga CSV: Exporta los datos

---

## 🎨 Estructura Técnica

### Arquitectura Modular

```
gui/
├── app.py                 # Aplicación principal (orquestador)
├── components/
│   ├── sidebar.py        # Panel lateral con controles
│   ├── map_display.py    # Funciones de visualización de mapas
│   └── results_panel.py  # Gráficos y tablas de estadísticas
├── assets/
│   └── style.css         # Estilos personalizados (opcional)
└── README.md             # Esta documentación
```

### Responsabilidades

#### `app.py` - Aplicación Principal
- Configuración de la página
- Carga automática de datos (con caché)
- Inicialización de session_state
- Estructura de tabs
- Llama a los componentes

#### `sidebar.py` - Panel Lateral
- Botón: Recargar datos (opcional)
- Botón: Generar emergencias
- Checkbox: Opciones de visualización
- Métricas: Información del sistema
- Expander: Parámetros configurados

#### `map_display.py` - Visualización de Mapas
- `crear_mapa_base()`: Mapa Folium
- `agregar_grafo_al_mapa()`: Red vial
- `agregar_nodos_al_mapa()`: Nodos del grafo
- `agregar_origen_al_mapa()`: Clínica (punto azul)
- `agregar_emergencias_al_mapa()`: Emergencias coloreadas
- `mostrar_mapa_streamlit()`: Renderizar en Streamlit
- `mostrar_leyenda_mapa()`: Leyenda explicativa

#### `results_panel.py` - Estadísticas y Resultados
- `mostrar_metricas_generales()`: Cards con KPIs
- `mostrar_estadisticas_capacidades()`: Histograma + stats
- `mostrar_estadisticas_tiempos()`: Histograma + stats
- `mostrar_tabla_aristas()`: Tabla de datos
- `mostrar_resumen_emergencias()`: Métricas de emergencias
- `mostrar_tabla_emergencias()`: Tabla completa con descarga
- `graficar_emergencias_por_severidad()`: Gráfico de barras

---

## 🔧 Funciones Principales

### Carga de Datos

```python
@st.cache_data
def cargar_datos_modelo():
    """Carga los datos procesados del modelo"""
    # Carga desde data/processed/datos_modelo.pkl
```

```python
@st.cache_data
def cargar_geodataframes():
    """Carga los GeoDataFrames de nodos y aristas"""
    # Carga desde data/processed/*.pkl
```

### Visualización de Mapas

```python
def crear_mapa_base(centro_lat, centro_lon, zoom=15):
    """Crea el mapa base de Folium"""
```

```python
def agregar_grafo_al_mapa(mapa, gdf_aristas, mostrar_capacidades=False):
    """Agrega las calles del grafo al mapa"""
```

```python
def agregar_origen_al_mapa(mapa, lat, lon, nombre):
    """Agrega el punto de origen (Clínica) al mapa"""
```

```python
def agregar_emergencias_al_mapa(mapa, emergencias):
    """Agrega las emergencias al mapa con colores"""
```

---

## 📊 Datos Visualizados

### Del Grafo
- Número de nodos y aristas (~347 nodos, ~891 aristas)
- Longitud total de vías
- Capacidad promedio de vías (30-100 km/h)
- Tiempos de viaje por arista (calculados)
- Área: 1 km² alrededor de la Clínica Medellín

### De Emergencias
- ID único
- Severidad (leve/media/crítica)
- Velocidad requerida (según severidad)
- Ambulancia asignada (relación 1:1)
- Nodo destino
- Coordenadas (latitud, longitud)
- Origen común: Clínica Medellín - Sede El Poblado

---

## 🎯 Características Técnicas

### Sistema de Caché

La aplicación usa `@st.cache_data` para:
- ✅ Cargar datos solo una vez
- ✅ Mejorar el rendimiento
- ✅ Evitar recargas innecesarias

**Rendimiento:**
- Primera carga: ~2-3 segundos
- Siguientes interacciones: Instantáneas (caché)
- Cambio de tab: Sin recarga
- Generación emergencias: < 1 segundo

### Session State

Variables persistentes entre interacciones:
- `inicializado`: Flag de carga única
- `datos_cargados`: Boolean
- `datos_modelo`: Dict con el modelo completo
- `gdf_nodos`: GeoDataFrame de nodos
- `gdf_aristas`: GeoDataFrame de aristas
- `emergencias_generadas`: Lista de emergencias
- `mostrar_capacidades`: Boolean para visualización

### Flujo de Carga Automática

```
Usuario abre la aplicación
    ↓
main() ejecuta inicializar_session_state()
    ↓
¿st.session_state.inicializado == False?
    ↓ Sí
Muestra spinner "Cargando datos..."
    ↓
cargar_datos_modelo() (con @st.cache_data)
    ↓
cargar_geodataframes() (con @st.cache_data)
    ↓
¿Datos cargados exitosamente?
    ↓ Sí
st.session_state.datos_cargados = True
st.session_state.inicializado = True
    ↓
Interfaz lista con todos los datos
```

---

## 🔄 Comandos Útiles

### Ejecutar la Aplicación
```bash
python ejecutar_app.py
```

### Detener la Aplicación
```
Ctrl + C
```

### Reiniciar la Aplicación
```
1. Ctrl + C (detener)
2. python ejecutar_app.py (reiniciar)
```

### Limpiar Caché
```
En el navegador: Presiona R
O: Click en el menú (⋮) → Clear cache
```

### Recargar Datos
Si modificas los datos y quieres actualizar:

**Opción 1**: En el navegador → Presiona **R**

**Opción 2**: Sidebar → Click **"🔄 Recargar Datos"**

**Opción 3**: Regenera y recarga:
```bash
python preparar_datos.py
# En el navegador: Presiona R
```

---

## 🐛 Solución de Problemas

### Error: "Sistema no operativo" o "No se encontraron datos"
**Causa**: No hay datos en `data/processed/`

**Solución**:
```bash
python preparar_datos.py
# Recarga navegador (R)
```

### Error: "No module named 'streamlit_folium'"
**Solución**: 
```bash
pip install streamlit-folium
```

### Error: "ImportError: scikit-learn"
**Solución**:
```bash
pip install scikit-learn
```

### Error: "No se puede cargar el mapa"
**Causa**: GeoDataFrames no se cargaron

**Solución**:
```bash
# Verificar archivos
ls data/processed/

# Regenerar si faltan
python preparar_datos.py
```

### El mapa está vacío
**Causa**: Datos cargados pero sin emergencias

**Solución**:
En la app: Sidebar → "🎲 Generar Nuevas Emergencias"

### El mapa no se actualiza
**Solución**: Presiona **R** en el navegador

### La aplicación no se abre
**Solución**: Verifica el puerto 8501 esté libre

---

## 🎨 Personalización

### Colores

Los colores están definidos en el código:
- **Emergencia Leve**: Verde (`green`)
- **Emergencia Media**: Naranja (`orange`)
- **Emergencia Crítica**: Rojo (`red`)
- **Origen**: Azul (`blue`)
- **Vías**: Azul (`#3388ff`)
- **Capacidad Baja**: Rojo (`red`)
- **Capacidad Media**: Naranja (`orange`)
- **Capacidad Alta**: Verde (`green`)

### Estilos CSS

Puedes personalizar los estilos editando:

```python
st.markdown("""
<style>
    /* Tus estilos personalizados aquí */
</style>
""", unsafe_allow_html=True)
```

---

## ✅ Checklist de Funcionamiento

Antes de ejecutar la GUI, verifica:

- [ ] ✅ Ejecutaste `python preparar_datos.py`
- [ ] ✅ Existe `data/processed/datos_modelo.pkl`
- [ ] ✅ Existe `data/processed/medellin_poblado_nodos.pkl`
- [ ] ✅ Existe `data/processed/medellin_poblado_aristas.pkl`
- [ ] ✅ Instalaste `pip install streamlit-folium scikit-learn`

Si todo está ✅:

```bash
python ejecutar_app.py
```

---

## 💡 Consejos y Mejores Prácticas

1. **Primero carga los datos** → Ejecuta `preparar_datos.py` antes
2. **Usa tooltips** → Hover sobre elementos del mapa para información
3. **Prueba zoom** → Acércate para ver detalles de calles
4. **Genera varias veces** → Cada ejecución genera escenarios diferentes
5. **Compara tabs** → Visualización vs. datos tabulares
6. **Exporta datos** → Usa botones de descarga CSV
7. **Experimenta** → Genera nuevas emergencias y observa cambios

---

## 🎯 Casos de Uso

### Caso 1: Usuario Final (Producción)
```
1. Ejecuta: python ejecutar_app.py
2. Aplicación abre en navegador
3. Datos ya cargados automáticamente
4. Explora mapas y estadísticas
5. Genera nuevas emergencias si quiere
```

### Caso 2: Desarrollador (Desarrollo)
```
1. Modifica datos: python preparar_datos.py
2. Recarga aplicación: Ctrl+R en navegador
   O click en "🔄 Recargar Datos" en sidebar
3. Cambios reflejados inmediatamente
```

### Caso 3: Análisis de Escenarios
```
1. Cargar aplicación
2. Generar emergencias múltiples veces
3. Comparar distribuciones
4. Exportar datos para análisis externo
```

---

## ⚠️ Nota Importante

Esta es una aplicación de **visualización de datos y exploración**. Para ejecutar el modelo de optimización completo, se necesitará implementar el componente de optimización en `src/models/optimization_model.py`.

---

## 📚 Referencias

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium)
- [Plotly Documentation](https://plotly.com/python/)
- [OSMnx Documentation](https://osmnx.readthedocs.io/)

---

## 🚀 Próximas Características

- [ ] Filtros de severidad en el mapa
- [ ] Animaciones de rutas
- [ ] Exportación de reportes PDF
- [ ] Comparación de escenarios
- [ ] Estadísticas en tiempo real
- [ ] Integración con modelo de optimización
- [ ] Visualización de rutas óptimas

---

## 🎉 Características Destacadas

### ✨ Carga Automática
Los datos se cargan **automáticamente** al abrir la aplicación. No más clics manuales.

### 🗺️ Mapa Interactivo Completo
- Red vial real de OSM
- Marcadores personalizados
- Información en tooltips
- Zoom y navegación fluida

### 📊 Estadísticas en Tiempo Real
- Gráficos con Plotly
- Métricas destacadas
- Tablas descargables

### 🎲 Generación Dinámica
- Genera nuevas emergencias al instante
- Sin recargar toda la app

### 🎨 Interfaz Moderna
- Diseño limpio
- Colores informativos
- Tabs organizados
- Sidebar funcional

### ⚡ Alto Rendimiento
- Caché de Streamlit
- Carga única
- Interacciones instantáneas

---

**Desarrollado para el proyecto de Optimización de Rutas de Ambulancias - Medellín, Colombia** 🇨🇴
