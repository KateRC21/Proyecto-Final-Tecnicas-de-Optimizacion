# 🚀 Guía de Despliegue en Streamlit Cloud

## 📋 Tabla de Contenidos
- [Prerrequisitos](#prerrequisitos)
- [Paso 1: Preparar el Repositorio Local](#paso-1-preparar-el-repositorio-local)
- [Paso 2: Crear Repositorio en GitHub](#paso-2-crear-repositorio-en-github)
- [Paso 3: Subir el Código a GitHub](#paso-3-subir-el-código-a-github)
- [Paso 4: Registrarse en Streamlit Cloud](#paso-4-registrarse-en-streamlit-cloud)
- [Paso 5: Configurar el Despliegue](#paso-5-configurar-el-despliegue)
- [Paso 6: Verificar y Monitorear](#paso-6-verificar-y-monitorear)
- [Solución de Problemas](#solución-de-problemas)
- [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)

---

## Prerrequisitos

Antes de comenzar, asegúrate de tener:

- ✅ **Cuenta de GitHub** (gratuita)
- ✅ **Git instalado** en tu computadora
- ✅ **Aplicación funcionando localmente** (prueba con `streamlit run gui/app.py`)
- ✅ **Internet** para subir archivos y configurar

---

## Paso 1: Preparar el Repositorio Local

### 1.1 Inicializar Git (si no lo has hecho)

Abre PowerShell en la carpeta de tu proyecto y ejecuta:

```powershell
# Navega a tu carpeta del proyecto
cd "C:\Users\Usuario\Documents\Universidad UPB\Quinto Semestre\Trabajo Final Técnicas de Optimización"

# Inicializar repositorio Git
git init
```

### 1.2 Configurar Git (primera vez)

Si es la primera vez que usas Git en esta computadora:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tuemail@ejemplo.com"
```

### 1.3 Preparar archivos importantes

Ya tienes estos archivos creados:
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `.gitignore` - Archivos a ignorar
- ✅ `packages.txt` - Dependencias del sistema (NUEVO - creado automáticamente)
- ✅ `.streamlit/config.toml` - Configuración de Streamlit (NUEVO - creado automáticamente)

### 1.4 Verificar archivos críticos

Asegúrate que estos archivos existan en tu proyecto:
```
✅ requirements.txt
✅ .gitignore
✅ packages.txt (nuevo)
✅ .streamlit/config.toml (nuevo)
✅ gui/app.py (tu aplicación principal)
✅ preparar_datos.py (script de inicialización)
✅ README.md
```

### 1.5 Agregar archivos al repositorio

```powershell
# Agregar SOLO los archivos necesarios (no datos procesados grandes)
git add requirements.txt
git add .gitignore
git add packages.txt
git add .streamlit/
git add gui/
git add src/
git add config/
git add docs/
git add preparar_datos.py
git add ejecutar_app.py
git add README.md
git add DESPLIEGUE_STREAMLIT.md
git add notebooks/

# Hacer el primer commit
git commit -m "Initial commit: Sistema de Optimización de Rutas de Ambulancias"
```

**⚠️ IMPORTANTE:** NO subas las carpetas `data/`, `cache/`, `outputs/` ni `__pycache__/` ya que:
- Son archivos generados automáticamente
- Pueden ser muy pesados
- Se regenerarán en Streamlit Cloud

---

## Paso 2: Crear Repositorio en GitHub

### 2.1 Ir a GitHub

1. Abre tu navegador y ve a: **https://github.com**
2. Inicia sesión (o crea una cuenta si no tienes)

### 2.2 Crear nuevo repositorio

1. Click en el botón **"+"** (arriba derecha) → **"New repository"**
2. Completa los campos:
   - **Repository name:** `optimizacion-ambulancias-medellin`
   - **Description:** `Sistema de optimización de rutas para ambulancias en Medellín - Streamlit`
   - **Visibility:** Elige **Public** (necesario para Streamlit Cloud gratuito)
   - **NO marques** "Initialize this repository with a README" (ya tienes uno)
3. Click en **"Create repository"**

### 2.3 Copiar la URL del repositorio

Verás una página con instrucciones. Copia la URL que aparece, algo como:
```
https://github.com/tu-usuario/optimizacion-ambulancias-medellin.git
```

---

## Paso 3: Subir el Código a GitHub

### 3.1 Conectar tu repositorio local con GitHub

En PowerShell, desde tu carpeta del proyecto:

```powershell
# Agregar el repositorio remoto (reemplaza con TU URL de GitHub)
git remote add origin https://github.com/TU-USUARIO/optimizacion-ambulancias-medellin.git

# Verificar que se agregó correctamente
git remote -v
```

### 3.2 Subir tu código

```powershell
# Cambiar el nombre de la rama principal a 'main' (estándar actual)
git branch -M main

# Subir todos los archivos a GitHub
git push -u origin main
```

**Si te pide credenciales:**
- **Username:** Tu usuario de GitHub
- **Password:** Usa un **Personal Access Token** (no tu contraseña)
  - Ve a: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - Dale permisos a "repo"
  - Copia el token y úsalo como contraseña

### 3.3 Verificar en GitHub

1. Refresca tu repositorio en GitHub
2. Deberías ver todos tus archivos ahí
3. Verifica que `gui/app.py` y `requirements.txt` estén presentes

---

## Paso 4: Registrarse en Streamlit Cloud

### 4.1 Ir a Streamlit Cloud

Abre tu navegador y ve a: **https://streamlit.io/cloud**

### 4.2 Crear cuenta

1. Click en **"Sign up"**
2. Elige **"Continue with GitHub"**
3. Autoriza a Streamlit Cloud para acceder a tu cuenta de GitHub
4. Completa tu perfil (si es necesario)

---

## Paso 5: Configurar el Despliegue

### 5.1 Crear nueva app

1. Una vez dentro de Streamlit Cloud, click en **"New app"**
2. Te pedirá conectar con GitHub (si no lo hiciste ya)

### 5.2 Configurar la aplicación

Completa los campos:

**Repository:**
- Selecciona: `tu-usuario/optimizacion-ambulancias-medellin`

**Branch:**
- Deja: `main`

**Main file path:**
- Escribe: `gui/app.py`

**Advanced settings** (click en "Advanced settings"):

#### Python version:
- Selecciona: **3.11** (o la versión que usas localmente)

#### Secrets (Opcional):
- Puedes dejar vacío por ahora

**App URL (opcional):**
- Puedes personalizar la URL o dejar la que genera automáticamente
- Ejemplo: `optimizacion-ambulancias-medellin`

### 5.3 Desplegar

1. Click en **"Deploy!"**
2. Streamlit Cloud comenzará a:
   - Clonar tu repositorio
   - Instalar dependencias de `requirements.txt`
   - Instalar paquetes del sistema de `packages.txt`
   - Ejecutar tu aplicación

**⏱️ Tiempo estimado:** 3-10 minutos la primera vez

---

## Paso 6: Verificar y Monitorear

### 6.1 Ver logs de despliegue

Mientras se despliega, verás logs en tiempo real:
- ✅ Instalando dependencias...
- ✅ Preparando ambiente...
- ✅ Iniciando aplicación...

### 6.2 Primera ejecución

**⚠️ IMPORTANTE:** La primera vez que alguien acceda a tu app, se ejecutará `preparar_datos.py` automáticamente porque no hay datos precargados.

Esto significa:
- La app descargará el mapa de OpenStreetMap
- Generará los archivos procesados
- **Puede tardar 2-5 minutos** en la primera carga

**Solución recomendada:**
- Accede tú primero a la app después del despliegue
- Espera a que termine de cargar los datos
- Después comparte la URL con otros

### 6.3 Acceder a tu aplicación

Una vez desplegada, verás:
- ✅ **Estado:** Running
- 🌐 **URL:** `https://optimizacion-ambulancias-medellin.streamlit.app`

Click en la URL para abrir tu aplicación en vivo.

### 6.4 Compartir la aplicación

Simplemente comparte la URL con quien quieras:
```
https://tu-app.streamlit.app
```

---

## Solución de Problemas

### ❌ Error: "ModuleNotFoundError"

**Causa:** Falta una dependencia en `requirements.txt`

**Solución:**
```powershell
# Agrega la dependencia faltante a requirements.txt
# Ejemplo: echo "nombre-paquete>=version" >> requirements.txt

# Haz commit y push
git add requirements.txt
git commit -m "Agregado dependencia faltante"
git push
```

Streamlit Cloud se actualizará automáticamente.

---

### ❌ Error: "No module named 'osmnx'"

**Causa:** Problema con dependencias geoespaciales

**Solución:**
El archivo `packages.txt` (que creamos) debería resolver esto. Si persiste:
1. Verifica que `packages.txt` esté en la raíz del proyecto
2. Verifica que tenga estas líneas:
   ```
   gdal-bin
   libgdal-dev
   libspatialindex-dev
   ```

---

### ❌ Error: "File not found: data/processed/datos_modelo.pkl"

**Causa:** La aplicación intenta cargar datos que no existen en el servidor

**Solución:** Esto es esperado. Tu app debería manejar esto automáticamente:
- El archivo `preparar_datos.py` se ejecuta cuando no encuentra datos
- Si no lo hace automáticamente, modifica `gui/app.py` para ejecutar `preparar_datos.py` en la primera carga

---

### ❌ Error: "Memory limit exceeded"

**Causa:** Streamlit Cloud gratuito tiene límite de RAM (1 GB)

**Solución:**
1. Reduce el área de estudio en `config/parametros.py`
2. Usa menos emergencias
3. O considera actualizar a Streamlit Cloud Pro

---

### ❌ La aplicación se queda "cargando" indefinidamente

**Causa:** El script `preparar_datos.py` está tardando mucho

**Solución:**
1. Ve a los logs de Streamlit Cloud
2. Verifica que no haya errores
3. Si está descargando datos de OSM, espera (puede tardar hasta 5 min)

---

### ❌ "Failed to download OSM data"

**Causa:** Problema de red o límites de OSM

**Solución:**
1. Reduce el área de estudio
2. Agrega manejo de reintentos en `osm_loader.py`
3. O precarga los datos localmente y súbelos al repositorio (si son < 50 MB)

---

## Limitaciones y Consideraciones

### 📊 Streamlit Cloud Gratuito

| Recurso | Límite |
|---------|--------|
| RAM | 1 GB |
| CPU | Compartida |
| Almacenamiento | 1 GB |
| Apps públicas | Ilimitadas |
| Apps privadas | 1 |

### ⚠️ Consideraciones Importantes

1. **Datos persistentes:** Los archivos generados (cache, datos procesados) se **perderán** cuando la app se reinicie. Considera:
   - Usar st.cache_data para cachear en memoria
   - Subir datos procesados al repo (si son < 50 MB)
   - Usar base de datos externa para persistencia

2. **Tiempos de carga:** La primera carga puede ser lenta (2-5 min) por descarga de OSM

3. **Actualizaciones automáticas:** Cada vez que hagas `git push`, Streamlit Cloud se actualizará automáticamente

4. **Sleep después de inactividad:** Si nadie usa tu app por ~5 días, se "duerme". Al acceder de nuevo, tardará ~30s en despertar.

---

## 🔄 Actualizar tu Aplicación

Cuando hagas cambios en tu código local:

```powershell
# Guardar cambios
git add .
git commit -m "Descripción de tus cambios"
git push

# Streamlit Cloud detectará los cambios y se actualizará automáticamente
```

---

## 📧 Soporte

Si tienes problemas:
1. **Logs de Streamlit Cloud:** Revisa los logs en tiempo real
2. **Documentación oficial:** https://docs.streamlit.io/streamlit-community-cloud
3. **Foro de Streamlit:** https://discuss.streamlit.io/

---

## ✨ Siguiente Nivel

Para producción profesional, considera:

1. **Streamlit Cloud Pro:**
   - Más RAM y CPU
   - Apps privadas ilimitadas
   - Dominios personalizados

2. **Base de datos externa:**
   - PostgreSQL
   - MongoDB
   - AWS S3 para datos grandes

3. **Autenticación:**
   - st-authenticator
   - OAuth2

4. **Monitoreo:**
   - Google Analytics
   - Sentry para errores

---

**¡Felicidades! 🎉 Tu aplicación ahora está en la nube y accesible desde cualquier lugar del mundo.**

**URL de tu app:** `https://tu-app.streamlit.app`

---

**Desarrollado para el curso de Técnicas de Optimización - UPB Medellín 🇨🇴**

