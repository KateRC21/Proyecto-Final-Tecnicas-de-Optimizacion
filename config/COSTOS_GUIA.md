# 💰 Guía Completa del Módulo de Costos

## 📋 Descripción General

Este módulo proporciona configuración completa de costos operacionales para el sistema de optimización de ambulancias, con valores reales calculados para Medellín, Colombia.

---

## 📊 Estructura de Costos Disponible

### Tipos de Ambulancia y Prioridades

```python
# Mapeo automático de prioridad a ambulancia
'leve'    → TAB_leve      ($5.585/km  + $35.000 activación)
'media'   → TAM_moderada  ($10.534/km + $60.000 activación)
'crítica' → TAM_grave     ($20.396/km + $85.000 activación)
```

### Valores Calculados (COP)

| Tipo | Costo Fijo | Costo/km | Total 10km |
|------|------------|----------|------------|
| TAB Leve | $35.000 | $5.585 | $90.850 |
| TAM Moderada | $60.000 | $10.534 | $165.340 |
| TAM Grave | $85.000 | $20.396 | $288.960 |

---

## 🔧 Ejemplos de Uso

### Ejemplo 1: Importar y Ver Configuración

```python
from config.costos import COSTOS, PRIORIDAD_A_AMBULANCIA

# Ver configuración completa de una ambulancia
config_tab = COSTOS['TAB_leve']
print(f"Nombre: {config_tab['nombre']}")
print(f"Costo fijo: ${config_tab['costo_fijo_activacion']:,}")
print(f"Costo por km: ${config_tab['costo_por_km']:,}")
print(f"Personal: {', '.join(config_tab['equipo_medico'])}")

# Ver desglose detallado
desglose = config_tab['desglose_km']
print(f"\nDesglose por kilómetro:")
print(f"  Depreciación/Mant: ${desglose['depreciacion_mantenimiento']}")
print(f"  Combustible:       ${desglose['combustible']}")
print(f"  Personal:          ${desglose['personal']}")
print(f"  Insumos:           ${desglose['insumos']}")
```

**Salida esperada:**
```
Nombre: TAB - Transporte Asistencial Básico
Costo fijo: $35,000
Costo por km: $5,585
Personal: conductor, auxiliar_enfermeria

Desglose por kilómetro:
  Depreciación/Mant: $1910
  Combustible:       $1031
  Personal:          $769
  Insumos:           $1875
```

### Ejemplo 2: Calcular Costo de un Servicio

```python
from config.costos import calcular_costo_servicio

# Servicio de ambulancia TAB: 15 km
distancia = 15  # km
costo_tab = calcular_costo_servicio('TAB_leve', distancia)
print(f"Costo TAB (15 km): ${costo_tab:,.0f} COP")
# Resultado: $118,775 = $35,000 + (15 * $5,585)

# Servicio de ambulancia TAM grave: 8 km
costo_tam_grave = calcular_costo_servicio('TAM_grave', 8)
print(f"Costo TAM grave (8 km): ${costo_tam_grave:,.0f} COP")
# Resultado: $248,168 = $85,000 + (8 * $20,396)

# Comparar costos
print(f"\nDiferencia: ${costo_tam_grave - costo_tab:,.0f} COP")
```

### Ejemplo 3: Obtener Desglose Detallado

```python
from config.costos import obtener_desglose_costo

distancia = 12  # km
desglose = obtener_desglose_costo('TAM_moderada', distancia)

print("Desglose completo del servicio:")
print(f"  Costo fijo:         ${desglose['costo_fijo']:,.0f}")
print(f"  Depreciación/Mant:  ${desglose['depreciacion_mantenimiento']:,.0f}")
print(f"  Combustible:        ${desglose['combustible']:,.0f}")
print(f"  Personal:           ${desglose['personal']:,.0f}")
print(f"  Insumos:            ${desglose['insumos']:,.0f}")
print(f"  ─────────────────────────────")
print(f"  TOTAL:              ${desglose['total']:,.0f}")
```

### Ejemplo 4: Validar Asignación de Ambulancia

