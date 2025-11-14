# Metodología del Proyecto

## 1. Descripción del Problema

El sistema de despacho de ambulancias debe optimizar la asignación de recursos de emergencia considerando:

- **Prioridades clínicas**: Leve, media, crítica
- **Costos operativos**: Diferentes por tipo de ambulancia
- **Capacidades viales**: Velocidades máximas en cada calle
- **Velocidades requeridas**: Por cada flujo de emergencia

## 2. Formulación Matemática

### 2.1 Conjuntos

- \( N \): Conjunto de nodos (intersecciones) en el grafo
- \( A \): Conjunto de aristas (calles) en el grafo
- \( K \): Conjunto de emergencias
- \( H \): Conjunto de hospitales (orígenes)
- \( T \): Conjunto de tipos de ambulancia {básica, intermedia, crítica}

### 2.2 Parámetros

- \( c_{ij} \): Capacidad (velocidad máxima) de la arista \((i,j)\) [km/h]
- \( l_{ij} \): Longitud de la arista \((i,j)\) [km]
- \( r_k \): Velocidad requerida para la emergencia \(k\) [km/h]
- \( p_k \): Prioridad de la emergencia \(k\) (1=leve, 2=media, 3=crítica)
- \( \text{cost}_t \): Costo operativo del tipo de ambulancia \(t\)
- \( o_k \): Nodo origen (hospital) de la emergencia \(k\)
- \( d_k \): Nodo destino (ubicación emergencia) de la emergencia \(k\)

### 2.3 Variables de Decisión

- \( x_{ijk} \in \{0,1\} \): 1 si el flujo \(k\) usa la arista \((i,j)\), 0 en caso contrario
- \( y_{kt} \in \{0,1\} \): 1 si la emergencia \(k\) es atendida por ambulancia tipo \(t\)
- \( t_k \geq 0 \): Tiempo de respuesta para la emergencia \(k\) [minutos]
- \( v_{ijk} \geq 0 \): Velocidad del flujo \(k\) en la arista \((i,j)\) [km/h]

### 2.4 Función Objetivo

Minimizar:

\[
Z = w_1 \sum_{k \in K} p_k \cdot t_k + w_2 \sum_{k \in K} \sum_{t \in T} \text{cost}_t \cdot y_{kt} \cdot \text{dist}_k
\]

Donde:
- \( w_1, w_2 \): Pesos para tiempo y costo
- \( \text{dist}_k \): Distancia total recorrida por el flujo \(k\)

### 2.5 Restricciones

#### Conservación de Flujo
Para cada emergencia \(k\) y nodo \(i\):

\[
\sum_{j:(i,j) \in A} x_{ijk} - \sum_{j:(j,i) \in A} x_{jik} = 
\begin{cases}
1 & \text{si } i = o_k \\
-1 & \text{si } i = d_k \\
0 & \text{en otro caso}
\end{cases}
\]

#### Asignación Única de Ambulancia
Cada emergencia debe ser atendida por exactamente una ambulancia:

\[
\sum_{t \in T} y_{kt} = 1 \quad \forall k \in K
\]

#### Tipo Apropiado de Ambulancia
La ambulancia asignada debe ser adecuada para la prioridad:

\[
y_{k,\text{básica}} = 0 \quad \text{si } p_k \in \{\text{media}, \text{crítica}\}
\]

\[
y_{k,\text{intermedia}} = 0 \quad \text{si } p_k = \text{crítica}
\]

#### Respeto de Capacidades
La velocidad en cada arista no debe exceder la capacidad:

\[
v_{ijk} \leq c_{ij} \quad \forall (i,j) \in A, k \in K
\]

#### Velocidad Mínima Requerida
Cada flujo debe mantener al menos su velocidad requerida:

\[
v_{ijk} \geq r_k \cdot x_{ijk} \quad \forall (i,j) \in A, k \in K
\]

#### Cálculo del Tiempo
El tiempo de respuesta es la suma de tiempos en cada arista:

\[
t_k = \sum_{(i,j) \in A} \frac{l_{ij}}{v_{ijk}} \cdot x_{ijk} \quad \forall k \in K
\]

## 3. Algoritmo de Solución

1. **Preprocesamiento**:
   - Cargar grafo de Medellín con OSMnx
   - Asignar capacidades aleatorias a las vías
   - Generar emergencias con ubicaciones y prioridades

2. **Construcción del Modelo**:
   - Definir variables de decisión
   - Construir función objetivo
   - Agregar todas las restricciones

3. **Resolución**:
   - Usar solver (PuLP con CBC o Gurobi)
   - Establecer tiempo límite y gap de optimalidad
   - Obtener solución

4. **Postprocesamiento**:
   - Extraer rutas de las variables binarias
   - Calcular métricas de rendimiento
   - Generar visualizaciones

## 4. Herramientas Utilizadas

- **OSMnx**: Descarga de mapas reales
- **NetworkX**: Manipulación de grafos
- **PuLP**: Modelado y optimización lineal
- **Streamlit**: Interfaz web interactiva
- **Folium**: Visualización de mapas
- **Plotly**: Gráficos interactivos

## 5. Validación

- Tests unitarios para cada componente
- Verificación manual de rutas pequeñas
- Validación de restricciones en la solución
- Análisis de sensibilidad de parámetros

## 6. Limitaciones

- Las capacidades son simplificadas (solo velocidad)
- No se considera congestión dinámica en tiempo real
- Modelo determinístico (sin incertidumbre)
- Computacionalmente costoso para grafos muy grandes

## 7. Trabajo Futuro

- Incorporar incertidumbre en tiempos de viaje
- Modelo dinámico con reoptimización
- Considerar múltiples hospitales como origen
- Incluir restricciones de disponibilidad de personal
- Validación con datos reales de emergencias

