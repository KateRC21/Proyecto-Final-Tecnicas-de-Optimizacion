# 🚑 Sistema de Optimización de Rutas de Ambulancias

Sistema de optimización de rutas para el despacho de ambulancias en Medellín, Colombia.

## 📑 Tabla de Contenidos

| Sección | Descripción |
|---------|-------------|
| [📋 Descripción del Proyecto](#-descripción-del-proyecto) | Visión general y estado del proyecto |
| [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas) | Stack tecnológico |
| [🚀 Inicio Rápido](#-inicio-rápido) | Instalación y ejecución en 3 pasos |
| [📁 Estructura del Proyecto](#-estructura-del-proyecto) | Organización de archivos y módulos |
| [🎯 Funcionalidades](#-funcionalidades) | Características del sistema |
| [⚙️ Configuración del Sistema](#️-configuración-del-sistema) | Parámetros y costos |
| [📐 Formulación Matemática](#-formulación-matemática-del-modelo) | Modelo matemático completo |
| [🔧 Procedimiento de Solución](#-procedimiento-de-solución) | Fases de resolución del problema |
| [📊 Resultados y Escenarios](#-resultados-y-escenarios-de-prueba) | Escenarios de prueba y análisis |
| [📚 Documentación](#-documentación) | Guías de usuario y técnicas |
| [🔧 Solución de Problemas](#-solución-de-problemas) | Errores comunes y soluciones |
| [👥 Autores](#-autores) | Información del proyecto |

---

## 📋 Descripción del Proyecto

El sistema optimiza la asignación de recursos de emergencia considerando:
- **Prioridades clínicas:** Leve, media, grave
- **Costos operativos:** Diferenciados por tipo de ambulancia
- **Capacidades viales:** Velocidades máximas en cada calle
- **Requerimientos de velocidad:** Por cada flujo de emergencia
- **Red vial real:** Obtenida de OpenStreetMap (Medellín)

### 🎯 **Estado del Proyecto: COMPLETADO Y FUNCIONAL** ✅

- ✅ Sistema de carga y procesamiento de datos
- ✅ Modelo de optimización Multi-Commodity Flow con PuLP
- ✅ Interfaz gráfica completa con Streamlit
- ✅ Visualización de rutas óptimas en mapas interactivos
- ✅ Análisis de costos y utilización de vías
- ✅ Configuración flexible de parámetros

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **OSMnx**: Obtención de redes viales reales desde OpenStreetMap
- **PuLP/Gurobi**: Solvers de optimización matemática
- **Streamlit**: Interfaz web interactiva
- **Folium**: Mapas interactivos
- **Plotly**: Visualización de datos
- **NetworkX**: Manipulación y análisis de grafos
- **GeoPandas**: Procesamiento de datos geoespaciales

## 🚀 Inicio Rápido

### Opción A: Ejecución Local

#### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 2: Generar Datos (Solo primera vez)
```bash
python preparar_datos.py
```
Esto descarga el mapa de Medellín y genera datos procesados (~2-5 min la primera vez).

#### Paso 3: Ejecutar la Aplicación
```bash
python ejecutar_app.py
```

O directamente:
```bash
streamlit run gui/app.py
```

**¡Listo!** La aplicación se abrirá automáticamente en tu navegador: `http://localhost:8501`

### Opción B: Despliegue en la Nube (Streamlit Cloud)

Para desplegar esta aplicación en Streamlit Cloud y hacerla accesible desde internet:

📖 **Lee la guía completa:** [`DESPLIEGUE_STREAMLIT.md`](DESPLIEGUE_STREAMLIT.md)

**Resumen rápido:**
1. Sube tu código a GitHub
2. Conecta con Streamlit Cloud
3. ¡Tu app estará en línea en minutos!

🌐 **Sin instalación** - Sin configuración de servidores - **100% Gratuito**

### ✨ Características Principales
- ✅ **Carga automática de datos** al abrir la aplicación
- 🗺️ **Mapa interactivo** de Medellín con emergencias y rutas optimizadas
- 🎯 **Modelo de optimización** Multi-Commodity Flow (PuLP)
- 📊 **Estadísticas y análisis** en tiempo real
- 🎲 **Generación dinámica de escenarios** de emergencias
- 💰 **Costos configurables** desde la interfaz
- 🚑 **Visualización de rutas óptimas** con costos y métricas detalladas

## 📁 Estructura del Proyecto

```
proyecto_optimizacion_ambulancias/
├── config/              # Configuraciones y parámetros
│   ├── parametros.py   # Velocidades, capacidades, área de estudio
│   ├── costos.py       # Costos operacionales por tipo de ambulancia
│   ├── README.md       # Documentación del módulo
│   └── COSTOS_GUIA.md  # Guía detallada de costos
│
├── src/                 # Código fuente
│   ├── data/           # Carga y procesamiento de datos
│   │   ├── osm_loader.py        # Descarga de OSM con caché
│   │   └── graph_processor.py   # Procesamiento y enriquecimiento
│   ├── models/         # Modelos de optimización
│   │   ├── optimization_model.py  # Modelo Multi-Commodity Flow (PuLP)
│   │   └── constraints.py         # Documentación de restricciones
│   └── utils/          # Utilidades generales
│       ├── validators.py   # Validación de datos
│       └── calculations.py # Cálculos auxiliares
│
├── gui/                # Interfaz gráfica (Streamlit)
│   ├── app.py          # Aplicación principal
│   ├── components/     # Componentes modulares
│   │   ├── sidebar.py       # Panel de control
│   │   ├── map_display.py   # Visualización de mapas
│   │   └── results_panel.py # Gráficos y tablas
│   └── README.md       # Guía completa de usuario
│
├── data/               # Datos procesados
│   ├── graphs/         # Grafos de OSMnx (caché)
│   └── processed/      # Datos listos para optimización
│
├── docs/               # Documentación técnica
│   └── metodologia.md  # Formulación matemática detallada
│
├── notebooks/          # Jupyter notebooks (análisis exploratorio)
├── cache/              # Caché de OSMnx
│
├── ejecutar_app.py     # Script para iniciar la aplicación
├── preparar_datos.py   # Script para generar datos
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
```

## 🎯 Funcionalidades

### Sistema de Datos
- **Red vial real:** Descarga automática desde OpenStreetMap
- **Área de estudio:** 1 km² alrededor de Clínica Medellín (El Poblado)
- **Generación de escenarios:** 3-5 emergencias aleatorias con diferentes prioridades
- **Asignación de capacidades:** Velocidades máximas (30-100 km/h) para cada vía
- **Sistema de caché:** Evita descargas repetidas

### Interfaz Gráfica
- **Carga automática:** Datos listos al abrir la aplicación
- **Mapa interactivo:** Visualización con Folium de calles y emergencias
- **Marcadores coloreados:** Verde (leve), naranja (media), rojo (crítica)
- **Estadísticas:** Gráficos con distribución de capacidades y tiempos
- **Exportación:** Descarga de datos en CSV

### Configuración
- **Costos editables:** Ajusta costos operacionales desde la GUI
- **Parámetros flexibles:** Velocidades, capacidades, número de emergencias
- **Valores por defecto:** Calculados para Medellín, Colombia

## ⚙️ Configuración del Sistema

### Velocidades y Capacidades
- **Velocidades requeridas:** 30-90 km/h (según severidad)
  - Leve: 30-50 km/h
  - Media: 50-70 km/h
  - Grave: 70-90 km/h
- **Capacidades de vías:** 30-100 km/h (asignadas aleatoriamente, configurables hasta 1000)

### Costos Operacionales (Medellín, COP)
| Tipo | Uso | Costo Fijo | Costo/km |
|------|-----|------------|----------|
| TAB | Leve | $35.000 | $5.585 |
| TAM | Media | $60.000 | $10.534 |
| TAM Grave | Grave | $85.000 | $20.396 |

### Datos de Entrada
- **Origen único:** Clínica Medellín - Sede El Poblado
- **Emergencias:** 3-5 generadas aleatoriamente (solo nodos internos bien conectados)
- **Relación:** 1 ambulancia por emergencia (1:1)

## 📐 Formulación Matemática del Modelo

### Tipo de Modelo
**Multi-Commodity Flow Problem** con restricciones de capacidad

Cada emergencia representa un "commodity" (flujo) independiente que debe viajar desde un origen común (Clínica) hasta su destino específico.

### Conjuntos

- **V**: Conjunto de nodos (intersecciones de calles) - típicamente ~300 nodos
- **E**: Conjunto de aristas dirigidas (calles) - típicamente ~600 aristas
- **K**: Conjunto de flujos/emergencias {1, 2, ..., k} - típicamente 3-5 emergencias

Donde:
- **V_o**: Nodo de origen (Clínica Medellín) - singleton
- **V_d**: Nodos destino (ubicación de emergencias) ⊂ V
- **V_i**: Nodos intermedios = V \ (V_o ∪ V_d)

### Parámetros

- **c_ij**: Capacidad (velocidad máxima) de la arista (i,j) en km/h
- **r_k**: Velocidad requerida por la emergencia k en km/h (según severidad)
- **d_ij**: Distancia de la arista (i,j) en metros
- **CF_t**: Costo fijo de activación de ambulancia tipo t (COP)
- **CK_t**: Costo por kilómetro de ambulancia tipo t (COP/km)
- **tipo_k**: Tipo de ambulancia asignada a emergencia k
- **dest_k**: Nodo destino de la emergencia k

### Variables de Decisión

**x_ijk ∈ {0, 1}** para todo k ∈ K, (i,j) ∈ E

Donde x_ijk = 1 si el flujo k (ambulancia k) utiliza la arista (i,j), 0 en caso contrario.

**Total de variables:** |K| × |E| (típicamente 3-5 × 600 = 1,800 - 3,000 variables binarias)

### Función Objetivo

**MINIMIZAR:**

```
Z = Σ_{k∈K} CF_{tipo_k} + Σ_{k∈K} Σ_{(i,j)∈E} (d_ij/1000) × CK_{tipo_k} × x_ijk
```

Donde:
- Primer término: Suma de costos fijos de activación
- Segundo término: Suma de costos variables por distancia recorrida

### Restricciones

#### 1. Conservación de Flujo

Para cada flujo k y cada nodo v:

**a) Nodo Origen (v = o):**
```
Σ_{j:(o,j)∈E} x_ojk - Σ_{i:(i,o)∈E} x_iok = 1
```
El flujo k SALE del origen (genera 1 unidad)

**b) Nodos Intermedios (v ∈ V_i):**
```
Σ_{i:(i,v)∈E} x_ivk - Σ_{j:(v,j)∈E} x_vjk = 0
```
Lo que entra = lo que sale (conservación)

**c) Nodo Destino (v = dest_k):**
```
Σ_{i:(i,v)∈E} x_ivk - Σ_{j:(v,j)∈E} x_vjk = -1
```
El flujo k LLEGA a su destino (absorbe 1 unidad)

**Total restricciones de flujo:** |K| × |V| (típicamente 3-5 × 300 = 900 - 1,500 restricciones)

#### 2. Capacidad de Vías

Para cada arista (i,j):

```
Σ_{k∈K} r_k × x_ijk ≤ c_ij
```

La suma de velocidades requeridas por todos los flujos que usan la arista no puede exceder su capacidad.

**Total restricciones de capacidad:** |E| (típicamente ~600 restricciones)

#### 3. Integralidad

```
x_ijk ∈ {0, 1}  ∀k ∈ K, ∀(i,j) ∈ E
```

Las variables son binarias (ruta usada o no).

---

## 🔧 Procedimiento de Solución

### Fase 1: Preparación de Datos

1. **Descarga de red vial:**
   ```bash
   python preparar_datos.py
   ```
   - Descarga grafo de OpenStreetMap (área de 1km² en El Poblado)
   - Simplifica grafo a DiGraph (elimina aristas paralelas redundantes)
   - Asigna capacidades aleatorias a cada arista: c_ij ∈ [C_MIN, C_MAX]
   - Calcula tiempos de viaje por arista

2. **Identificación del nodo origen:**
   - Encuentra el nodo más cercano a las coordenadas de la Clínica Medellín
   - Marca como nodo de origen para todos los flujos

3. **Generación de emergencias:**
   - Genera 3-5 emergencias aleatorias con severidades equiprobables
   - Asigna velocidades requeridas según severidad:
     - Leve: r_k ∈ [30, 50] km/h
     - Media: r_k ∈ [50, 70] km/h
     - Grave: r_k ∈ [70, 90] km/h
   - Asigna cada emergencia a un **nodo interno** (≥3 entradas y ≥3 salidas)
   - Esto evita nodos de borde mal conectados

### Fase 2: Construcción del Modelo

1. **Inicialización (PuLP):**
   - Crea problema de minimización
   - Simplifica MultiDiGraph → DiGraph automáticamente
   - Define variables de decisión x[i,j,k] (binarias)

2. **Función objetivo:**
   - Calcula costos fijos totales (Σ CF_tipo_k)
   - Define costos variables (Σ Σ distancia × costo_km × x_ijk)
   - Minimiza la suma de ambos

3. **Restricciones:**
   - Agrega |K| × |V| restricciones de conservación de flujo
   - Agrega |E| restricciones de capacidad de vías
   - Todas las variables se declaran binarias

### Fase 3: Resolución

1. **Configuración del solver:**
   - Solver: CBC (incluido en PuLP)
   - Tiempo límite: 120 segundos
   - Gap de optimalidad: 1%

2. **Ejecución:**
   - El solver busca la solución óptima
   - Explora el espacio de soluciones mediante Branch & Bound
   - Típicamente resuelve en 2-10 segundos

3. **Estados posibles:**
   - **Optimal:** Solución óptima encontrada ✅
   - **Infeasible:** No existe solución factible (parámetros incompatibles)
   - **Unbounded:** Problema mal formulado (raro)

### Fase 4: Extracción de Resultados

1. **Reconstrucción de rutas:**
   - Para cada flujo k, sigue las variables x[i,j,k] = 1
   - Construye secuencia de nodos desde origen hasta destino
   - Valida que no haya ciclos

2. **Cálculo de métricas:**
   - Distancia total por ruta (suma de d_ij)
   - Costos por emergencia (fijo + variable)
   - Uso de cada arista (cuántos flujos la comparten)
   - Utilización: (Σ r_k × x_ijk) / c_ij

3. **Visualización:**
   - Dibuja rutas en mapa interactivo (Folium)
   - Genera gráficos de costos y distancias (Plotly)
   - Muestra tablas detalladas con métricas

---

## 📊 Resultados y Escenarios de Prueba

### Escenario 1

**Parámetros de configuración:**
- Número de emergencias: 5
- Velocidades requeridas: R_MIN = 30 km/h, R_MAX = 62 km/h
- Capacidades de vías: C_MIN = 250 km/h, C_MAX = 700 km/h
- Costos operacionales: Valores por defecto
  - TAB (Leve): $35,000 + $5,585/km
  - TAM (Media): $60,000 + $10,534/km
  - TAM Grave (Grave): $85,000 + $20,396/km

**Resultados obtenidos:**
- ✅ **Estado de la solución:** Optimal
- 💰 **Costo total:** $350,691 COP
- ⏱️ **Tiempo de resolución:** 0.2 s
- 📏 **Distancia total recorrida:** 4.3 km

**Distribución de emergencias:**
- 🟢 Leves: 1
- 🟠 Medias: 3
- 🔴 Graves: 1

#### Información de Emergencias

![Tabla de emergencias - Escenario 1](tests_images\EmergenciasRuta1.png)

*Captura de pantalla del tab "🚑 Emergencias" mostrando el detalle de cada emergencia generada*

#### Mapa de Rutas Optimizadas

![Mapa de rutas - Escenario 1](tests_images\MapaRuta1.png)

*Captura de pantalla del tab "🗺️ Mapa Interactivo" mostrando las rutas óptimas calculadas*


---

### Escenario 2

**Parámetros de configuración:**
- Número de emergencias: 5
- Velocidades requeridas: R_MIN = 30 km/h, R_MAX = 90 km/h
- Capacidades de vías: C_MIN = 250 km/h, C_MAX = 550 km/h
- Costos operacionales: 
  - TAB (Leve): $35,000 + $5,585/km
  - TAM (Media): $60,000 + $10,534/km
  - TAM Grave (Grave): $70,000 + $24,900/km

**Resultados obtenidos:**
- **Estado de la solución:** Optimal
- 💰 **Costo total:** $348.809 COP
- ⏱️ **Tiempo de resolución:** 0.2 segundos
- 📏 **Distancia total recorrida:** 5 km

**Distribución de emergencias:**
- 🟢 Leves: 2
- 🟠 Medias: 1
- 🔴 Graves: 2

#### Información de Emergencias

![Tabla de emergencias - Escenario 2](tests_images\EmergenciasRuta2.png)

*Captura de pantalla del tab "🚑 Emergencias" mostrando el detalle de cada emergencia generada*

#### Mapa de Rutas Optimizadas

![Mapa de rutas - Escenario 2](tests_images\MapaRuta2.png)

*Captura de pantalla del tab "🗺️ Mapa Interactivo" mostrando las rutas óptimas calculadas*



---

### Escenario 3: 

**Parámetros de configuración:**
- Número de emergencias: 4
- Velocidades requeridas: R_MIN = 30 km/h, R_MAX = 90 km/h
- Capacidades de vías: C_MIN = 50 km/h, C_MAX = 250 km/h
- Costos operacionales: 
  - TAB (Leve): $35,000 + $6,500/km
  - TAM (Media): $60,000 + $10,000/km
  - TAM Grave (Grave): $70,000 + $24,900/km

**Resultados obtenidos:**
- **Estado de la solución:** Infeasible
- 💰 **Costo total:** N/A
- ⏱️ **Tiempo de resolución:** N/A
- 📏 **Distancia total recorrida:** N/A

**Distribución de emergencias:**
- 🟢 Leves: 2
- 🟠 Medias: 1
- 🔴 Graves: 1

#### Información de Emergencias

![Tabla de emergencias - Escenario 3](tests_images\EmergenciasRuta3.png)

*Captura de pantalla del tab "🚑 Emergencias" mostrando el detalle de cada emergencia generada*

#### Mapa de Rutas Optimizadas

![Mapa de rutas - Escenario 3](tests_images\MapaRuta3.png)

*Captura de pantalla del tab "🗺️ Mapa Interactivo" mostrando las rutas óptimas calculadas*

**Análisis:**
Al ser un problema que no se puede solucionar, se le muestran las siguientes sugerencias al usuario.

![Sugerencias cuando problema es infeasible](tests_images\SugerenciasRuta3.png)

---

## 📚 Documentación

### 🎯 Guías de Usuario
| Documento | Descripción | Para quién |
|-----------|-------------|------------|
| **`README.md`** | Este archivo - Información general | Todos |
| **`gui/README.md`** | Guía completa de la interfaz gráfica | Usuarios finales |

### 🔧 Documentación Técnica
| Documento | Descripción | Para quién |
|-----------|-------------|------------|
| **`docs/metodologia.md`** | Formulación matemática del modelo | Desarrolladores/Investigadores |
| **`config/COSTOS_GUIA.md`** | Guía completa de costos (ejemplos y uso) | Desarrolladores |
| **`config/README.md`** | Documentación del módulo de configuración | Desarrolladores |

### 📖 Guía Rápida de Lectura

**Si eres usuario final:**
1. Lee este README para empezar
2. Consulta `gui/README.md` para usar la interfaz

**Si eres desarrollador:**
1. Lee este README para entender el sistema completo
2. Lee `docs/metodologia.md` para la formulación matemática
3. Consulta `config/COSTOS_GUIA.md` para trabajar con costos
4. Revisa `config/README.md` para documentación del módulo de configuración

## 🔧 Solución de Problemas

### Error: "No se encontraron datos"
```bash
python preparar_datos.py
# Luego recarga el navegador (R)
```

### Error: Módulo no encontrado
```bash
pip install -r requirements.txt
```

### La aplicación no se abre
Verifica que el puerto 8501 esté libre o usa:
```bash
streamlit run gui/app.py --server.port 8502
```

### El mapa está vacío
En la aplicación: Sidebar → "🎲 Generar Nuevas Emergencias"

---

## 👥 Autores

- Katheryn Ramírez Chimá
 Como trabajo final de la materia Técnicas de Optimización - Quinto Semestre
 en la Universidad Pontificia Bolivariana -  Medellín, Colombia

## 📄 Licencia

Este proyecto es de uso académico.

---


**Desarrollado para el análisis y optimización de sistemas de emergencias médicas en Medellín, Colombia** 🇨🇴