```python
from config.costos import validar_tipo_ambulancia_para_prioridad, PRIORIDAD_A_AMBULANCIA

# Verificar si una ambulancia es apropiada para una prioridad
prioridad = 'crítica'
tipo_ambulancia = 'TAB_leve'

es_valido = validar_tipo_ambulancia_para_prioridad(tipo_ambulancia, prioridad)

if not es_valido:
    print(f"❌ {tipo_ambulancia} NO es apropiada para urgencia {prioridad}")
else:
    print(f"✅ {tipo_ambulancia} es apropiada para urgencia {prioridad}")

# Encontrar la ambulancia correcta
ambulancia_correcta = PRIORIDAD_A_AMBULANCIA[prioridad]
print(f"Para urgencia {prioridad}, usar: {ambulancia_correcta}")
```

### Ejemplo 5: Generar Tabla Comparativa

```python
from config.costos import COSTOS
import pandas as pd

def generar_tabla_comparativa():
    """Genera tabla comparativa de costos"""
    datos = []
    
    for tipo, config in COSTOS.items():
        datos.append({
            'Tipo': config['nombre'],
            'Prioridad': config['prioridad_asignada'].capitalize(),
            'Personal': len(config['equipo_medico']),
            'Costo Fijo': f"${config['costo_fijo_activacion']:,}",
            'Costo/km': f"${config['costo_por_km']:,}",
            'Vel. Min': f"{config['velocidad_min_requerida']} km/h",
            'Vel. Max': f"{config['velocidad_max_requerida']} km/h"
        })
    
    df = pd.DataFrame(datos)
    return df

# Usar en notebook o reportes
tabla = generar_tabla_comparativa()
print(tabla.to_string(index=False))
```

---

## 🖥️ Uso en la GUI (Streamlit)

### Sistema de Costos Editables Implementado

El módulo incluye un sistema completo para que el usuario edite costos desde la interfaz gráfica de manera simple.

### Características de la GUI:

- ✅ **Solo 2 campos por prioridad:** Costo Fijo + Costo/km
- ✅ **6 campos en total** (2 × 3 tipos) - Muy simple para el usuario
- ✅ **Valores por defecto pre-cargados**
- ✅ **Cálculo de ejemplo en tiempo real** (para 10 km)
- ✅ **Desglose detallado opcional** (colapsado)
- ✅ **Botón de restaurar valores por defecto**
- ✅ **Guardado automático** en `st.session_state['costos_usuario']`

### Vista de la Interfaz:

```
┌─────────────────────────────────────────────┐
│  💰 Costos Operacionales                    │
├─────────────────────────────────────────────┤
│  ▼ 🟡 Urgencia LEVE (TAB)                   │
│     ┌──────────────┬──────────────┐          │
│     │ Costo Fijo   │  Costo/km    │          │
│     │ $ 35,000     │  $ 5,585     │          │
│     └──────────────┴──────────────┘          │
│     💡 Ejemplo 10 km: $90,850 COP            │
│     ▶ 📊 Desglose del valor por defecto     │
│                                              │
│  ▼ 🟠 Urgencia MEDIA (TAM)                  │
│     (similar...)                             │
│                                              │
│  ▼ 🔴 Urgencia CRÍTICA (TAM Grave)          │
│     (similar...)                             │
│                                              │
│  [🔄 Restaurar]  [❓]                        │
└─────────────────────────────────────────────┘
```

### Integración en la GUI:

```python
# En gui/app.py
import streamlit as st
from gui.components.sidebar import crear_sidebar

def main():
    st.title("🚑 Sistema de Optimización")
    
    # Crear sidebar (incluye configuración de costos automáticamente)
    crear_sidebar()
    
    # Los costos editados se guardan automáticamente en:
    # st.session_state['costos_usuario']
    
    # Ejecutar optimización
    if st.button("🚀 Ejecutar"):
        ejecutar_optimizacion()

def ejecutar_optimizacion():
    # Obtener costos editados por el usuario
    costos_usuario = st.session_state.get('costos_usuario', None)
    
    # Crear modelo con costos personalizados
    modelo = AmbulanceOptimizationModel(
        grafo=st.session_state.grafo,
        emergencias=st.session_state.emergencias,
        hospitales=st.session_state.hospitales,
        costos_usuario=costos_usuario  # ← Aquí se pasan
    )
    
    # Resolver
    modelo.construir_modelo()
    modelo.resolver()
```

