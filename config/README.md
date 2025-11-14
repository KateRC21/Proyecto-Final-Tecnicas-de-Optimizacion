# Módulo de Configuración

Este directorio contiene todas las configuraciones del sistema de optimización de ambulancias.

## 📁 Archivos

### ✅ `costos.py` - **COMPLETADO**
Configuración completa de costos operacionales con valores reales calculados para Medellín, Colombia.

**Incluye:**
- 3 tipos de ambulancia (TAB, TAM moderada, TAM grave)
- Costos detallados por kilómetro
- Desglose por componente (depreciación, combustible, personal, insumos)
- Funciones de utilidad listas para usar

**Valores:**
| Tipo | Costo Fijo | Costo/km |
|------|------------|----------|
| TAB Leve | $35.000 | $5.585 |
| TAM Moderada | $60.000 | $10.534 |
| TAM Grave | $85.000 | $20.396 |

**Documentación:** 
- `COSTOS_GUIA.md` - Guía completa con ejemplos y uso en modelo/GUI ✨

**Verificar:** Ejecutar `python test_costos.py`

**Costos Editables en GUI:** ✅ **IMPLEMENTADO**
- Usuario solo edita 2 valores por prioridad: costo fijo + costo/km
- Valores se guardan en `st.session_state['costos_usuario']`
- Modelo usa `calcular_costo_con_valores_usuario()` automáticamente
- Desglose detallado disponible como referencia (opcional)

---

### ⏳ `parametros.py` - Por completar
Parámetros del modelo de optimización.

**Debe incluir:**
- `R_MIN`, `R_MAX`: Rango de velocidades requeridas (km/h)
- `C_MIN`, `C_MAX`: Rango de capacidades de vías (km/h)
- Pesos de la función objetivo
- Otros parámetros del modelo

**Valores sugeridos:**
```python
PARAMETROS = {
    'velocidades_requeridas': {
        'min': 40,  # km/h
        'max': 80   # km/h
    },
    'capacidades_vias': {
        'min': 30,   # km/h
        'max': 100   # km/h
    },
    'pesos_funcion_objetivo': {
        'tiempo': 0.6,
        'costo': 0.4
    },
    'tiempo_max_respuesta': {
        'leve': 30,      # minutos
        'media': 20,     # minutos
        'crítica': 15    # minutos
    }
}
```

---

### ⏳ `ubicaciones.py` - Por completar
Coordenadas de hospitales y zonas de Medellín.

**Debe incluir:**
- Lista de hospitales con coordenadas (lat, lon)
- Ambulancias disponibles por hospital
- Zonas de alta demanda de emergencias
- Límites geográficos de la ciudad

**Hospitales sugeridos para incluir:**
1. Hospital Pablo Tobón Uribe (6.2089, -75.5664)
2. Hospital General de Medellín (6.2476, -75.5658)
3. Clínica Las Américas (6.2036, -75.5789)
4. Hospital San Vicente Fundación (6.2637, -75.5664)
5. Clínica El Poblado (6.2087, -75.5666)
6. Clínica Medellín (6.2442, -75.5812)

---

## 🚀 Cómo usar

### Importar configuraciones completas

```python
from config import COSTOS, PARAMETROS, HOSPITALES
```

### Importar funciones específicas

```python
from config.costos import calcular_costo_servicio
from config.parametros import PARAMETROS
from config.ubicaciones import HOSPITALES
```

### Ejemplo completo

```python
from config.costos import COSTOS, PRIORIDAD_A_AMBULANCIA, calcular_costo_servicio

# Obtener tipo de ambulancia para una emergencia
emergencia = {
    'prioridad': 'crítica',
    'distancia_estimada': 12  # km
}

tipo_ambulancia = PRIORIDAD_A_AMBULANCIA[emergencia['prioridad']]
# → 'TAM_grave'

# Calcular costo del servicio
costo = calcular_costo_servicio(tipo_ambulancia, emergencia['distancia_estimada'])
# → $288,752 COP

print(f"Ambulancia: {COSTOS[tipo_ambulancia]['nombre']}")
print(f"Costo total: ${costo:,} COP")
```

---

## ✅ Verificación

Para verificar que el módulo de costos funciona correctamente:

```bash
cd config
python test_costos.py
```

Deberías ver:
```
✅ TODOS LOS TESTS PASARON EXITOSAMENTE
```

---

## 📚 Documentación adicional

- `COSTOS_GUIA.md`: Guía completa con ejemplos y uso en modelo/GUI
- `../docs/metodologia.md`: Formulación matemática del modelo
- `../RESUMEN_IMPLEMENTACION.md`: Estado de implementación del proyecto

---

## 🔄 Próximos pasos

1. ✅ ~~Completar `costos.py`~~ **HECHO**
2. ⏳ Completar `parametros.py` con valores razonables
3. ⏳ Completar `ubicaciones.py` con hospitales de Medellín
4. ⏳ Descomentar imports en `__init__.py`
5. ✅ Verificar con tests

---

## 💡 Tips

- Los valores en `costos.py` son editables desde la GUI
- Usa rangos de velocidad consistentes con la capacidad de las vías
- Las coordenadas deben ser en formato decimal (no grados/minutos/segundos)
- Verifica que los hospitales estén dentro de los límites de Medellín

---

**Última actualización:** Noviembre 2024  
**Estado:** Módulo de costos completado ✅