---

## 🎯 Uso en el Modelo de Optimización

### Función Helper Principal: `calcular_costo_con_valores_usuario()`

Esta función usa costos personalizados del usuario si están disponibles, o valores por defecto automáticamente.

```python
from config.costos import calcular_costo_con_valores_usuario

# Automáticamente usa costos del usuario si existen, o por defecto si no
costo = calcular_costo_con_valores_usuario(
    prioridad='leve',
    distancia_km=15,
    costos_usuario=costos_usuario  # Puede ser None
)
```

### Integración en el Modelo:

```python
# En src/models/optimization_model.py

from config.costos import calcular_costo_con_valores_usuario

class AmbulanceOptimizationModel:
    def __init__(self, grafo, emergencias, hospitales, parametros, costos_usuario=None):
        self.grafo = grafo
        self.emergencias = emergencias
        self.hospitales = hospitales
        self.parametros = parametros
        self.costos_usuario = costos_usuario  # Guardar costos del usuario
    
    def construir_funcion_objetivo(self):
        """
        Minimiza: Tiempo ponderado + Costo total
        """
        costo_total = 0
        tiempo_total = 0
        
        for emergencia in self.emergencias:
            prioridad = emergencia['prioridad']
            distancia = emergencia['distancia_estimada']
            tiempo = emergencia['tiempo_estimado']
            
            # Calcular costo (usa valores usuario o por defecto)
            costo = calcular_costo_con_valores_usuario(
                prioridad=prioridad,
                distancia_km=distancia,
                costos_usuario=self.costos_usuario  # ← Usa costos editados
            )
            
            # Agregar al total con peso de prioridad
            peso_prioridad = self._obtener_peso_prioridad(prioridad)
            costo_total += costo
            tiempo_total += peso_prioridad * tiempo
        
        # Función objetivo: balance entre tiempo y costo
        w1 = self.parametros.get('peso_tiempo', 0.6)
        w2 = self.parametros.get('peso_costo', 0.4)
        
        return w1 * tiempo_total + w2 * costo_total
    
    def _obtener_peso_prioridad(self, prioridad):
        """Retorna peso numérico según prioridad"""
        pesos = {'leve': 1, 'media': 2, 'crítica': 3}
        return pesos.get(prioridad, 1)
```

### Con Variables de Decisión (PuLP):

```python
import pulp
from config.costos import PRIORIDAD_A_AMBULANCIA, COSTOS

class AmbulanceOptimizationModel:
    def __init__(self, grafo, emergencias, hospitales, parametros, costos_usuario=None):
        self.grafo = grafo
        self.emergencias = emergencias
        self.costos_usuario = costos_usuario
        self.modelo = pulp.LpProblem("Ambulance_Routing", pulp.LpMinimize)
    
    def _definir_funcion_objetivo(self):
        """Define función objetivo con costos editables"""
        
        # Componente de costo
        costo_total = 0
        for k, emergencia in enumerate(self.emergencias):
            prioridad = emergencia['prioridad']
            
            # Obtener costos (usuario o por defecto)
            if self.costos_usuario and prioridad in self.costos_usuario:
                costo_fijo = self.costos_usuario[prioridad]['costo_fijo']
                costo_km = self.costos_usuario[prioridad]['costo_km']
            else:
                tipo_amb = PRIORIDAD_A_AMBULANCIA[prioridad]
                costo_fijo = COSTOS[tipo_amb]['costo_fijo_activacion']
                costo_km = COSTOS[tipo_amb]['costo_por_km']
            
            # Costo fijo + costo variable por distancia
            costo_total += costo_fijo * self.vars_asignacion[k]
            
            # Costo por kilómetro (suma de aristas usadas)
            for i, j in self.grafo.edges():
                longitud_km = self.grafo[i][j][0]['length'] / 1000
                costo_total += costo_km * longitud_km * self.vars_flujo[i, j, k]
        
        # Función objetivo combinada
        w1 = self.parametros.get('peso_tiempo', 0.6)
        w2 = self.parametros.get('peso_costo', 0.4)
        
        self.modelo += w1 * tiempo_total + w2 * costo_total
```

---

## 🔄 Flujo de Datos Completo

```
┌─────────────────────────────────────────────────────────┐
│  1. USUARIO EDITA EN GUI                                 │
│     • Costo Fijo: $40,000                               │
│     • Costo/km: $6,000                                  │
└───────────────────┬─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  2. GUARDADO EN SESSION STATE                            │
│     st.session_state['costos_usuario'] = {              │
│         'leve': {'costo_fijo': 40000, 'costo_km': 6000} │
│         'media': {...}                                   │
│         'crítica': {...}                                 │
│     }                                                    │
└───────────────────┬─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  3. PASADO AL MODELO                                     │
│     modelo = AmbulanceOptimizationModel(                │
│         ...,                                             │
│         costos_usuario=st.session_state['costos_usuario']│
│     )                                                    │
└───────────────────┬─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  4. USADO EN FUNCIÓN OBJETIVO                            │
│     costo = calcular_costo_con_valores_usuario(...)     │
│     # Retorna: Usa valores editados o por defecto       │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 Uso en Visualización

```python
# En src/visualization/results_plotter.py

from config.costos import COSTOS
import plotly.graph_objects as go

def graficar_costos_por_tipo(resultado):
    """Gráfico de costos desglosados por tipo de ambulancia"""
    tipos = []
    costos = []
    colores = []
    
    for asignacion in resultado['asignaciones']:
        tipo = asignacion['tipo_ambulancia']
        tipos.append(COSTOS[tipo]['nombre'])
        costos.append(asignacion['costo'])
        colores.append(COSTOS[tipo]['color_visualizacion'])
    
    fig = go.Figure(data=[
        go.Bar(
            x=tipos,
            y=costos,
            marker_color=colores,
            text=[f"${c:,.0f}" for c in costos],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Costos por Tipo de Ambulancia",
        xaxis_title="Tipo de Ambulancia",
        yaxis_title="Costo Total (COP)"
    )
    
    return fig
```

---

## 🧪 Tests Unitarios

```python
# En tests/test_costs.py

import pytest
from config.costos import (
    calcular_costo_servicio,
    calcular_costo_con_valores_usuario,
    validar_tipo_ambulancia_para_prioridad,
    COSTOS
)

def test_calcular_costo_servicio_tab():
    """Test: Cálculo correcto de costo TAB"""
    costo = calcular_costo_servicio('TAB_leve', distancia_km=10)
    esperado = 35000 + (10 * 5585)
    assert costo == esperado

def test_validar_ambulancia_correcta():
    """Test: Validación de ambulancia apropiada"""
    assert validar_tipo_ambulancia_para_prioridad('TAB_leve', 'leve') == True
    assert validar_tipo_ambulancia_para_prioridad('TAB_leve', 'crítica') == False
    assert validar_tipo_ambulancia_para_prioridad('TAM_grave', 'crítica') == True

def test_calcular_con_valores_usuario():
    """Test: Usa valores del usuario correctamente"""
    costos = {
        'leve': {'costo_fijo': 40000, 'costo_km': 6000}
    }
    
    costo = calcular_costo_con_valores_usuario('leve', 10, costos)
    esperado = 40000 + (10 * 6000)
    
    assert costo == esperado

def test_usa_valores_por_defecto_si_no_hay_usuario():
    """Test: Usa valores por defecto automáticamente"""
    costo = calcular_costo_con_valores_usuario('leve', 10, None)
    esperado = 35000 + (10 * 5585)
    
    assert costo == esperado

def test_desglose_suma_correcta():
    """Test: El desglose suma al costo total por km"""
    for tipo, config in COSTOS.items():
        desglose = config['desglose_km']
        suma_desglose = sum(desglose.values())
        assert suma_desglose == config['costo_por_km'], \
            f"Desglose de {tipo} no suma correctamente"
```

---

## ✨ Funciones Disponibles

| Función | Descripción | Uso |
|---------|-------------|-----|
| `COSTOS` | Diccionario con configuración completa | `COSTOS['TAB_leve']` |
| `PRIORIDAD_A_AMBULANCIA` | Mapeo de prioridad a tipo | `PRIORIDAD_A_AMBULANCIA['leve']` |
| `calcular_costo_servicio()` | Calcula costo total | `calcular_costo_servicio('TAB_leve', 15)` |
| `calcular_costo_con_valores_usuario()` | Usa costos editados o por defecto | `calcular_costo_con_valores_usuario('leve', 15, costos)` |
| `obtener_desglose_costo()` | Desglose detallado | `obtener_desglose_costo('TAM_grave', 10)` |
| `obtener_info_ambulancia_por_prioridad()` | Info completa por prioridad | `obtener_info_ambulancia_por_prioridad('leve')` |
| `validar_tipo_ambulancia_para_prioridad()` | Valida asignación | `validar_tipo_ambulancia_para_prioridad('TAB', 'leve')` |
| `VALORES_DEFAULT_INTERFAZ` | Valores para GUI | Para controles de Streamlit |

---

## ✅ Ventajas del Sistema

### Para el Usuario:
- ✅ **Simple:** Solo 6 campos para editar (2 × 3 tipos)
- ✅ **Intuitivo:** Costo fijo + Costo/km es claro
- ✅ **Visual:** Ve ejemplo de cálculo en tiempo real
- ✅ **Informativo:** Puede ver desglose si tiene curiosidad
- ✅ **Seguro:** Botón para restaurar valores por defecto

### Para el Desarrollador:
- ✅ **Modular:** Función `configurar_costos_sidebar()` separada
- ✅ **Reutilizable:** `calcular_costo_con_valores_usuario()` funciona en cualquier parte
- ✅ **Robusto:** Valores por defecto automáticos si no se edita
- ✅ **Mantenible:** Código claro y bien documentado
- ✅ **Testeable:** Función pura, fácil de probar

### Para el Proyecto:
- ✅ **Cumple requisito:** "Costos configurables en la GUI" ✓
- ✅ **Flexible:** Usuario puede ajustar según contexto
- ✅ **Profesional:** Desglose detallado muestra seriedad del cálculo
- ✅ **Extensible:** Fácil agregar más tipos si se necesita

---

## 📊 Comparación: Antes vs Después

### ❌ Antes (Complejo):
```
Usuario debe ingresar:
• Depreciación/Mantenimiento por km
• Combustible por km  
• Personal por km
• Insumos por km
• Costo fijo
─────────────────────────
5 valores × 3 tipos = 15 campos 😰
```

### ✅ Después (Simple):
```
Usuario solo ingresa:
• Costo Fijo
• Costo por km
─────────────────────────
2 valores × 3 tipos = 6 campos 😊
```

---

## 🔧 Verificación

Para verificar que el módulo funciona correctamente:

```bash
cd config
python test_costos.py
```

Deberías ver:
```
✅ TODOS LOS TESTS PASARON EXITOSAMENTE
```

---

## 🎓 Resumen Ejecutivo

Se ha implementado un sistema completo y funcional para que el usuario edite costos operacionales en la GUI de forma simple (solo 2 valores por tipo), manteniendo toda la fundamentación técnica y desglose detallado como referencia opcional.

**El sistema:**
- ✅ Es simple de usar (6 campos en total)
- ✅ Es robusto (valores por defecto automáticos)
- ✅ Es flexible (usuario puede personalizar)
- ✅ Es transparente (desglose disponible)
- ✅ Es profesional (bien documentado y testeado)
- ✅ Cumple con los requisitos del proyecto

---

**¡Todo listo para usar en tu proyecto! 🚀**

